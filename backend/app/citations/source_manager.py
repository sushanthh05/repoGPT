from pydantic import BaseModel, Field

class SourceEvidence(BaseModel):
    file_path: str = Field(..., description="The path of the source file")
    chunk_id: str = Field(..., description="The chunk ID in the vector store")
    similarity_score: float = Field(..., description="Relevance score (higher is better)")
    language: str = Field(default="unknown", description="Programming language of the file")
    snippet: str = Field(..., description="A brief preview snippet of the chunk's content")
