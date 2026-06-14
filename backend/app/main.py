from fastapi import FastAPI

from app.routes.repo_routes import router as repo_router

app = FastAPI(
    title="RepoGPT Backend",
    description="Backend for repository acquisition and management",
    version="2.0.0",
)

from app.database.postgres import engine, Base
from app.database.models import models

Base.metadata.create_all(bind=engine)

app.include_router(repo_router)


@app.get("/")
def health_check():
    return {"message": "RepoGPT Backend Running"}
