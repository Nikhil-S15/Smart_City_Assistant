from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    chroma_db_path: str = "data/chroma_db"
    ollama_model: str = "llama3"
    api_port: int = 8000
    api_host: str = "0.0.0.0"

settings = Settings()