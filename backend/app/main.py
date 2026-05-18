from fastapi import FastAPI
from app.routes.repo_routes import router as repo_router

app = FastAPI(
    title="AI Codebase Chatbot",
    description="Backend for AI Codebase Chatbot using RAG",
    version="1.0.0"
)

# Register routes
app.include_router(repo_router)

@app.get("/")
def health_check():
    return {"message": "AI Codebase Chatbot Backend Running"}
