from pathlib import Path


EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "JavaScript React",
    ".tsx": "TypeScript React",
    ".java": "Java",
    ".md": "Markdown",
    ".json": "JSON",
    ".html": "HTML",
    ".css": "CSS",
}


def detect_language(file_path: Path | str) -> str:
    extension = Path(file_path).suffix.lower()
    return EXTENSION_LANGUAGE_MAP.get(extension, "Unknown")
