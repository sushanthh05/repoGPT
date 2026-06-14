from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config.settings import settings

class EmbeddingService:
    def __init__(self):
        # Load model once during init
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        # HuggingFaceEmbeddings handles batching internally if multiple texts are passed
        return self.embeddings.embed_documents(texts)
    
    def generate_embedding(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
