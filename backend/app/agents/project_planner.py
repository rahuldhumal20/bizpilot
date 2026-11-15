
from app.config import llm
from app.graph.state import BizPilotState


def create_roadmap(state: BizPilotState):

    print("Project Planner Agent is working...")

    business_analysis = str(
        state.get("business_analysis", {})
    )[:700]

    solution_data = state.get("solution_architecture", {})
    solution = str(
        solution_data.get("solution", solution_data)
        if isinstance(solution_data, dict)
        else solution_data
    )[:1400]

    cost_data = state.get("cost_analysis", {})
    cost = str(
        cost_data.get("financial_analysis", cost_data)
        if isinstance(cost_data, dict)
        else cost_data
    )[:700]

    financial_validation = str(
        state.get("financial_validation", {})
    )[:500]

    budget_amount = state.get("budget_amount", "Not provided")
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    prompt = f"""
You are an experienced Business Project Manager.

Create a practical implementation roadmap using ONLY
the proposed solution provided below.

BUSINESS:
{state.get("business_name")}

INDUSTRY:
{state.get("industry")}

BUSINESS SIZE:
{state.get("business_size")}

CUSTOMER PROBLEM:
{str(state.get("business_problem", ""))[:500]}

AVAILABLE BUDGET:
{currency} {budget_amount}

BUDGET COVERAGE:
{budget_scope}

BUSINESS ANALYSIS:
{business_analysis}

PROPOSED SOLUTION:
{solution}

COST ANALYSIS:
{cost}

FINANCIAL VALIDATION:
{financial_validation}

IMPORTANT RULES:

1. Plan only the solution proposed by the Solution Architect.
2. Do not introduce additional software, hardware or features.
3. Do not invent customer counts, staff availability or infrastructure.
4. Respect the budget and its coverage.
5. Distinguish one-time costs from recurring costs.
6. Do not invent vendor prices, savings or financial benefits.
7. Mark unconfirmed requirements as dependencies.
8. Use realistic indicative timelines.
9. Include customer approval and staff training where relevant.
10. Include appropriate testing before rollout.
11. Do not claim legal, safety or regulatory compliance without verification.
12. Do not repeat the business analysis or solution architecture.

CREATE EXACTLY THREE PHASES:

## Phase 1 – MVP / Initial Setup
## Phase 2 – Core Implementation
## Phase 3 – Testing and Rollout

For EACH phase include:

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

FORMATTING RULES:

1. Use valid GitHub Flavored Markdown.
2. Prefer headings and bullet points.
3. Do not use Markdown tables.
4. Keep the complete roadmap around 450-550 words.
5. Complete all three phases.
6. Never stop in the middle of a sentence or task.
7. Clearly label indicative timelines and assumptions.
8. Return only the implementation roadmap.
"""

    response = llm.invoke(prompt)

    roadmap = response.content

    if isinstance(roadmap, list):
        roadmap = "\n".join(
            item.get("text", "")
            for item in roadmap
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    return {
        "project_roadmap": {
            "roadmap": str(roadmap)
        },
        "agent_logs": [
            {
                "agent": "Project Planner",
                "status": "completed"
            }
        ]
    }
