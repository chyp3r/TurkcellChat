from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.agents.router import route_question
from app.agents.consultant.state import ConsultantState as AppState 
from app.agents.consultant.workflow import consultant_graph
from app.agents.tech_support.workflow import tech_support_graph

workflow = StateGraph(AppState)

workflow.add_node("tariff_expert", consultant_graph)
workflow.add_node("tech_expert", tech_support_graph)

workflow.set_conditional_entry_point(
    route_question,
    {
        "tariff_expert": "tariff_expert",
        "tech_expert": "tech_expert",
    }
)

workflow.add_edge("tariff_expert", END)
workflow.add_edge("tech_expert", END)

memory = MemorySaver()
master_app = workflow.compile(checkpointer=memory)