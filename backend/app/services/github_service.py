import json
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from app.models.repository import RepositoryMetadata
from app.utils.path_utils import get_metadata_path, get_repositories_root


GITHUB_REPO_PATTERN = re.compile(r"^/([^/]+)/([^/]+?)(?:\.git)?/?$")


@dataclass
class ParsedRepository:
    owner: str
    name: str
    repository_url: str


class GitHubService:
    def __init__(self) -> None:
        self.repositories_root = get_repositories_root()
        self.metadata_path = get_metadata_path()
        self._metadata_cache = self._load_metadata()

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
        existing = self._find_by_url(parsed.repository_url)
        if existing is not None and Path(existing.local_path).exists():
            return existing.model_copy(update={"status": "exists"})

        if existing is not None:
            self._metadata_cache = [item for item in self._metadata_cache if item.repository_id != existing.repository_id]
            self._save_metadata()

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

        repository = RepositoryMetadata.create(
            repository_id=repository_id,
            repository_name=parsed.name,
            repository_url=parsed.repository_url,
            local_path=str(local_path),
            status="cloned",
        )
        self._metadata_cache.append(repository)
        self._save_metadata()
        return repository

    def list_repositories(self) -> list[RepositoryMetadata]:
        return list(self._metadata_cache)

    def get_repository_by_id(self, repository_id: str) -> RepositoryMetadata | None:
        return self._find_by_id(repository_id)

    def delete_repository(self, repository_id: str) -> None:
        repository = self._find_by_id(repository_id)
        if repository is None:
            raise FileNotFoundError("Repository not found")

        shutil.rmtree(Path(repository.local_path), ignore_errors=True)
        self._metadata_cache = [item for item in self._metadata_cache if item.repository_id != repository_id]
        self._save_metadata()

    def _generate_repository_id(self) -> str:
        while True:
            repository_id = f"repo_{uuid.uuid4().hex[:6]}"
            if self._find_by_id(repository_id) is None and not (self.repositories_root / repository_id).exists():
                return repository_id

    def _load_metadata(self) -> list[RepositoryMetadata]:
        if not self.metadata_path.exists():
            return []

        try:
            with self.metadata_path.open("r", encoding="utf-8") as file:
                raw_entries: list[dict[str, Any]] = json.load(file)
        except json.JSONDecodeError:
            return []

        repositories: list[RepositoryMetadata] = []
        for item in raw_entries:
            try:
                repositories.append(RepositoryMetadata.model_validate(item))
            except Exception:
                continue
        return repositories

    def _save_metadata(self) -> None:
        with self.metadata_path.open("w", encoding="utf-8") as file:
            json.dump([item.model_dump() for item in self._metadata_cache], file, indent=2)

    def _find_by_url(self, repository_url: str) -> RepositoryMetadata | None:
        for item in self._metadata_cache:
            if item.repository_url == repository_url:
                return item
        return None

    def _find_by_id(self, repository_id: str) -> RepositoryMetadata | None:
        for item in self._metadata_cache:
            if item.repository_id == repository_id:
                return item
        return None