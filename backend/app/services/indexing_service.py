from sqlalchemy.orm import Session
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_store_service import VectorStoreService
from app.database.models.models import ChunkDB, RepositoryDB
import math

class IndexingService:
    def __init__(self, db: Session, embedding_service: EmbeddingService, vector_store: VectorStoreService):
        self.db = db
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_repository(self, repository_id: str, batch_size: int = 100) -> dict:
        repo = self.db.query(RepositoryDB).filter(RepositoryDB.id == repository_id).first()
        if not repo:
            raise FileNotFoundError("Repository not found")

        chunks = self.db.query(ChunkDB).filter(ChunkDB.repository_id == repository_id).all()
        if not chunks:
            raise ValueError("No chunks found for repository. Please chunk the repository first.")

        # Optional: recreate collection to start fresh
        self.vector_store.delete_collection(repository_id)
        self.vector_store.create_collection(repository_id)

        total_chunks = len(chunks)
        processed_chunks = 0
        failed_chunks = 0

        # Process in batches
        for i in range(0, total_chunks, batch_size):
            batch = chunks[i:i + batch_size]
            texts = [c.content for c in batch]
            ids = [c.id for c in batch]
            metadatas = [
                {
                    "chunk_id": c.id,
                    "repository_id": c.repository_id,
                    "document_id": c.document_id,
                    "chunk_index": c.chunk_index,
                    "language": c.language
                } for c in batch
            ]

            try:
                embeddings = self.embedding_service.generate_embeddings(texts)
                self.vector_store.add_chunks(
                    repository_id=repository_id,
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=texts
                )
                processed_chunks += len(batch)
            except Exception as e:
                print(f"Failed to index batch {i}: {e}")
                failed_chunks += len(batch)

        repo.status = "indexed"
        self.db.commit()

        return {
            "status": "success",
            "repository_id": repository_id,
            "chunks_indexed": processed_chunks,
            "failed_chunks": failed_chunks,
            "total_chunks": total_chunks
        }
