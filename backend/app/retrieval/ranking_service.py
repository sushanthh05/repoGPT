from app.retrieval.retrieval_models import RetrievedChunk

class RankingService:
    def rank_and_filter(self, chunks: list[RetrievedChunk], top_k: int = 5) -> list[RetrievedChunk]:
        """
        Sort chunks by similarity score (higher is better) and apply duplicate reduction.
        ChromaDB returns distance, so we'll assume the Retriever has already mapped it
        so that a higher score means higher relevance, OR we just assume they are already
        sorted by the retriever/ChromaDB.
        
        For duplicate reduction, we limit the number of chunks from a single file to 2.
        """
        # Sort by similarity_score descending
        sorted_chunks = sorted(chunks, key=lambda c: c.similarity_score, reverse=True)
        
        filtered_chunks = []
        file_counts: dict[str, int] = {}
        
        for chunk in sorted_chunks:
            count = file_counts.get(chunk.file_path, 0)
            if count < 2:
                filtered_chunks.append(chunk)
                file_counts[chunk.file_path] = count + 1
                
            if len(filtered_chunks) >= top_k:
                break
                
        return filtered_chunks
