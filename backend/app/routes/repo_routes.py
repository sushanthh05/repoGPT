from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

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
from app.services.indexing_service import IndexingService
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_store_service import VectorStoreService
from app.database.postgres import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/api/repositories", tags=["repositories"])

def get_github_service(db: Session = Depends(get_db)) -> GitHubService:
    return GitHubService(db)

def get_parser_service(db: Session = Depends(get_db)) -> ParserService:
    return ParserService(db)

def get_chunking_service(db: Session = Depends(get_db)) -> ChunkingService:
    return ChunkingService(db)

def get_indexing_service(db: Session = Depends(get_db)) -> IndexingService:
    embedding_service = EmbeddingService()
    vector_store = VectorStoreService()
    return IndexingService(db, embedding_service, vector_store)


@router.post("/analyze", response_model=RepositoryResponse)
def analyze_repository(payload: RepositoryAnalyzeRequest, github_service: GitHubService = Depends(get_github_service)):
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
def list_repositories(github_service: GitHubService = Depends(get_github_service)):
    repositories = github_service.list_repositories()
    return [
        RepositoryListItem(repository_id=item.repository_id, repository_name=item.repository_name)
        for item in repositories
    ]


@router.post("/{repository_id}/parse", response_model=RepositoryParseResponse)
def parse_repository(repository_id: str, parser_service: ParserService = Depends(get_parser_service)):
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
def get_parsed_documents(repository_id: str, parser_service: ParserService = Depends(get_parser_service)):
    parsed_documents = parser_service.get_parsed_repository_documents(repository_id)
    if parsed_documents is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parsed documents not found")

    return parsed_documents


@router.post("/{repository_id}/chunk", response_model=RepositoryChunkResponse)
def chunk_repository(repository_id: str, chunking_service: ChunkingService = Depends(get_chunking_service)):
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
def get_chunk_batch(repository_id: str, chunking_service: ChunkingService = Depends(get_chunking_service)):
    chunk_batch = chunking_service.get_chunk_batch(repository_id)
    if chunk_batch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chunks not found")

    return chunk_batch


@router.get("/health")
def repo_health():
    return {"status": "Repository routing works"}

class SearchRequest(BaseModel):
    query: str

@router.post("/{repository_id}/index")
def index_repository(repository_id: str, indexing_service: IndexingService = Depends(get_indexing_service)):
    try:
        result = indexing_service.index_repository(repository_id)
        return result
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

@router.post("/{repository_id}/test-search")
def test_search(repository_id: str, request: SearchRequest, indexing_service: IndexingService = Depends(get_indexing_service)):
    try:
        embedding = indexing_service.embedding_service.generate_embedding(request.query)
        results = indexing_service.vector_store.search_chunks(repository_id, embedding)
        
        # Format the results dynamically
        formatted_results = []
        if results and "metadatas" in results and results["metadatas"]:
            for i, metadata in enumerate(results["metadatas"][0]):
                score = results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                file_path = metadata.get("file_path", "Unknown")
                formatted_results.append({
                    "file_path": file_path,
                    "score": score
                })
        
        return formatted_results
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

from app.services.retrieval_service import RetrievalService
from app.retrieval.retrieval_models import SearchRequest as RetrievalSearchRequest, SearchResponse, ContextResponse

def get_retrieval_service() -> RetrievalService:
    return RetrievalService()

@router.post("/{repository_id}/search", response_model=SearchResponse)
def search_repository(repository_id: str, request: RetrievalSearchRequest, retrieval_service: RetrievalService = Depends(get_retrieval_service)):
    try:
        results = retrieval_service.search(repository_id, request.query)
        return SearchResponse(results=results)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

@router.post("/{repository_id}/context", response_model=ContextResponse)
def build_context(repository_id: str, request: RetrievalSearchRequest, retrieval_service: RetrievalService = Depends(get_retrieval_service)):
    try:
        context, sources = retrieval_service.build_context(repository_id, request.query)
        return ContextResponse(context=context, sources=sources)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
from app.services.chat_service import ChatService
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]

def get_chat_service() -> ChatService:
    return ChatService()

@router.post("/{repository_id}/chat", response_model=ChatResponse)
def chat_repository(repository_id: str, request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    try:
        answer, sources = chat_service.chat(repository_id, request.question)
        return ChatResponse(answer=answer, sources=sources)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

from app.services.repository_analysis_service import RepositoryAnalysisService
from app.analysis.analysis_models import RepositoryInsights

def get_repository_analysis_service(db: Session = Depends(get_db)) -> RepositoryAnalysisService:
    return RepositoryAnalysisService(db)

@router.post("/{repository_id}/analyze", response_model=RepositoryInsights)
def analyze_repository_profile(
    repository_id: str,
    analysis_service: RepositoryAnalysisService = Depends(get_repository_analysis_service)
):
    try:
        insights = analysis_service.generate_insights(repository_id)
        return insights
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
