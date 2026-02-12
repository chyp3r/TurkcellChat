from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from app.agents.graph import master_app 

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    thread_id: str = Field(default="session_1")

@router.post("/master-agent") 
async def agent_chat(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        inputs = {"messages": [HumanMessage(content=request.question)]}
        
        result = master_app.invoke(inputs, config=config)
        
        last_message = result["messages"][-1]
        return {"answer": last_message.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))