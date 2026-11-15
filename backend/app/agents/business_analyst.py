
from app.config import llm
from app.graph.state import BizPilotState


def analyze_business(state: BizPilotState):

    print("Business Analyst Agent is working...")

    prompt = f"""
You are a professional Business Analyst helping small and medium businesses.

Analyze the following business information:

Business Name: {state.get("business_name", "Not provided")}
Industry: {state.get("industry", "Not provided")}
Description: {state.get("business_description", "Not provided")}
Problem: {state.get("business_problem", "Not provided")}
Budget: {state.get("budget_amount", "Not provided")}
Currency: {state.get("currency", "INR")}
Business Size: {state.get("business_size", "Not provided")}

Prepare a clear and practical business analysis for the owner.

Use exactly these five sections:

## 1. Business Overview
Summarize the business, industry, size, current operations,
budget and main business objective.

## 2. Operational Problems
Identify the main operational problems.
For each problem, explain its symptoms and business impact.

## 3. Root Causes
Identify the likely root causes behind the problems.
Clearly distinguish confirmed facts from assumptions.

## 4. Customer Experience Issues
Explain how the operational problems affect customers,
including service quality, convenience, trust and satisfaction.
Only include relevant issues.

## 5. Automation Opportunities
Suggest 3 to 5 practical, affordable automation opportunities.
For each opportunity, include:
- Automation area
- Suggested solution
- Expected business benefit

IMPORTANT RULES:

1. Keep the complete report concise, approximately 450-600 words.
2. Complete all five sections. Never stop midway through a section.
3. Do not invent business facts, prices, software capabilities or statistics.
4. Clearly label assumptions and missing information.
5. Do not treat inferred problems as confirmed facts.
6. Do not recommend expensive or unnecessarily complex solutions.
7. Consider the available budget when suggesting opportunities.
8. Use valid GitHub Flavored Markdown.
9. Prefer headings and bullet points over tables.
10. Do not use HTML tags such as <br>.
11. Do not repeat the same information in multiple sections.
12. Finish with a short list of important missing information
    that the owner should confirm.

Return only the business analysis report.
"""

    response = llm.invoke(prompt)

    analysis = response.content

    return {
        "business_analysis": {
            "analysis": analysis
        },
        "agent_logs": [
            {
                "agent": "Business Analyst",
                "status": "completed"
            }
        ]
    }
