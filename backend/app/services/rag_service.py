from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.core.config import settings
from app.db.session import engine
from app.constants.db_collections import DBCollections

class RagService:
    def __init__(self, collection_name = DBCollections.GENERAL):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001", 
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=collection_name,
            connection=engine,
            use_jsonb=True,
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=settings.GOOGLE_API_KEY
        )

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    def answer_question(self, question: str):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 1})
        
        template = """
        Bilgi: {context}
        
        Soru: {question}
        
        Sadece yukarıdaki bilgiye dayanarak cevapla.
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(question)
    
    def belge_yukle(self, metin: str, kaynak_adi: str):
        print(f"--- YÜKLEME BAŞLADI: {kaynak_adi} ---")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

        docs = [Document(page_content=metin, metadata={"source": kaynak_adi})]
        
        splits = text_splitter.split_documents(docs)
        self.vector_store.add_documents(splits)
        print(f"Metin {len(splits)} parçaya bölündü.")