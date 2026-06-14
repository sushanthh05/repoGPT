from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.document import Document, ParsedRepositoryDocuments
from app.models.repository import RepositoryParseStatistics
from app.parsers.file_parser import parse_file
from app.parsers.repository_parser import discover_repository_files
from app.services.github_service import GitHubService
from app.database.models.models import DocumentDB

class ParserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.github_service = GitHubService(db)

    def parse_repository(self, repository_id: str) -> tuple[list[Document], RepositoryParseStatistics]:
        repository = self.github_service.get_repository_by_id(repository_id)
        if repository is None:
            raise FileNotFoundError("Repository not found")

        repository_root = Path(repository.local_path)
        if not repository_root.exists():
            raise FileNotFoundError("Repository files are missing locally")

        # Clear existing documents for this repo
        self.db.query(DocumentDB).filter(DocumentDB.repository_id == repository_id).delete()
        self.db.commit()

        discovery = discover_repository_files(repository_root)
        documents: list[Document] = []
        languages: set[str] = set()

        docs_db_list = []

        for file_path in discovery.files:
            parsed_file = parse_file(file_path, repository_root)
            if parsed_file is None:
                continue

            if parsed_file.language == "Unknown":
                continue

            languages.add(parsed_file.language)
            doc_id = f"doc_{uuid.uuid4().hex[:8]}"
            
            doc_model = Document(
                document_id=doc_id,
                repository_id=repository_id,
                filename=parsed_file.filename,
                file_path=parsed_file.file_path,
                language=parsed_file.language,
                file_extension=parsed_file.file_extension,
                content=parsed_file.content,
                size=parsed_file.size,
            )
            documents.append(doc_model)
            
            docs_db_list.append(DocumentDB(
                id=doc_id,
                repository_id=repository_id,
                file_path=parsed_file.file_path,
                language=parsed_file.language,
                file_extension=parsed_file.file_extension
            ))

        if docs_db_list:
            self.db.bulk_save_objects(docs_db_list)
            self.db.commit()

        statistics = RepositoryParseStatistics(
            total_files=discovery.total_files,
            parsed_files=len(documents),
            ignored_files=discovery.ignored_files + (len(discovery.files) - len(documents)),
            ignored_directories=discovery.ignored_directories,
            languages=sorted(languages),
        )

        return documents, statistics

    def get_parsed_repository_documents(self, repository_id: str) -> ParsedRepositoryDocuments | None:
        repository = self.github_service.get_repository_by_id(repository_id)
        if repository is None:
            return None
            
        docs_db = self.db.query(DocumentDB).filter(DocumentDB.repository_id == repository_id).all()
        if not docs_db:
            return None

        repository_root = Path(repository.local_path)
        documents = []
        languages = set()
        
        for d in docs_db:
            full_path = repository_root / d.file_path
            content = ""
            size = 0
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding="utf-8")
                    size = len(content)
                except Exception:
                    pass
            
            if d.language:
                languages.add(d.language)
            documents.append(Document(
                document_id=d.id,
                repository_id=d.repository_id,
                filename=Path(d.file_path).name,
                file_path=d.file_path,
                language=d.language or "Unknown",
                file_extension=d.file_extension or "",
                content=content,
                size=size,
                created_at=str(d.created_at) if d.created_at else datetime.now(timezone.utc).isoformat()
            ))

        statistics = RepositoryParseStatistics(
            total_files=len(documents), # Approximate stats
            parsed_files=len(documents),
            ignored_files=0,
            ignored_directories=0,
            languages=sorted(languages),
        )

        return ParsedRepositoryDocuments(
            repository_id=repository_id,
            parsed_at=datetime.now(timezone.utc).isoformat(),
            statistics=statistics.model_dump(),
            documents=documents
        )
