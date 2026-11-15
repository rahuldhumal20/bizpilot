
from app.config import llm
from app.graph.state import BizPilotState


def design_solution(state: BizPilotState):

    print("Solution Architect Agent is working...")

    domain_context = str(
        state.get("domain_context", "")
    )[:1000]

    business_analysis = str(
        state.get("business_analysis", {})
    )[:1400]

    budget_amount = state.get("budget_amount", "Not provided")
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    prompt = f"""
You are a Senior Business Solution Architect.

Design a practical solution for the customer's actual business problem.

BUSINESS INFORMATION:

Business: {state.get("business_name")}
Industry: {state.get("industry")}
Business size: {state.get("business_size")}
Budget: {currency} {budget_amount}
Budget coverage: {budget_scope}

CUSTOMER DESCRIPTION:
{str(state.get("business_description", ""))[:600]}

CUSTOMER PROBLEM:
{str(state.get("business_problem", ""))[:800]}

BUSINESS ANALYSIS:
{business_analysis}

INDUSTRY GUIDANCE:
{domain_context}

IMPORTANT RULES:

1. Solve the actual problem described by the customer.
2. Recommend practical and affordable solutions.
3. Respect the available budget and its coverage.
4. Separate confirmed facts from assumptions.
5. Never invent vendor prices, features, quotations or test results.
6. Mark unverified vendor pricing and features for confirmation.
7. Do not claim a solution is safe, compliant or effective without evidence.
8. Identify important missing information.
9. Avoid unnecessary complexity and expensive technologies.
10. Do not repeat the business analysis.

OUTPUT FORMAT:

## 1. Requirement Understanding
Briefly explain what the customer needs.

## 2. Recommended Solution
Describe the primary solution and how it works.

## 3. Required Resources
List the necessary hardware, software, equipment or services.

## 4. Alternatives
Provide up to two practical alternatives, if relevant.

## 5. Budget Considerations
Explain expected cost categories.
Distinguish initial costs from recurring costs.
Do not invent exact prices or claim the solution fits
the budget without sufficient cost information.

## 6. Implementation Requirements
List the essential setup and implementation steps.

## 7. Risks and Missing Information
Identify important risks, assumptions and information
that must be confirmed before implementation.

INDUSTRY SAFETY:

For water purification:
- Require appropriate laboratory water-quality testing.
- Distinguish microbial and chemical contamination.
- Make treatment recommendations conditional on test results.
- Do not claim drinking-water safety from TDS or basic sensors.
- Require treated-water verification.

FORMATTING:

- Use valid Markdown headings and bullet points.
- Do not use Markdown tables.
- Keep the complete report around 400-500 words.
- Complete every section.
- Never end in the middle of a sentence.
- Return only the solution architecture report.
"""

    response = llm.invoke(prompt)

    solution = response.content

    if isinstance(solution, list):
        solution = "\n".join(
            item.get("text", "")
            for item in solution
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    return {
        "solution_architecture": {
            "solution": str(solution)
        },
        "agent_logs": [
            {
                "agent": "Solution Architect",
                "status": "completed"
            }
        ]
    }
