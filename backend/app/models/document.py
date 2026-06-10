from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: str
    repository_id: str
    filename: str
    file_path: str
    language: str
    file_extension: str
    content: str
    size: int
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ParsedRepositoryDocuments(BaseModel):
    repository_id: str
    parsed_at: str
    statistics: dict[str, object]
    documents: list[Document]
