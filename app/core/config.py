from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sunderland Travel Hub API"
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # Comma-separated list of allowed origins (e.g. "http://localhost:5173,https://example.com")
    allowed_origins: str = "http://localhost:5173"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
