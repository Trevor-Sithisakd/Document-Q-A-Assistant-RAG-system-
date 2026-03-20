from pydantic import BaseModel


class IngestResponse(BaseModel):
    document_name: str
    pages: int
    chunks_created: int
    status: str