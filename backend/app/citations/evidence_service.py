from app.retrieval.retrieval_models import RetrievedChunk
from app.citations.source_manager import SourceEvidence

class EvidenceService:
    def extract_snippet(self, content: str, max_lines: int = 7, max_chars: int = 300) -> str:
        """
        Extracts a clean snippet from chunk content.
        Gets the first `max_lines` or `max_chars`, whichever comes first.
        """
        if not content:
            return ""
            
        lines = content.strip().split("\n")
        snippet_lines = lines[:max_lines]
        snippet = "\n".join(snippet_lines)
        
        if len(snippet) > max_chars:
            snippet = snippet[:max_chars] + "..."
        elif len(lines) > max_lines:
            snippet += "\n..."
            
        return snippet

    def build_evidence(self, chunk: RetrievedChunk) -> SourceEvidence:
        """
        Converts a RetrievedChunk into a SourceEvidence object.
        """
        snippet = self.extract_snippet(chunk.content)
        return SourceEvidence(
            file_path=chunk.file_path,
            chunk_id=chunk.chunk_id,
            similarity_score=round(chunk.similarity_score, 4),
            language=chunk.language,
            snippet=snippet
        )

    def calculate_confidence(self, chunks: list[RetrievedChunk]) -> int:
        """
        Generates a 0-100 confidence score based on retrieval results.
        Heuristics:
        - Max possible score is derived from the highest similarity score.
        - Number of retrieved chunks adds minor confidence.
        """
        if not chunks:
            return 0
            
        # Basic heuristic: we scale the similarity score (0.0 - 1.0) to 0-100.
        # Often vector store scores might not be perfectly 1.0, 
        # so we map an expected "good" score range.
        best_score = max(chunk.similarity_score for chunk in chunks)
        
        # We assume similarity_score is between 0 and 1.
        # If it's a distance, we assume it's been inverted in the retriever.
        base_confidence = min(best_score * 100, 100.0)
        
        # Add a small bump if there are multiple supporting chunks (e.g. up to +5)
        support_bump = min((len(chunks) - 1) * 2.5, 5.0)
        
        final_score = int(base_confidence + support_bump)
        
        # Ensure it doesn't exceed 100
        return min(max(final_score, 0), 100)
