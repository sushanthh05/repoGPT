from dataclasses import dataclass
from pathlib import Path

from app.parsers.language_detector import detect_language


@dataclass
class ParsedFile:
    filename: str
    file_path: str
    language: str
    file_extension: str
    content: str
    size: int


def read_file_content(file_path: Path) -> str | None:
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None
    except OSError:
        return None


def parse_file(file_path: Path, repository_root: Path) -> ParsedFile | None:
    if not file_path.is_file():
        return None

    try:
        size = file_path.stat().st_size
    except OSError:
        return None

    if size > 1_048_576:
        return None

    content = read_file_content(file_path)
    if content is None:
        return None

    relative_path = file_path.relative_to(repository_root)
    return ParsedFile(
        filename=file_path.name,
        file_path=relative_path.as_posix(),
        language=detect_language(file_path),
        file_extension=file_path.suffix.lower(),
        content=content,
        size=size,
    )
