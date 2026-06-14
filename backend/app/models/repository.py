from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class RepositoryAnalyzeRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL")

    @field_validator("repo_url")
    @classmethod
    def normalize_repo_url(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("repo_url is required")
        return normalized


class RepositoryMetadata(BaseModel):
    repository_id: str
    repository_name: str
    repository_url: str
    local_path: str
    created_at: datetime | str
    updated_at: datetime | str | None = None
    status: Literal["cloned", "exists", "failed"]

    @classmethod
    def create(
        cls,
        repository_id: str,
        repository_name: str,
        repository_url: str,
        local_path: str,
        status: Literal["cloned", "exists", "failed"] = "cloned",
    ) -> "RepositoryMetadata":
        return cls(
            repository_id=repository_id,
            repository_name=repository_name,
            repository_url=repository_url,
            local_path=local_path,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            status=status,
        )


class RepositoryResponse(BaseModel):
    status: str
    repository_id: str
    repository_name: str
    message: str


class RepositoryListItem(BaseModel):
    repository_id: str
    repository_name: str


class RepositoryParseResponse(BaseModel):
    status: str
    repository_id: str
    documents_created: int
    message: str


class RepositoryParseStatistics(BaseModel):
    total_files: int
    parsed_files: int
    ignored_files: int
    ignored_directories: int
    languages: list[str]