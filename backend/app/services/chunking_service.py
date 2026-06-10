from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.chunkers.chunk_metadata import ChunkMetadata
from app.chunkers.document_chunker import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE, chunk_document
from app.models.chunk import Chunk, ChunkBatch, ChunkingStatistics
from app.models.document import Document, ParsedRepositoryDocuments
from app.services.parser_service import ParserService
from app.utils.path_utils import get_chunks_path


class ChunkingService:
    def __init__(self) -> None:
        self.parser_service = ParserService()
        self.chunks_path = get_chunks_path()

    def chunk_repository(self, repository_id: str) -> tuple[list[Chunk], ChunkingStatistics]:
        parsed_documents = self.parser_service.get_parsed_repository_documents(repository_id)
        if parsed_documents is None:
            raise FileNotFoundError("Parsed documents not found")

        chunks: list[Chunk] = []
        per_document_chunk_counts: list[int] = []

        for document in parsed_documents.documents:
            chunked_document = chunk_document(document)
            per_document_chunk_counts.append(len(chunked_document.chunks))

            for chunk_index, chunk_text in enumerate(chunked_document.chunks):
                if not chunk_text.strip():
                    continue

                metadata = ChunkMetadata(
                    repository_id=document.repository_id,
                    document_id=document.document_id,
                    file_path=document.file_path,
                    filename=document.filename,
                    language=document.language,
                    chunk_index=chunk_index,
                )
                chunks.append(
                    Chunk(
                        chunk_id=f"chunk_{uuid.uuid4().hex[:8]}",
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
                )

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

        self._save_chunks(repository_id, chunks, statistics)
        return chunks, statistics

    def get_chunk_batch(self, repository_id: str) -> ChunkBatch | None:
        for item in self._load_chunk_batches():
            if item.get("repository_id") != repository_id:
                continue

            try:
                return ChunkBatch.model_validate(item)
            except Exception:
                return None

        return None

    def _save_chunks(self, repository_id: str, chunks: list[Chunk], statistics: ChunkingStatistics) -> None:
        payload = self._load_chunk_batches()
        payload = [item for item in payload if item.get("repository_id") != repository_id]
        payload.append(
            ChunkBatch(
                repository_id=repository_id,
                chunked_at=datetime.now(timezone.utc).isoformat(),
                statistics=statistics,
                chunks=chunks,
            ).model_dump(mode="json")
        )
        self.chunks_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _load_chunk_batches(self) -> list[dict[str, Any]]:
        if not self.chunks_path.exists():
            return []

        try:
            raw_payload = json.loads(self.chunks_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        if isinstance(raw_payload, list):
            return [item for item in raw_payload if isinstance(item, dict)]
        return []