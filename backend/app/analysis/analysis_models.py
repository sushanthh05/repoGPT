from pydantic import BaseModel

class RepositoryMetrics(BaseModel):
    total_files: int
    total_documents: int
    total_chunks: int
    languages_used: dict[str, int]

class TechStack(BaseModel):
    frontend: list[str]
    backend: list[str]
    database: list[str]
    other: list[str]

class RepositoryInsights(BaseModel):
    repository_id: str
    summary: str
    tech_stack: TechStack
    entrypoints: list[str]
    important_files: list[str]
    architecture_overview: str
    metrics: RepositoryMetrics
