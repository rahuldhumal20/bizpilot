
import json

from app.config import llm
from app.graph.state import BizPilotState


REQUIRED_FIELDS = [
    "currency",
    "initial_cost_min",
    "initial_cost_max",
    "monthly_opex_min",
    "monthly_opex_max",
    "annual_gross_benefit_min",
    "annual_gross_benefit_max",
]


def get_response_text(content):
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        return "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        ).strip()

    raise ValueError("Unsupported LLM response format.")


def extract_json(content):
    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()
        content = "\n".join(
            line for line in lines
            if not line.strip().startswith("```")
        )

    start = content.find("{")

    if start == -1:
        raise ValueError("No JSON object found.")

    data, _ = json.JSONDecoder().raw_decode(content[start:])

    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object.")

    return data


def validate_response(data, currency):

    for field in REQUIRED_FIELDS:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    if data["currency"] != currency:
        raise ValueError("Currency mismatch.")

    numeric_fields = [
        "initial_cost_min",
        "initial_cost_max",
        "monthly_opex_min",
        "monthly_opex_max",
    ]

    for field in numeric_fields:
        value = data[field]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} must be numeric.")

        if value < 0:
            raise ValueError(f"{field} cannot be negative.")

    benefit_fields = [
        "annual_gross_benefit_min",
        "annual_gross_benefit_max",
    ]

    for field in benefit_fields:
        value = data[field]

        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or value < 0
        ):
            raise ValueError(f"{field} must be non-negative or null.")

    if data["initial_cost_min"] > data["initial_cost_max"]:
        raise ValueError("Initial cost minimum exceeds maximum.")

    if data["monthly_opex_min"] > data["monthly_opex_max"]:
        raise ValueError("Monthly cost minimum exceeds maximum.")

    min_benefit = data["annual_gross_benefit_min"]
    max_benefit = data["annual_gross_benefit_max"]

    if min_benefit is not None and max_benefit is not None:
        if min_benefit > max_benefit:
            raise ValueError("Annual benefit minimum exceeds maximum.")

    return data


def analyze_cost(state: BizPilotState):

    print("Cost Analyst Agent is working...")

    solution_data = state.get("solution_architecture", {})

    solution = str(
        solution_data.get("solution", solution_data)
        if isinstance(solution_data, dict)
        else solution_data
    )[:2600]

    budget_amount = state.get("budget_amount", 0)
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    prompt = f"""
You are a careful and realistic Business Financial Analyst.

Your task is to estimate the financial requirements of the
solution designed by the Solution Architect.

BUSINESS:
{state.get("business_name")}

INDUSTRY:
{state.get("industry")}

BUSINESS SIZE:
{state.get("business_size")}

CUSTOMER BUDGET:
{currency} {budget_amount}

BUDGET COVERAGE:
{budget_scope}

SOLUTION ARCHITECTURE:
{solution}

Return ONLY one valid JSON object.
Do not use Markdown or code fences.

Use exactly this structure:

{{
  "currency": "{currency}",
  "initial_cost_min": 0,
  "initial_cost_max": 0,
  "monthly_opex_min": 0,
  "monthly_opex_max": 0,
  "annual_gross_benefit_min": null,
  "annual_gross_benefit_max": null,
  "assumptions": [],
  "financial_risks": []
}}

FINANCIAL ESTIMATION RULES:

1. Use the Solution Architect's REQUIRED resources as the basis
   for the cost estimate.
2. Do not add resources that are absent from the recommended
   solution.
3. Do not omit essential resources to make the estimate cheaper.
4. Do not include OPTIONAL resources in the required estimate.
   Mention their possible financial impact in assumptions if relevant.
5. Do not estimate alternative solutions as if they were selected.
6. Separate one-time initial costs from monthly recurring costs.
7. Use the customer's requested currency.
8. Provide realistic indicative ranges, not false precision.
9. Do not invent vendor quotations or claim that estimates
   are verified market prices.
10. Clearly mention when local quotations or supplier confirmation
    are required.
11. Do not invent revenue, savings, customer counts or growth.
12. If annual benefits cannot be reasonably calculated from
    supplied business information, both annual benefit fields
    MUST be null.
13. Unknown benefits must never be represented as zero.
14. All costs must be non-negative numbers.
15. Minimum values must not exceed maximum values.
16. Consider whether the budget covers initial costs only
    or the entire first year.
17. Keep assumptions and financial risks concise.
18. Return complete valid JSON with every required field.
"""

    data = None
    last_error = None

    for attempt in range(1, 3):

        try:
            print(f"Cost Analyst attempt {attempt}/2...")

            response = llm.invoke(prompt)

            raw_response = get_response_text(response.content)
            data = extract_json(raw_response)
            data = validate_response(data, currency)

            print("Financial data validated successfully.")
            break

        except Exception as error:
            last_error = error
            print(f"Attempt {attempt} failed: {error}")

    if data is None:

        print("Cost Analyst failed:", last_error)

        return {
            "cost_analysis": {
                "financial_analysis": (
                    "Financial estimates could not be generated. "
                    "Manual financial review is required."
                ),
                "financial_data": {}
            },
            "agent_logs": [
                {
                    "agent": "Cost Analyst",
                    "status": "needs_review"
                }
            ]
        }

    financial_data = {
        field: data[field]
        for field in REQUIRED_FIELDS
    }

    assumptions = data.get("assumptions", [])
    risks = data.get("financial_risks", [])

    if not isinstance(assumptions, list):
        assumptions = []

    if not isinstance(risks, list):
        risks = []

    min_benefit = data["annual_gross_benefit_min"]
    max_benefit = data["annual_gross_benefit_max"]

    benefit_text = (
        f"{min_benefit:,.2f} to {max_benefit:,.2f}"
        if min_benefit is not None and max_benefit is not None
        else "Not available — requires business data"
    )

    financial_analysis = (
        "## Estimated Financial Requirements\n\n"
        f"- **Currency:** {currency}\n"
        f"- **Budget scope:** {budget_scope}\n"
        f"- **Initial cost:** {currency} "
        f"{data['initial_cost_min']:,.2f} to "
        f"{data['initial_cost_max']:,.2f}\n"
        f"- **Monthly operating cost:** {currency} "
        f"{data['monthly_opex_min']:,.2f} to "
        f"{data['monthly_opex_max']:,.2f}\n"
        f"- **Annual gross benefit:** {benefit_text}\n\n"
        "## Assumptions\n\n"
        + "\n".join(f"- {item}" for item in assumptions)
        + "\n\n## Financial Risks\n\n"
        + "\n".join(f"- {item}" for item in risks)
    )

    return {
        "cost_analysis": {
            "financial_analysis": financial_analysis,
            "financial_data": financial_data
        },
        "agent_logs": [
            {
                "agent": "Cost Analyst",
                "status": "completed"
            }
        ]
    }
