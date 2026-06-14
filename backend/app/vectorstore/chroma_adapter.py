import chromadb
from chromadb.config import Settings
from chromadb.api.models.Collection import Collection
from app.config.settings import settings

class ChromaAdapter:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False)
        )

    def _get_collection_name(self, repository_id: str) -> str:
        # ChromaDB collection names must be 3-63 characters, alphanumeric or underscores, no hyphens
        return repository_id.replace("-", "_")

    def create_collection(self, repository_id: str) -> Collection:
        name = self._get_collection_name(repository_id)
        return self.client.get_or_create_collection(name=name)

    def get_collection(self, repository_id: str) -> Collection | None:
        name = self._get_collection_name(repository_id)
        try:
            return self.client.get_collection(name=name)
        except Exception:
            return None

    def collection_exists(self, repository_id: str) -> bool:
        return self.get_collection(repository_id) is not None

    def delete_collection(self, repository_id: str) -> None:
        name = self._get_collection_name(repository_id)
        try:
            self.client.delete_collection(name=name)
        except Exception:
            pass

    def add_chunks(self, repository_id: str, ids: list[str], embeddings: list[list[float]], metadatas: list[dict], documents: list[str]) -> None:
        collection = self.create_collection(repository_id)
        # Chroma handles batch insertion, but it's good practice to limit batch size. We'll assume the caller passes reasonable batches.
        collection.add(  # type: ignore
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def search_chunks(self, repository_id: str, query_embedding: list[float], n_results: int = 5) -> dict:
        collection = self.get_collection(repository_id)
        if not collection:
            raise ValueError(f"Collection for repository {repository_id} does not exist.")

        return collection.query(  # type: ignore
            query_embeddings=[query_embedding],
            n_results=n_results
        )
