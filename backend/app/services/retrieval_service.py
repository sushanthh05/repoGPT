from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_store_service import VectorStoreService
from app.retrieval.ranking_service import RankingService
from app.retrieval.retrieval_models import RetrievedChunk

class RetrievalService:
    def __init__(self):
        # Initialize dependencies
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        self.ranking_service = RankingService()
        self.retriever = Retriever(
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
            ranking_service=self.ranking_service
        )
        self.context_builder = ContextBuilder()

    def search(self, repository_id: str, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """
        Executes a semantic search and returns a list of RetrievedChunk models.
        """
        return self.retriever.retrieve(query=query, repository_id=repository_id, top_k=top_k)

    def build_context(self, repository_id: str, query: str, top_k: int = 5) -> tuple[str, list[dict]]:
        """
        Executes a search and formats the results into a prompt-ready context string.
        Returns (context_string, sources_list).
        """
        chunks = self.search(repository_id, query, top_k=top_k)
        return self.context_builder.build_context(chunks)
