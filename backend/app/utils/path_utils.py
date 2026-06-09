from pathlib import Path


def get_backend_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_repositories_root() -> Path:
    repositories_root = get_backend_root() / "repositories"
    repositories_root.mkdir(parents=True, exist_ok=True)
    return repositories_root


def get_metadata_path() -> Path:
    return get_backend_root() / "repository_metadata.json"