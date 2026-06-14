import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from sqlalchemy.orm import Session

from typing import Literal, cast

from app.models.repository import RepositoryMetadata
from app.utils.path_utils import get_repositories_root
from app.database.models.models import RepositoryDB

GITHUB_REPO_PATTERN = re.compile(r"^/([^/]+)/([^/]+?)(?:\.git)?/?$")

@dataclass
class ParsedRepository:
    owner: str
    name: str
    repository_url: str

class GitHubService:
    def __init__(self, db: Session) -> None:
        self.repositories_root = get_repositories_root()
        self.db = db

    def validate_repo_url(self, repo_url: str) -> ParsedRepository:
        parsed = urlparse(repo_url.strip())
        if parsed.scheme != "https":
            raise ValueError("Only https GitHub repository URLs are supported")

        hostname = parsed.netloc.lower()
        if hostname not in {"github.com", "www.github.com"}:
            raise ValueError("Only GitHub repository URLs are supported")

        if parsed.query or parsed.fragment:
            raise ValueError("Repository URL must not include query parameters or fragments")

        match = GITHUB_REPO_PATTERN.match(parsed.path)
        if not match:
            raise ValueError("Repository URL must follow https://github.com/<owner>/<repository>")

        owner, name = match.groups()
        canonical_url = f"https://github.com/{owner}/{name}"
        return ParsedRepository(owner=owner, name=name, repository_url=canonical_url)

    def clone_repository(self, repo_url: str) -> RepositoryMetadata:
        parsed = self.validate_repo_url(repo_url)
        existing_db = self._find_by_url(parsed.repository_url)
        
        if existing_db is not None and Path(str(self.repositories_root / existing_db.id)).exists():
            return RepositoryMetadata(
                repository_id=existing_db.id,
                repository_name=existing_db.repository_name,
                repository_url=existing_db.repository_url,
                local_path=str(self.repositories_root / existing_db.id),
                status="exists",
                created_at=existing_db.created_at,
                updated_at=existing_db.updated_at
            )

        if existing_db is not None:
            self.db.delete(existing_db)
            self.db.commit()

        repository_id = self._generate_repository_id()
        local_path = self.repositories_root / repository_id
        local_path.mkdir(parents=True, exist_ok=True)

        try:
            from git import Repo
            from git.exc import GitCommandError

            Repo.clone_from(parsed.repository_url, str(local_path))
        except ImportError as exc:
            shutil.rmtree(local_path, ignore_errors=True)
            raise RuntimeError("GitPython is not installed") from exc
        except GitCommandError as exc:
            shutil.rmtree(local_path, ignore_errors=True)
            error_message = str(exc).lower()
            if "not found" in error_message or "repository not found" in error_message:
                raise FileNotFoundError("Repository not found") from exc
            if "permission denied" in error_message or "could not read from remote repository" in error_message:
                raise PermissionError("Private repository or insufficient access") from exc
            raise RuntimeError("Failed to clone repository") from exc
        except OSError as exc:
            shutil.rmtree(local_path, ignore_errors=True)
            raise RuntimeError("Clone failed due to a local file system error") from exc

        repo_db = RepositoryDB(
            id=repository_id,
            repository_name=parsed.name,
            repository_url=parsed.repository_url,
            status="cloned"
        )
        self.db.add(repo_db)
        self.db.commit()
        self.db.refresh(repo_db)

        return RepositoryMetadata(
            repository_id=repo_db.id,
            repository_name=repo_db.repository_name,
            repository_url=repo_db.repository_url,
            local_path=str(local_path),
            status=cast(Literal["cloned", "exists", "failed"], repo_db.status),
            created_at=repo_db.created_at,
            updated_at=repo_db.updated_at
        )

    def list_repositories(self) -> list[RepositoryMetadata]:
        repos_db = self.db.query(RepositoryDB).all()
        return [
            RepositoryMetadata(
                repository_id=r.id,
                repository_name=r.repository_name,
                repository_url=r.repository_url,
                local_path=str(self.repositories_root / r.id),
                status=cast(Literal["cloned", "exists", "failed"], r.status),
                created_at=r.created_at,
                updated_at=r.updated_at
            ) for r in repos_db
        ]

    def get_repository_by_id(self, repository_id: str) -> RepositoryMetadata | None:
        repo_db = self._find_by_id(repository_id)
        if repo_db is None:
            return None
        return RepositoryMetadata(
            repository_id=repo_db.id,
            repository_name=repo_db.repository_name,
            repository_url=repo_db.repository_url,
            local_path=str(self.repositories_root / repo_db.id),
            status=cast(Literal["cloned", "exists", "failed"], repo_db.status),
            created_at=repo_db.created_at,
            updated_at=repo_db.updated_at
        )

    def delete_repository(self, repository_id: str) -> None:
        repo_db = self._find_by_id(repository_id)
        if repo_db is None:
            raise FileNotFoundError("Repository not found")

        local_path = self.repositories_root / repo_db.id
        shutil.rmtree(local_path, ignore_errors=True)
        
        self.db.delete(repo_db)
        self.db.commit()

    def _generate_repository_id(self) -> str:
        while True:
            repository_id = f"repo_{uuid.uuid4().hex[:6]}"
            if self._find_by_id(repository_id) is None and not (self.repositories_root / repository_id).exists():
                return repository_id

    def _find_by_url(self, repository_url: str) -> RepositoryDB | None:
        return self.db.query(RepositoryDB).filter(RepositoryDB.repository_url == repository_url).first()

    def _find_by_id(self, repository_id: str) -> RepositoryDB | None:
        return self.db.query(RepositoryDB).filter(RepositoryDB.id == repository_id).first()