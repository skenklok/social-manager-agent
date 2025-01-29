from src.models.blog_post import Base
from src.core.database import engine
from src.core.logging_config import setup_logging

logger = setup_logging()

def init_database():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise