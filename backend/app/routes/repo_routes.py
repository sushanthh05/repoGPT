from fastapi import APIRouter

router = APIRouter(
    prefix="/repo",
    tags=["repository"]
)

@router.get("/health")
def repo_health():
    return {"status": "Repository routing works"}
