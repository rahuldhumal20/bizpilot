
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


def create_roadmap(state: BizPilotState):

    print("Project Planner Agent is working...")

    business_analysis = str(
        state.get("business_analysis", {})
    )[:900]

    solution_data = state.get("solution_architecture", {})

    solution = str(
        solution_data.get("solution", solution_data)
        if isinstance(solution_data, dict)
        else solution_data
    )[:2200]

    cost_data = state.get("cost_analysis", {})

    cost = str(
        cost_data.get("financial_analysis", cost_data)
        if isinstance(cost_data, dict)
        else cost_data
    )[:1000]

    financial_validation = str(
        state.get("financial_validation", {})
    )[:700]

    budget_amount = state.get("budget_amount", "Not provided")
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    prompt = f"""
You are an experienced Business Project Manager.

Create a realistic implementation roadmap for the customer's
business using the information supplied below.

BUSINESS:
{state.get("business_name")}

INDUSTRY:
{state.get("industry")}

BUSINESS SIZE:
{state.get("business_size")}

CUSTOMER PROBLEM:
{str(state.get("business_problem", ""))[:600]}

AVAILABLE BUDGET:
{currency} {budget_amount}

BUDGET COVERAGE:
{budget_scope}

BUSINESS ANALYSIS:
{business_analysis}

SOLUTION ARCHITECTURE:
{solution}

COST ANALYSIS:
{cost}

FINANCIAL VALIDATION:
{financial_validation}

CORE RULES:

1. Plan only the primary solution proposed by the Solution Architect.
2. Use the REQUIRED resources identified by the architect.
3. Do not introduce additional software, hardware or features.
4. Do not treat optional resources or alternatives as mandatory.
5. Use the Cost Analyst's estimates. Do not create new prices.
6. Respect the customer's budget and budget coverage.
7. Distinguish one-time costs from recurring costs.
8. Do not invent customer counts, staff availability,
   infrastructure, savings or financial benefits.
9. Mark unconfirmed requirements as dependencies.
10. Use realistic indicative timelines, not guaranteed dates.
11. Include customer approval and staff training where relevant.
12. Include appropriate testing before rollout.
13. Do not claim legal, safety or regulatory compliance
    without appropriate verification.
14. Do not repeat the business analysis or solution description.

CREATE EXACTLY THREE PHASES:

## Phase 1 – MVP / Initial Setup
## Phase 2 – Core Implementation
## Phase 3 – Testing and Rollout

FOR EACH PHASE INCLUDE:

- Objective
- Priority
- Estimated duration
- Key tasks
- Dependencies
- Deliverables

ALSO INCLUDE:

## Key Dependencies
## Testing Strategy
## Training and Handover
## Success Metrics
## Risks and Contingency Plans
## Information Required Before Implementation

FORMATTING:

- Use valid Markdown headings and bullet points.
- Do not use Markdown tables.
- Keep the roadmap concise, around 350-450 words.
- Complete all three phases and all additional sections.
- Clearly label indicative timelines and assumptions.
- Never end in the middle of a sentence or task.
- Return only the implementation roadmap.
"""

    response = llm.invoke(prompt)
    roadmap = get_response_text(response.content)

    return {
        "project_roadmap": {
            "roadmap": roadmap
        },
        "agent_logs": [
            {
                "agent": "Project Planner",
                "status": "completed"
            }
        ]
    }
