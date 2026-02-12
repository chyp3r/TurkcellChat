from typing import List, TypedDict, Annotated
from langchain_core.documents import Document
from langgraph.graph.message import add_messages

class ConsultantState(TypedDict):
    question: str                   
    documents: List[Document]       
    generation: str                 
    messages: Annotated[list, add_messages]
    