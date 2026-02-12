from app.agents.tech_support.state import TechSupportState
from app.services.rag_service import RagService
from app.constants.db_collections import DBCollections

rag_service = RagService(DBCollections.SUPPORT)

def retrieve(state: TechSupportState):
    print("Tech Support Retrieve Started")
    last_message = state["messages"][-1]
    question = last_message.content

    documents = rag_service.retriever.invoke(question)

    return {"documents": documents}

def generate(state: TechSupportState):
    print("Tech support Agent Generate Started")
    last_message = state["messages"][-1]
    question = last_message.content
    messages = state["messages"]
    documents = state["documents"]

    history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in messages[:-1]])
    context_text = "\n\n".join([doc.page_content for doc in documents])    

    prompt = f"""
    Sen Turkcell Teknik Destek Danışmanısın. 
    Görevin kullanıcıların teknik sorunlarını çözmek
    
    GEÇMİŞ KONUŞMALAR:
    {history_text}

    BİLGİLER:
    {context_text}
    
    SON SORU:
    {question}
    """

    response = rag_service.llm.invoke(prompt)
    return {"messages": [response]}
