import os
from dataclasses import dataclass
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".idea",
    ".next",
    ".cache",
    ".vscode",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "venv",
    "__pycache__",
}

IGNORED_FILE_EXTENSIONS = {
    ".dll",
    ".exe",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".lock",
    ".mp3",
    ".mp4",
    ".png",
    ".so",
    ".zip",
}

SUPPORTED_FILE_EXTENSIONS = {
    ".css",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".ts",
    ".tsx",
}


@dataclass
class RepositoryDiscoveryResult:
    files: list[Path]
    total_files: int
    ignored_files: int
    ignored_directories: int


def discover_repository_files(repository_root: Path) -> RepositoryDiscoveryResult:
    discovered_files: list[Path] = []
    total_files = 0
    ignored_files = 0
    ignored_directories = 0

    for current_root, directories, filenames in os.walk(repository_root):
        current_path = Path(current_root)

        filtered_directories = []
        for directory in directories:
            if directory in IGNORED_DIRECTORIES:
                ignored_directories += 1
                continue
            filtered_directories.append(directory)
        directories[:] = filtered_directories

        for filename in filenames:
            total_files += 1
            file_path = current_path / filename
            extension = file_path.suffix.lower()

            if extension in IGNORED_FILE_EXTENSIONS:
                ignored_files += 1
                continue

            if extension not in SUPPORTED_FILE_EXTENSIONS:
                ignored_files += 1
                continue

            discovered_files.append(file_path)

    return RepositoryDiscoveryResult(
        files=discovered_files,
        total_files=total_files,
        ignored_files=ignored_files,
        ignored_directories=ignored_directories,
    )
