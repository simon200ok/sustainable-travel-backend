from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sunderland Travel Hub API"
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
