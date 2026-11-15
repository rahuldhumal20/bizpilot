
from langgraph.graph import StateGraph, START, END

from app.graph.state import BizPilotState

from app.agents.business_analyst import analyze_business
from app.agents.solution_architect import design_solution
from app.agents.cost_analyst import analyze_cost
from app.agents.financial_validator_agent import validate_financials
from app.agents.project_planner import create_roadmap
from app.agents.critic import review_solution


def compile_report(state: BizPilotState):
    print("Compiling final BizPilot report...")

    return {
        "final_report": {
            "business_name": state.get("business_name"),
            "industry": state.get("industry"),
            "business_analysis": state.get("business_analysis"),
            "solution": state.get("solution_architecture"),
            "cost_analysis": state.get("cost_analysis"),
            "financial_validation": state.get(
                "financial_validation"
            ),
            "project_roadmap": state.get("project_roadmap"),
            "critic_review": state.get("critic_feedback"),
            "quality_status": state.get("quality_status")
        }
    }


def build_workflow():
    workflow = StateGraph(BizPilotState)

    workflow.add_node("business_analyst", analyze_business)
    workflow.add_node("solution_architect", design_solution)
    workflow.add_node("cost_analyst", analyze_cost)
    workflow.add_node("financial_validator", validate_financials)
    workflow.add_node("project_planner", create_roadmap)
    workflow.add_node("critic", review_solution)
    workflow.add_node("compile_report", compile_report)

    workflow.add_edge(START, "business_analyst")
    workflow.add_edge("business_analyst", "solution_architect")
    workflow.add_edge("solution_architect", "cost_analyst")

    # Validate financial estimates immediately after cost analysis.
    workflow.add_edge("cost_analyst", "financial_validator")

    workflow.add_edge("financial_validator", "project_planner")
    workflow.add_edge("project_planner", "critic")
    workflow.add_edge("critic", "compile_report")
    workflow.add_edge("compile_report", END)

    return workflow.compile()


bizpilot_graph = build_workflow()

print("BizPilot LangGraph workflow initialized successfully!")
