
import operator
from typing import TypedDict, List, Dict, Any, Annotated


class BizPilotState(TypedDict, total=False):

    # Business information
    business_name: str
    industry: str
    industry_domain: str
    business_description: str
    business_problem: str

    # Financial input
    budget_amount: float
    currency: str
    budget: str
    budget_scope: str
    business_size: str

    # Domain intelligence
    domain_context: str

    # Agent outputs
    business_analysis: Dict[str, Any]
    solution_architecture: Dict[str, Any]
    cost_analysis: Dict[str, Any]
    financial_validation: Dict[str, Any]
    project_roadmap: Dict[str, Any]
    critic_feedback: Dict[str, Any]

    # Workflow information
    quality_status: str
    revision_count: int

    # Agent execution logs
    agent_logs: Annotated[
        List[Dict[str, Any]],
        operator.add
    ]

    # Final compiled report
    final_report: Dict[str, Any]
