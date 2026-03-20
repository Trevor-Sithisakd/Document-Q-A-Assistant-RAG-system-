from fastapi import APIRouter
from app.api.schemas.query import QueryRequest
from app.services.query_service import QueryService

router = APIRouter()
query_service = QueryService()


@router.post("/query")
def query_documents(request: QueryRequest):
    return query_service.answer_question(
        question=request.question,
        top_k=request.top_k
    )