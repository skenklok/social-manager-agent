import pytest
from src.core.logging_config import setup_logging

@pytest.fixture(autouse=True)
def setup_test_logging():
    """Setup logging for all tests"""
    logger = setup_logging()
    return logger