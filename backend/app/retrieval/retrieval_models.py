from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    chunk_id: str
    repository_id: str
    file_path: str
    content: str
    language: str
    similarity_score: float
    chunk_index: int

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list[RetrievedChunk]

class ContextResponse(BaseModel):
    context: str
    sources: list[dict]
