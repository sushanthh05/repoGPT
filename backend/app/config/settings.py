import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./repogpt.db"
    VECTOR_DB: str = "chroma"
    CHROMA_PATH: str = "data/chroma"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    GROQ_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
