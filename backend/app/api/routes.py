
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.graph.workflow import bizpilot_graph
from app.domain.industry_rules import build_domain_context


router = APIRouter()


IndustryDomain = Literal[
    "retail",
    "beauty",
    "food",
    "healthcare",
    "education",
    "manufacturing",
    "water",
    "agriculture",
    "hospitality",
    "logistics",
    "professional",
    "other"
]


class BusinessRequest(BaseModel):
    business_name: str = Field(min_length=2, max_length=120)

    industry: str = Field(min_length=2, max_length=100)

    industry_domain: IndustryDomain

    business_description: str = Field(
        min_length=10,
        max_length=2000
    )

    business_problem: str = Field(
        min_length=10,
        max_length=2000
    )

    budget_amount: float = Field(gt=0, le=1_000_000_000)

    currency: Literal["INR", "USD", "EUR", "GBP"] = "INR"

    budget_scope: Literal[
    "initial_only",
    "first_year_total"
] = "initial_only"

    business_size: Literal[
        "Startup",
        "Small Business",
        "Medium Business",
        "Enterprise"
    ]


@router.post("/analyze")
async def analyze_business_route(data: BusinessRequest):

    try:
        print("Starting BizPilot business analysis...")

        initial_state = {
            **data.model_dump(),
            "budget": (
                f"{data.currency} {data.budget_amount:,.2f}"
            ),
            "domain_context": build_domain_context(
                data.industry_domain
            ),
            "revision_count": 0,
            "agent_logs": []
        }

        result = await bizpilot_graph.ainvoke(initial_state)

        return {
            "success": True,
            "message": "Business analysis completed successfully",
            "report": result.get("final_report", {}),
            "agent_logs": result.get("agent_logs", [])
        }

    except Exception as e:
        print(f"BizPilot Error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Business analysis failed. Check backend logs."
        )
