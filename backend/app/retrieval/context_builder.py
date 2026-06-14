from app.retrieval.retrieval_models import RetrievedChunk

class ContextBuilder:
    def __init__(self, max_chunks: int = 5, max_chars: int = 10000):
        self.max_chunks = max_chunks
        self.max_chars = max_chars

    def build_context(self, chunks: list[RetrievedChunk]) -> tuple[str, list[dict]]:
        """
        Builds a single context string from the retrieved chunks, ensuring it does not
        exceed the maximum token/character limits.
        
        Returns a tuple of (context_string, list_of_sources)
        """
        context_parts = []
        sources = []
        current_chars = 0
        
        for i, chunk in enumerate(chunks):
            if i >= self.max_chunks:
                break
                
            formatted_chunk = f"File:\n{chunk.file_path}\n\nContent:\n{chunk.content}\n\n---\n\n"
            chunk_len = len(formatted_chunk)
            
            # If a single chunk is larger than max_chars, we might just truncate it or skip
            # But let's assume chunks are around 1000 chars anyway.
            if current_chars + chunk_len > self.max_chars and current_chars > 0:
                break
                
            context_parts.append(formatted_chunk)
            current_chars += chunk_len
            
            # Add to sources list
            sources.append({
                "repository_id": chunk.repository_id,
                "file_path": chunk.file_path,
                "language": chunk.language,
                "similarity_score": chunk.similarity_score,
                "chunk_index": chunk.chunk_index
            })
            
        context_string = "".join(context_parts).strip()
        
        return context_string, sources
