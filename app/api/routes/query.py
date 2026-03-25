from fastapi import APIRouter, HTTPException
from app.api.schemas.query import QueryRequest
from app.services.query_service import QueryService

router = APIRouter()
query_service = QueryService()


@router.post("/query")
def query_documents(request: QueryRequest):
    try:
        return query_service.answer_question(
            question=request.question,
            top_k=request.top_k
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected query error: {exc}") from exc
