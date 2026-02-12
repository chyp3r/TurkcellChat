from langgraph.graph import StateGraph, END
from app.agents.tech_support.state import TechSupportState
from app.agents.tech_support.nodes import retrieve, generate


workflow = StateGraph(TechSupportState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve","generate")
workflow.add_edge("generate",END)

tech_support_graph = workflow.compile()