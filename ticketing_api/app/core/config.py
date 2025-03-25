from pydantic import BaseSettings, Field
import os

print(f"Environment DATABASE_URL: {os.environ.get('DATABASE_URL')}")

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()

# Ajoutez ceci pour le débogage
print(f"Loaded DATABASE_URL: {settings.DATABASE_URL}")