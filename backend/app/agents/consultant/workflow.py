from langgraph.graph import StateGraph, END
from app.agents.consultant.state import ConsultantState
from app.agents.consultant.nodes import retrieve, generate

workflow = StateGraph(ConsultantState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

consultant_graph = workflow.compile()