from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sunderland Travel Hub API"
    #Original 
    # database_url: str = "sqlite:///./dev.db"
    
    #New
    database_url: str | None = None
    
    # Old secret key (for development only)
    # secret_key: str = "changeme"

    #New secret key 
    secret_key: str = "L9GPVLVk+1oNrusR0VD19uhNvg1B8fe2vYGBCv2iaEs="
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # Comma-separated list of allowed origins (e.g. "http://localhost:5173,https://example.com")
    allowed_origins: str = "http://localhost:5173" 
    # , https://uos-sustainable-travel.vercel.app"

    # New database url property
    @property
    def resolved_database_url(self) -> str:
        return self.database_url or "sqlite:///./dev.db"
    
    @property
    def allowed_origins_list(self) -> list[str]:
        # original
        # return [origin.strip() for origin in self.allowed_origins.split(",")]
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
