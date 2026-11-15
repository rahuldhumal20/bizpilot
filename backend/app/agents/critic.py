
import re

from app.config import llm
from app.graph.state import BizPilotState


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

    if validation_status == "not_validated":
        return "Conditional Approval"

    if score >= 80 and validation_status == "passed":
        return "Approved"

    if score >= 50:
        return "Conditional Approval"

    return "Rejected"


def review_solution(state: BizPilotState):

    print("Critic Agent is reviewing the proposal...")

    business = str(
        state.get("business_analysis", {})
    )[:900]

    solution = str(
        state.get("solution_architecture", {})
    )[:1100]

    cost = str(
        state.get("cost_analysis", {})
    )[:700]

    financial_validation = str(
        state.get("financial_validation", {})
    )[:700]

    roadmap = str(
        state.get("project_roadmap", {})
    )[:900]

    budget = state.get("budget", "Not provided")

    prompt = f"""
You are an independent Senior Business Proposal Reviewer.

Review the complete BizPilot proposal objectively.

BUSINESS:
{state.get("business_name")}

INDUSTRY:
{state.get("industry")}

BUSINESS SIZE:
{state.get("business_size")}

AVAILABLE BUDGET:
{budget}

BUSINESS ANALYSIS:
{business}

SOLUTION:
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

1. Check whether the solution addresses the actual problem.
2. Identify unsupported assumptions and missing information.
3. Check whether costs respect the customer's budget scope.
4. Consider the Python financial validation result.
5. Do not claim unknown benefits are zero.
6. Do not calculate or claim ROI if benefits are unknown.
7. If financial validation failed, identify the problem.
8. If financial validation is not_validated, state that
   financial estimates are unverified.
9. Do not treat estimated vendor pricing as verified quotations.
10. Identify safety and regulatory requirements where applicable.
11. Never approve a proposal solely because its score is high.

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

Be objective and concise.
Do not invent facts.
"""

    response = llm.invoke(prompt)

    review = response.content

    if isinstance(review, list):
        review = "\n".join(
            item.get("text", "")
            for item in review
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    review = str(review)[:2500]

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
