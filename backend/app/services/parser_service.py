from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.models.document import Document, ParsedRepositoryDocuments
from app.models.repository import RepositoryParseStatistics
from app.parsers.file_parser import parse_file
from app.parsers.repository_parser import discover_repository_files
from app.services.github_service import GitHubService
from app.utils.path_utils import get_parsed_documents_path


class ParserService:
    def __init__(self) -> None:
        self.github_service = GitHubService()
        self.parsed_documents_path = get_parsed_documents_path()

    def parse_repository(self, repository_id: str) -> tuple[list[Document], RepositoryParseStatistics]:
        repository = self.github_service.get_repository_by_id(repository_id)
        if repository is None:
            raise FileNotFoundError("Repository not found")

        repository_root = Path(repository.local_path)
        if not repository_root.exists():
            raise FileNotFoundError("Repository files are missing locally")

        discovery = discover_repository_files(repository_root)
        documents: list[Document] = []
        languages: set[str] = set()

        for file_path in discovery.files:
            parsed_file = parse_file(file_path, repository_root)
            if parsed_file is None:
                continue

            if parsed_file.language == "Unknown":
                continue

            languages.add(parsed_file.language)
            documents.append(
                Document(
                    document_id=f"doc_{uuid.uuid4().hex[:8]}",
                    repository_id=repository_id,
                    filename=parsed_file.filename,
                    file_path=parsed_file.file_path,
                    language=parsed_file.language,
                    file_extension=parsed_file.file_extension,
                    content=parsed_file.content,
                    size=parsed_file.size,
                )
            )

        statistics = RepositoryParseStatistics(
            total_files=discovery.total_files,
            parsed_files=len(documents),
            ignored_files=discovery.ignored_files + (len(discovery.files) - len(documents)),
            ignored_directories=discovery.ignored_directories,
            languages=sorted(languages),
        )

        self._save_parsed_documents(repository_id, documents, statistics)
        return documents, statistics

    def _save_parsed_documents(
        self,
        repository_id: str,
        documents: list[Document],
        statistics: RepositoryParseStatistics,
    ) -> None:
        payload = self._load_parsed_documents()
        payload = [item for item in payload if item.get("repository_id") != repository_id]
        payload.append(
            ParsedRepositoryDocuments(
                repository_id=repository_id,
                parsed_at=datetime.now(timezone.utc).isoformat(),
                statistics=statistics.model_dump(),
                documents=documents,
            ).model_dump(mode="json")
        )
        self.parsed_documents_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _load_parsed_documents(self) -> list[dict[str, Any]]:
        if not self.parsed_documents_path.exists():
            return []

        try:
            raw_payload = json.loads(self.parsed_documents_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        if isinstance(raw_payload, list):
            return [item for item in raw_payload if isinstance(item, dict)]
        return []
