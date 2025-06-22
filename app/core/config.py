import yaml

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TITLE: str = "Plumbus image generation Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Everyone have plumbus..."

settings = Settings()
