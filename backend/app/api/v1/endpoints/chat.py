from fastapi import APIRouter, Depends
from app.schemas.chat import QuestionRequest, AnswerResponse
from app.services.rag_service import RagService

router = APIRouter()

def get_rag_service():
    return RagService()

@router.post("/", response_model=AnswerResponse)
def chat(
    request: QuestionRequest, 
    service: RagService = Depends(get_rag_service)
):
    answer = service.answer_question(request.question)
    return AnswerResponse(answer=answer)