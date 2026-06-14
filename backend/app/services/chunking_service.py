from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from pathlib import Path

from app.chunkers.chunk_metadata import ChunkMetadata
from app.chunkers.document_chunker import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE, chunk_document
from app.models.chunk import Chunk, ChunkBatch, ChunkingStatistics
from app.services.parser_service import ParserService
from app.database.models.models import ChunkDB

class ChunkingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.parser_service = ParserService(db)

    def chunk_repository(self, repository_id: str) -> tuple[list[Chunk], ChunkingStatistics]:
        parsed_documents = self.parser_service.get_parsed_repository_documents(repository_id)
        if parsed_documents is None:
            raise FileNotFoundError("Parsed documents not found")

        self.db.query(ChunkDB).filter(ChunkDB.repository_id == repository_id).delete()
        self.db.commit()

        chunks: list[Chunk] = []
        chunks_db_list = []
        per_document_chunk_counts: list[int] = []

        for document in parsed_documents.documents:
            chunked_document = chunk_document(document)
            per_document_chunk_counts.append(len(chunked_document.chunks))

            for chunk_index, chunk_text in enumerate(chunked_document.chunks):
                if not chunk_text.strip():
                    continue

                chunk_id = f"chunk_{uuid.uuid4().hex[:8]}"

                metadata = ChunkMetadata(
                    repository_id=document.repository_id,
                    document_id=document.document_id,
                    file_path=document.file_path,
                    filename=document.filename,
                    language=document.language,
                    chunk_index=chunk_index,
                )
                
                chunk_model = Chunk(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    repository_id=document.repository_id,
                    chunk_index=chunk_index,
                    content=chunk_text,
                    source_file=document.file_path,
                    language=document.language,
                    metadata={
                        **metadata.as_dict(),
                        "chunk_size": DEFAULT_CHUNK_SIZE,
                        "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
                        "content_length": len(chunk_text),
                    },
                )
                chunks.append(chunk_model)
                
                chunks_db_list.append(ChunkDB(
                    id=chunk_id,
                    repository_id=document.repository_id,
                    document_id=document.document_id,
                    chunk_index=chunk_index,
                    content=chunk_text,
                    language=document.language
                ))

        if chunks_db_list:
            self.db.bulk_save_objects(chunks_db_list)
            self.db.commit()

        chunks_generated = len(chunks)
        documents_processed = len(parsed_documents.documents)
        average_chunk_size = (
            int(sum(len(chunk.content) for chunk in chunks) / chunks_generated) if chunks_generated else 0
        )
        largest_file_chunks = max(per_document_chunk_counts, default=0)

        statistics = ChunkingStatistics(
            documents_processed=documents_processed,
            chunks_generated=chunks_generated,
            average_chunk_size=average_chunk_size,
            largest_file_chunks=largest_file_chunks,
            chunk_size=DEFAULT_CHUNK_SIZE,
            chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        )

        return chunks, statistics

    def get_chunk_batch(self, repository_id: str) -> ChunkBatch | None:
        chunks_db = self.db.query(ChunkDB).filter(ChunkDB.repository_id == repository_id).order_by(ChunkDB.document_id, ChunkDB.chunk_index).all()
        if not chunks_db:
            return None

        # Fetch documents to reconstruct metadata
        parsed_documents = self.parser_service.get_parsed_repository_documents(repository_id)
        doc_map = {d.document_id: d for d in parsed_documents.documents} if parsed_documents else {}

        chunks = []
        doc_ids = set()
        total_content_length = 0

        for c in chunks_db:
            doc = doc_map.get(c.document_id)
            doc_ids.add(c.document_id)
            
            file_path = doc.file_path if doc else ""
            filename = Path(file_path).name if file_path else ""

            metadata = ChunkMetadata(
                repository_id=c.repository_id,
                document_id=c.document_id,
                file_path=file_path,
                filename=filename,
                language=c.language or "Unknown",
                chunk_index=c.chunk_index,
            )

            chunk_model = Chunk(
                chunk_id=c.id,
                document_id=c.document_id,
                repository_id=c.repository_id,
                chunk_index=c.chunk_index,
                content=c.content,
                source_file=file_path,
                language=c.language or "Unknown",
                created_at=str(c.created_at) if c.created_at else datetime.now(timezone.utc).isoformat(),
                metadata={
                    **metadata.as_dict(),
                    "chunk_size": DEFAULT_CHUNK_SIZE,
                    "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
                    "content_length": len(c.content),
                },
            )
            chunks.append(chunk_model)
            total_content_length += len(c.content)

        chunks_generated = len(chunks)
        documents_processed = len(doc_ids)
        average_chunk_size = int(total_content_length / chunks_generated) if chunks_generated else 0

        statistics = ChunkingStatistics(
            documents_processed=documents_processed,
            chunks_generated=chunks_generated,
            average_chunk_size=average_chunk_size,
            largest_file_chunks=0, # Approximation for now
            chunk_size=DEFAULT_CHUNK_SIZE,
            chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        )

        return ChunkBatch(
            repository_id=repository_id,
            chunked_at=datetime.now(timezone.utc).isoformat(),
            statistics=statistics,
            chunks=chunks
        )