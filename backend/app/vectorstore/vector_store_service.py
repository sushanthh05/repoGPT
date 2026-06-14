from app.vectorstore.chroma_adapter import ChromaAdapter

class VectorStoreService:
    def __init__(self) -> None:
        # Currently hardcoded to Chroma, but abstracted behind adapter
        self.adapter = ChromaAdapter()

    def create_collection(self, repository_id: str):
        return self.adapter.create_collection(repository_id)

    def collection_exists(self, repository_id: str) -> bool:
        return self.adapter.collection_exists(repository_id)

    def delete_collection(self, repository_id: str) -> None:
        self.adapter.delete_collection(repository_id)

    def get_collection(self, repository_id: str):
        return self.adapter.get_collection(repository_id)

    def add_chunks(self, repository_id: str, ids: list[str], embeddings: list[list[float]], metadatas: list[dict], documents: list[str]) -> None:
        self.adapter.add_chunks(repository_id, ids, embeddings, metadatas, documents)

    def search_chunks(self, repository_id: str, query_embedding: list[float], n_results: int = 5) -> dict:
        return self.adapter.search_chunks(repository_id, query_embedding, n_results)
