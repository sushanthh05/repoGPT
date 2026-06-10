from fastapi import APIRouter, HTTPException, status

from app.models.repository import (
    RepositoryAnalyzeRequest,
    RepositoryListItem,
    RepositoryParseResponse,
    RepositoryResponse,
)
from app.services.github_service import GitHubService
from app.services.parser_service import ParserService

router = APIRouter(prefix="/api/repositories", tags=["repositories"])
github_service = GitHubService()
parser_service = ParserService()


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


@router.get("/health")
def repo_health():
    return {"status": "Repository routing works"}
