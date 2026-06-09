from fastapi import APIRouter, HTTPException, status

from app.models.repository import (
    RepositoryAnalyzeRequest,
    RepositoryListItem,
    RepositoryResponse,
)
from app.services.github_service import GitHubService

router = APIRouter(prefix="/api/repositories", tags=["repositories"])
github_service = GitHubService()


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


@router.get("/health")
def repo_health():
    return {"status": "Repository routing works"}
