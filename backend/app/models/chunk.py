from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    repository_id: str
    chunk_index: int
    content: str
    source_file: str
    language: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, object]


class ChunkingStatistics(BaseModel):
    documents_processed: int
    chunks_generated: int
    average_chunk_size: int
    largest_file_chunks: int
    chunk_size: int
    chunk_overlap: int


class ChunkBatch(BaseModel):
    repository_id: str
    chunked_at: str
    statistics: ChunkingStatistics
    chunks: list[Chunk]


class RepositoryChunkResponse(BaseModel):
    status: str
    repository_id: str
    documents_processed: int
    chunks_generated: int
    message: str
    statistics: ChunkingStatistics