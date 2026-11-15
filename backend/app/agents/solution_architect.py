
from app.config import llm
from app.graph.state import BizPilotState


def get_response_text(content):
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        return "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        ).strip()

    return str(content)


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

Your responsibility is to design a practical solution for the
customer's actual business problem.

BUSINESS INFORMATION:

Business: {state.get("business_name")}
Industry: {state.get("industry")}
Business size: {state.get("business_size")}
Available budget: {currency} {budget_amount}
Budget coverage: {budget_scope}

CUSTOMER DESCRIPTION:
{str(state.get("business_description", ""))[:600]}

CUSTOMER PROBLEM:
{str(state.get("business_problem", ""))[:800]}

BUSINESS ANALYSIS:
{business_analysis}

INDUSTRY CONTEXT:
{domain_context}

CORE RULES:

1. Solve the actual problem described by the customer.
2. Adapt the solution to the business type, size and operating
   conditions. Do not assume every business needs software.
3. Prefer practical, affordable and maintainable solutions.
4. Respect the available budget and its coverage.
5. Separate confirmed facts from assumptions.
6. Do not invent business information, vendor quotations,
   product features, statistics or test results.
7. Do not recommend unnecessary technology or complexity.
8. Identify important missing information.
9. Consider relevant safety, legal and regulatory requirements
   for the particular industry. State when expert verification
   or testing is required. Never claim compliance without evidence.
10. Do not repeat the business analysis.

RESOURCE CONSISTENCY:

- List only resources necessary for the recommended solution.
- Mark each resource as REQUIRED or OPTIONAL.
- Explain briefly why each resource is needed.
- Do not provide specific monetary estimates.
- Do not introduce resources merely as examples and present them
  as requirements.
- The Cost Analyst will estimate the costs of these resources.
- Alternatives must remain separate from the primary solution.

OUTPUT FORMAT:

## 1. Requirement Understanding
Explain the customer's actual needs and main problem.

## 2. Recommended Solution
Describe the recommended solution and how it addresses the problem.
Explain its basic working process.

## 3. Required Resources
List required and optional hardware, software, equipment,
people or services, as relevant.

## 4. Alternatives
Provide up to two practical alternatives if they genuinely
offer value. Clearly distinguish alternatives from the
recommended solution.

## 5. Budget Considerations
Explain the types of initial and recurring costs involved.
Do not provide monetary estimates.
Do not claim that the solution fits the budget without
financial validation.

## 6. Implementation Requirements
List the essential setup, preparation and implementation steps.

## 7. Risks and Missing Information
Identify assumptions, operational risks, industry-specific
concerns and information that must be confirmed.

FORMATTING:

- Use valid Markdown headings and bullet points.
- Do not use Markdown tables.
- Keep the report concise, around 350-450 words.
- Complete every section.
- Do not repeat information unnecessarily.
- Never end in the middle of a sentence.
- Return only the solution architecture report.
"""

    response = llm.invoke(prompt)
    solution = get_response_text(response.content)

    return {
        "solution_architecture": {
            "solution": solution
        },
        "agent_logs": [
            {
                "agent": "Solution Architect",
                "status": "completed"
            }
        ]
    }
