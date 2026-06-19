from app.retrieval.retrieval_models import RetrievedChunk
from app.citations.source_manager import SourceEvidence
from collections import defaultdict

class CitationBuilder:
    def rank_and_deduplicate(self, chunks: list[RetrievedChunk], top_n: int = 5) -> list[RetrievedChunk]:
        """
        Ranks retrieved chunks primarily by similarity score. 
        It also optionally handles deduplication logic per file if we want
        to present only the top distinct files as evidence.
        """
        if not chunks:
            return []
            
        # First, sort all chunks by similarity_score descending
        sorted_chunks = sorted(chunks, key=lambda c: c.similarity_score, reverse=True)
        
        # Deduplicate: only take the highest scoring chunk per file, or allow multiple
        # For this implementation, we will allow multiple snippets from the same file
        # if they are distinct, but we will group them later in the UI or just return them ranked.
        # Let's deduplicate exactly on chunk_id just to be safe.
        seen_chunks = set()
        unique_chunks = []
        for chunk in sorted_chunks:
            if chunk.chunk_id not in seen_chunks:
                seen_chunks.add(chunk.chunk_id)
                unique_chunks.append(chunk)
                
        # To make "real code" files priority over markdown if scores are very close,
        # we could add a minor bump to score for non-markdown, but basic similarity is safest.
        
        return unique_chunks[:top_n]
