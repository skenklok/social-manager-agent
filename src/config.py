from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://default:vOoKGjkcATfmaQ5w1P3Za5P7Z77j3WW0@redis-13763.c338.eu-west-2-1.ec2.redns.redis-cloud.com:13763"
    
    # RSS Feed
    SUBSTACK_RSS_URL: str
    RSS_FETCH_INTERVAL: int = 3600
    
    # Social Media API Keys
    TWITTER_API_KEY: Optional[str] = None
    LINKEDIN_API_KEY: Optional[str] = None
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()