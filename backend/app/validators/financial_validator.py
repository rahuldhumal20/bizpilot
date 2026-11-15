
from typing import Any
import math


REQUIRED_FIELDS = [
    "currency",
    "initial_cost_min",
    "initial_cost_max",
    "monthly_opex_min",
    "monthly_opex_max",
    "annual_gross_benefit_min",
    "annual_gross_benefit_max",
]


def is_valid_number(value: Any) -> bool:
    """Check whether a value is a finite, non-negative number."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value >= 0
    )


def validate_financial_data(
    budget_amount: float,
    currency: str,
    financial_data: dict,
    budget_scope: str = "initial_only"
) -> dict:

    issues = []
    warnings = []
    calculations = {}

    if not isinstance(financial_data, dict):
        return {
            "validation_status": "not_validated",
            "issues": ["Financial data is missing or invalid."],
            "warnings": [],
            "calculations": {}
        }

    # 1. Check required fields
    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in financial_data
    ]

    if missing_fields:
        return {
            "validation_status": "not_validated",
            "issues": [
                "Missing fields: " + ", ".join(missing_fields)
            ],
            "warnings": [],
            "calculations": {}
        }

    # 2. Check currency
    if financial_data["currency"] != currency:
        issues.append(
            f"Currency mismatch: expected {currency}, "
            f"received {financial_data['currency']}."
        )

    # 3. Validate costs
    cost_fields = [
        "initial_cost_min",
        "initial_cost_max",
        "monthly_opex_min",
        "monthly_opex_max",
    ]

    for field in cost_fields:
        if not is_valid_number(financial_data[field]):
            issues.append(
                f"{field} must be a finite, non-negative number."
            )

    # 4. Validate benefits
    benefit_fields = [
        "annual_gross_benefit_min",
        "annual_gross_benefit_max"
    ]

    benefit_values = [
        financial_data[field] for field in benefit_fields
    ]

    benefit_known = all(
        is_valid_number(value) for value in benefit_values
    )

    benefit_unknown = all(
        value is None for value in benefit_values
    )

    if not benefit_known and not benefit_unknown:
        issues.append(
            "Annual benefit must contain two valid numbers "
            "or both values must be null."
        )

    if issues:
        return {
            "validation_status": "failed",
            "issues": issues,
            "warnings": [],
            "calculations": {}
        }

    # 5. Validate ranges
    range_pairs = [
        ("initial_cost_min", "initial_cost_max"),
        ("monthly_opex_min", "monthly_opex_max"),
    ]

    if benefit_known:
        range_pairs.append(
            ("annual_gross_benefit_min",
             "annual_gross_benefit_max")
        )

    for minimum, maximum in range_pairs:
        if financial_data[minimum] > financial_data[maximum]:
            issues.append(
                f"{minimum} cannot exceed {maximum}."
            )

    if issues:
        return {
            "validation_status": "failed",
            "issues": issues,
            "warnings": [],
            "calculations": {}
        }

    # 6. Calculate cost estimates
    initial_min = financial_data["initial_cost_min"]
    initial_max = financial_data["initial_cost_max"]

    monthly_min = financial_data["monthly_opex_min"]
    monthly_max = financial_data["monthly_opex_max"]

    initial_mid = (initial_min + initial_max) / 2
    monthly_mid = (monthly_min + monthly_max) / 2

    # 7. Check budget scope
    if budget_scope == "initial_only":
        budget_min = initial_min
        budget_max = initial_max

    elif budget_scope == "first_year_total":
        budget_min = initial_min + (monthly_min * 12)
        budget_max = initial_max + (monthly_max * 12)

    else:
        return {
            "validation_status": "failed",
            "issues": ["Invalid budget scope."],
            "warnings": [],
            "calculations": {}
        }

    if budget_max > budget_amount:
        warnings.append(
            "The maximum estimated cost exceeds the available budget."
        )

    calculations = {
        "currency": currency,
        "budget_scope": budget_scope,
        "estimated_initial_cost_mid": round(initial_mid, 2),
        "estimated_monthly_opex_mid": round(monthly_mid, 2),
        "estimated_budget_requirement_min": round(budget_min, 2),
        "estimated_budget_requirement_max": round(budget_max, 2),
        "available_budget": budget_amount,
    }

    # 8. Calculate ROI only when benefits are known
    if benefit_known:

        benefit_min = financial_data["annual_gross_benefit_min"]
        benefit_max = financial_data["annual_gross_benefit_max"]

        benefit_mid = (benefit_min + benefit_max) / 2

        annual_opex = monthly_mid * 12

        annual_net_benefit = benefit_mid - annual_opex

        if initial_mid > 0:
            roi = (
                annual_net_benefit / initial_mid
            ) * 100
        else:
            roi = None

        monthly_net_benefit = (
            benefit_mid / 12
        ) - monthly_mid

        if monthly_net_benefit > 0 and initial_mid > 0:
            break_even = initial_mid / monthly_net_benefit
        else:
            break_even = None

        calculations.update({
            "estimated_annual_gross_benefit_mid": round(
                benefit_mid, 2
            ),
            "estimated_annual_net_benefit": round(
                annual_net_benefit, 2
            ),
            "calculated_first_year_roi_percent": (
                round(roi, 2) if roi is not None else None
            ),
            "calculated_break_even_months": (
                round(break_even, 2)
                if break_even is not None else None
            )
        })

        if roi is None:
            warnings.append(
                "ROI cannot be calculated because initial cost is zero."
            )

        if break_even is None:
            warnings.append(
                "Break-even cannot be estimated from the "
                "available financial values."
            )

    else:
        warnings.append(
            "Annual business benefits are unknown. "
            "ROI and break-even have not been calculated."
        )

    status = "passed" if not warnings else "needs_review"

    return {
        "validation_status": status,
        "issues": [],
        "warnings": warnings,
        "calculations": calculations
    }
