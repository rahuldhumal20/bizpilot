
import re

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


def extract_score(review: str):
    """Extract the quality score from the critic response."""

    patterns = [
        r"Quality Score\s*[:\-]?\s*(\d{1,3})",
        r"Overall Score\s*[:\-]?\s*(\d{1,3})",
        r"Score\s*[:\-]?\s*(\d{1,3})\s*/\s*100"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            review,
            re.IGNORECASE
        )

        if match:
            score = int(match.group(1))

            if 0 <= score <= 100:
                return score

    return None


def determine_status(score, validation_status):

    if score is None:
        return "Manual Review Required"

    if validation_status == "failed":
        return "Rejected"

    if score < 50:
        return "Rejected"

    if validation_status != "passed":
        return "Conditional Approval"

    if score >= 80:
        return "Approved"

    return "Conditional Approval"


def review_solution(state: BizPilotState):

    print("Critic Agent is reviewing the proposal...")

    business = str(
        state.get("business_analysis", {})
    )[:1100]

    solution_data = state.get("solution_architecture", {})

    solution = str(
        solution_data.get("solution", solution_data)
        if isinstance(solution_data, dict)
        else solution_data
    )[:2000]

    cost_data = state.get("cost_analysis", {})

    cost = str(
        cost_data.get("financial_analysis", cost_data)
        if isinstance(cost_data, dict)
        else cost_data
    )[:1100]

    financial_validation = str(
        state.get("financial_validation", {})
    )[:800]

    roadmap_data = state.get("project_roadmap", {})

    roadmap = str(
        roadmap_data.get("roadmap", roadmap_data)
        if isinstance(roadmap_data, dict)
        else roadmap_data
    )[:1600]

    budget_amount = state.get("budget_amount", "Not provided")
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    prompt = f"""
You are an independent Senior Business Proposal Reviewer.

Evaluate the BizPilot proposal objectively and identify
whether it is practical, financially reasonable and suitable
for the customer's actual business problem.

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

BUSINESS ANALYSIS:
{business}

SOLUTION ARCHITECTURE:
{solution}

COST ANALYSIS:
{cost}

PYTHON FINANCIAL VALIDATION:
{financial_validation}

IMPLEMENTATION ROADMAP:
{roadmap}

EVALUATION FRAMEWORK:

Score each category from 0 to 100.

1. Problem Understanding: 20%
2. Solution Suitability: 25%
3. Financial Feasibility: 20%
4. Implementation Feasibility: 20%
5. Risk and Compliance Management: 15%

Calculate the weighted overall score.

REVIEW RULES:

1. Check whether the solution addresses the customer's actual problem.
2. Check whether the recommended resources are consistent
   across the solution, cost analysis and roadmap.
3. Check whether the cost estimate covers the required resources.
4. Check whether the budget scope has been respected.
5. Consider the Python financial validation result.
6. Identify unsupported assumptions and missing information.
7. Do not treat estimates as verified vendor quotations.
8. Do not treat unknown annual benefits as zero.
9. Do not calculate or claim ROI when benefits are unknown.
10. If financial validation failed, explain the problem.
11. If financial validation is not validated or needs review,
    state that financial estimates require confirmation.
12. Identify relevant safety and regulatory concerns.
13. Do not approve a proposal solely because its score is high.
14. Do not invent facts or requirements.
15. Keep the review concise and complete.

OUTPUT FORMAT:

1. Quality Score: XX/100

2. Category Scores:
   - Problem Understanding:
   - Solution Suitability:
   - Financial Feasibility:
   - Implementation Feasibility:
   - Risk and Compliance:

3. Approval Recommendation:
   - Approved
   - Conditional Approval
   - Rejected

4. Business Strengths

5. Financial Concerns

6. Technical Concerns

7. Missing Information

8. Critical Risks

9. Required Improvements

10. Final Verdict

Use the weighted evaluation framework consistently.
Return a complete review and do not stop mid-sentence.
"""

    response = llm.invoke(prompt)
    review = get_response_text(response.content)

    validation = state.get(
        "financial_validation", {}
    )

    validation_status = validation.get(
        "validation_status",
        "not_validated"
    )

    score = extract_score(review)

    approval_status = determine_status(
        score,
        validation_status
    )

    print("Critic quality score:", score)
    print("Critic approval:", approval_status)

    return {
        "critic_feedback": {
            "review": review,
            "quality_score": score,
            "approval_status": approval_status,
            "financial_validation_status": validation_status
        },
        "quality_status": approval_status,
        "agent_logs": [
            {
                "agent": "Critic Agent",
                "status": "completed"
            }
        ]
    }
