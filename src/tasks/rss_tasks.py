from celery import Celery
from src.core.database import SessionLocal
from src.services.rss_fetcher import SubstackRSSFetcher, RSSFetchError
from src.core.logging_config import setup_logging
from src.config import get_settings

logger = setup_logging()
settings = get_settings()

celery = Celery(
    'rss_tasks',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery.task(
    bind=True,
    max_retries=3,
    default_retry_delay=300  # 5 minutes
)
def fetch_substack_posts(self, rss_url: str):
    try:
        db = SessionLocal()
        fetcher = SubstackRSSFetcher(db, rss_url)
        posts = fetcher.fetch_posts()  # Changed from fetch_and_store_posts
        logger.info(f"Successfully fetched {len(posts)} new posts")
        db.close()
        
    except Exception as e:
        logger.error(f"Unexpected error in RSS fetch task: {str(e)}")
        self.retry(exc=e)