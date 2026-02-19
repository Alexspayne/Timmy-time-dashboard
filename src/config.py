from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Ollama host — override with OLLAMA_URL env var or .env file
    ollama_url: str = "http://localhost:11434"

    # LLM model passed to Agno/Ollama — override with OLLAMA_MODEL
    ollama_model: str = "llama3.2"

    # Set DEBUG=true to enable /docs and /redoc (disabled by default)
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
