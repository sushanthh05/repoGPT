from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_store_service import VectorStoreService
from app.retrieval.ranking_service import RankingService
from app.retrieval.retrieval_models import RetrievedChunk

class Retriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreService,
        ranking_service: RankingService
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.ranking_service = ranking_service

    def retrieve(self, query: str, repository_id: str, top_k: int = 5) -> list[RetrievedChunk]:
        """
        Orchestrates the retrieval process:
        1. Embed the query.
        2. Search the vector store.
        3. Map results to RetrievedChunk models.
        4. Pass through RankingService for duplicate reduction.
        """
        # 1. Query Embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # 2. Vector Search (we request a bit more than top_k so RankingService can filter)
        search_k = top_k * 3
        try:
            raw_results = self.vector_store.search_chunks(
                repository_id=repository_id,
                query_embedding=query_embedding,
                n_results=search_k
            )
        except ValueError:
            # Collection might not exist
            return []
            
        # ChromaDB results are lists of lists for multiple queries. We only have 1 query.
        if not raw_results or not raw_results.get("ids") or not raw_results["ids"][0]:
            return []
            
        ids = raw_results["ids"][0]
        distances = raw_results.get("distances", [[]])[0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        documents = raw_results.get("documents", [[]])[0]
        
        # 3. Map to RetrievedChunk
        chunks = []
        for i in range(len(ids)):
            # ChromaDB returns distance. For our simple RankingService, we want similarity_score
            # distance is typically L2 or cosine distance. We can just negate it so higher is better,
            # or do 1 - distance if it's cosine. We'll use 1 / (1 + distance) for a generic score.
            dist = distances[i] if i < len(distances) else 0.0
            similarity_score = 1.0 / (1.0 + dist)
            
            meta = metadatas[i] if i < len(metadatas) and metadatas[i] else {}
            
            # chunk_id might be stored directly in id or in metadata
            chunk_id = str(meta.get("chunk_id", ids[i]))
            file_path = str(meta.get("file_path", meta.get("document_id", "unknown_file")))
            language = str(meta.get("language", "unknown"))
            chunk_index = meta.get("chunk_index", 0)
            
            chunk = RetrievedChunk(
                chunk_id=chunk_id,
                repository_id=repository_id,
                file_path=file_path,
                content=str(documents[i]) if i < len(documents) and documents[i] is not None else "",
                language=language,
                similarity_score=similarity_score,
                chunk_index=int(chunk_index) if chunk_index is not None else 0
            )
            chunks.append(chunk)
            
        # 4. Rank and Filter
        return self.ranking_service.rank_and_filter(chunks, top_k=top_k)
