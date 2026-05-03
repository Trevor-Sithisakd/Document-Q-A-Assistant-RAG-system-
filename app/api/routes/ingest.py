import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingest_service import IngestService
from app.vectorstore.chroma_store import ChromaStore

router = APIRouter()
ingest_service = IngestService()
store = ChromaStore()


@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    try:
        temp_path = f"data/raw/{file.filename}"

        os.makedirs("data/raw", exist_ok=True)

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        result = ingest_service.ingest_document(temp_path)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected ingest error: {exc}") from exc


@router.get("/documents")
async def list_documents():
    return {"documents": store.list_sources()}


@router.delete("/documents/{source}")
async def delete_document(source: str):
    deleted = store.delete_source(source)
    if deleted == 0:
        raise HTTPException(status_code=404, detail=f"Document '{source}' not found.")
    return {"deleted": source, "chunks_removed": deleted}


@router.delete("/documents")
async def clear_all_documents():
    deleted = store.clear_all()
    return {"chunks_removed": deleted, "status": "cleared"}
