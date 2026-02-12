from typing import Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

class RouteQuery(BaseModel):
    target: Literal["tariff_expert", "tech_expert"] = Field(
        ...,
        description="Fiyat, kampanya, paket sorusuysa 'tariff_expert'. Teknik sorun, arıza, kurulum sorusuysa 'tech_expert' seç."
    )

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)

def route_question(state):
    print("Router Node Analysis")
    
    question = state["messages"][-1].content
    
    decision = structured_llm.invoke(
        f"""
        Gelen soruyu analiz et ve yönlendir.
        SORU: {question}
        """
    )
    
    print(f"Target: {decision.target}")
    
    return decision.target