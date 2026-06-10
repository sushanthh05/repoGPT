from dataclasses import dataclass, field


@dataclass(slots=True)
class ChunkMetadata:
    repository_id: str
    document_id: str
    file_path: str
    filename: str
    language: str
    chunk_index: int
    source_file: str = field(init=False)

    def __post_init__(self) -> None:
        self.source_file = self.file_path

    def as_dict(self) -> dict[str, object]:
        return {
            "repository_id": self.repository_id,
            "document_id": self.document_id,
            "file_path": self.file_path,
            "filename": self.filename,
            "language": self.language,
            "chunk_index": self.chunk_index,
            "source_file": self.source_file,
        }