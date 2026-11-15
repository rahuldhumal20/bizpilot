
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
    )[:1800]

    budget_amount = state.get("budget_amount", 0)
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    prompt = f"""
You are a careful business financial analyst.

Business: {state.get("business_name")}
Industry: {state.get("industry")}
Business size: {state.get("business_size")}

Available budget: {currency} {budget_amount}
Budget scope: {budget_scope}

Use the following recommended solution as the SINGLE source
for identifying required resources and estimating costs.

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

Rules:

1. Estimate costs for ALL essential resources in the recommended solution.
2. Do not add hardware, software or services not recommended
   by the Solution Architect.
3. Do not omit essential resources to make the estimate cheaper.
4. Separate one-time initial costs from monthly recurring costs.
5. Use the requested currency.
6. All costs must be non-negative numbers.
7. Minimum values must not exceed maximum values.
8. Unknown annual benefits MUST be null, not zero.
9. Never invent revenue, savings or customer numbers.
10. Do not invent vendor quotations or guaranteed prices.
11. Clearly label estimates as approximate.
12. Keep assumptions and financial risks concise.
13. Return complete valid JSON.
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
