from fastapi import APIRouter, HTTPException, status

from app.models.document import ParsedRepositoryDocuments
from app.models.repository import (
    RepositoryAnalyzeRequest,
    RepositoryListItem,
    RepositoryParseResponse,
    RepositoryResponse,
)
from app.models.chunk import ChunkBatch, RepositoryChunkResponse
from app.services.chunking_service import ChunkingService
from app.services.github_service import GitHubService
from app.services.parser_service import ParserService

router = APIRouter(prefix="/api/repositories", tags=["repositories"])
github_service = GitHubService()
parser_service = ParserService()
chunking_service = ChunkingService()


@router.post("/analyze", response_model=RepositoryResponse)
def analyze_repository(payload: RepositoryAnalyzeRequest):
    try:
        repository = github_service.clone_repository(payload.repo_url)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    message = "Repository cloned successfully"
    if repository.status == "exists":
        message = "Repository already exists locally"

    return RepositoryResponse(
        status="success",
        repository_id=repository.repository_id,
        repository_name=repository.repository_name,
        message=message,
    )


@router.get("", response_model=list[RepositoryListItem])
def list_repositories():
    repositories = github_service.list_repositories()
    return [
        RepositoryListItem(repository_id=item.repository_id, repository_name=item.repository_name)
        for item in repositories
    ]


@router.post("/{repository_id}/parse", response_model=RepositoryParseResponse)
def parse_repository(repository_id: str):
    try:
        documents, statistics = parser_service.parse_repository(repository_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    return RepositoryParseResponse(
        status="success",
        repository_id=repository_id,
        documents_created=len(documents),
        message="Repository parsed successfully",
    )


@router.get("/{repository_id}/documents", response_model=ParsedRepositoryDocuments)
def get_parsed_documents(repository_id: str):
    parsed_documents = parser_service.get_parsed_repository_documents(repository_id)
    if parsed_documents is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parsed documents not found")

    return parsed_documents


@router.post("/{repository_id}/chunk", response_model=RepositoryChunkResponse)
def chunk_repository(repository_id: str):
    try:
        chunks, statistics = chunking_service.chunk_repository(repository_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    return RepositoryChunkResponse(
        status="success",
        repository_id=repository_id,
        documents_processed=statistics.documents_processed,
        chunks_generated=len(chunks),
        message="Repository chunked successfully",
        statistics=statistics,
    )


@router.get("/{repository_id}/chunks", response_model=ChunkBatch)
def get_chunk_batch(repository_id: str):
    chunk_batch = chunking_service.get_chunk_batch(repository_id)
    if chunk_batch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chunks not found")

    return chunk_batch


@router.get("/health")
def repo_health():
    return {"status": "Repository routing works"}
