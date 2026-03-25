import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingest_service import IngestService

router = APIRouter()
ingest_service = IngestService()


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
