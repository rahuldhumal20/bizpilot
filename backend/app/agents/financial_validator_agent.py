
from app.graph.state import BizPilotState
from app.validators.financial_validator import validate_financial_data


def validate_financials(state: BizPilotState):

    print("Financial Validator is checking estimates...")

    cost_analysis = state.get("cost_analysis", {})
    financial_data = cost_analysis.get("financial_data", {})

    budget_amount = state.get("budget_amount", 0)
    currency = state.get("currency", "INR")
    budget_scope = state.get("budget_scope", "initial_only")

    if not financial_data:

        result = {
            "validation_status": "not_validated",
            "issues": [
                "Cost Analyst did not provide structured financial data."
            ],
            "warnings": [],
            "calculations": {}
        }

    else:

        result = validate_financial_data(
            budget_amount=budget_amount,
            currency=currency,
            financial_data=financial_data,
            budget_scope=budget_scope
        )

    print(
        "Financial validation status:",
        result["validation_status"]
    )

    return {
        "financial_validation": result,
        "agent_logs": [
            {
                "agent": "Financial Validator",
                "status": result["validation_status"]
            }
        ]
    }
