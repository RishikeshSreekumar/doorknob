from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@host:port/db"

    class Config:
        env_file = ".env"

settings = Settings()
