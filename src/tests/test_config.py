import pytest
from src.config import get_settings

def test_settings_loaded():
    settings = get_settings()
    assert settings.DATABASE_URL is not None
    assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def test_debug_setting():
    settings = get_settings()
    assert isinstance(settings.DEBUG, bool)

def test_api_keys_present():
    settings = get_settings()
    assert settings.SUBSTACK_API_KEY is not None
    assert settings.TWITTER_API_KEY is not None
    assert settings.LINKEDIN_API_KEY is not None