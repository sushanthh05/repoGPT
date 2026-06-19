from app.retrieval.retrieval_models import RetrievedChunk
from app.citations.citation_builder import CitationBuilder
from app.citations.evidence_service import EvidenceService

class CitationService:
    def __init__(self):
        self.citation_builder = CitationBuilder()
        self.evidence_service = EvidenceService()

    def generate_citations(self, chunks: list[RetrievedChunk]) -> tuple[list[dict], int]:
        """
        Takes raw retrieved chunks and returns a formatted list of evidence sources
        along with a confidence score.
        """
        # 1. Rank and Deduplicate chunks
        ranked_chunks = self.citation_builder.rank_and_deduplicate(chunks, top_n=5)
        
        # 2. Build Evidence objects
        sources = [self.evidence_service.build_evidence(chunk) for chunk in ranked_chunks]
        
        # 3. Calculate Confidence
        confidence = self.evidence_service.calculate_confidence(chunks)
        
        # 4. Return as dicts for the response model
        source_dicts = [source.model_dump() for source in sources]
        
        return source_dicts, confidence
