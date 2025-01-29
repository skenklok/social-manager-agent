import feedparser
import html2text
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.blog_post import BlogPost
from src.core.logging_config import setup_logging
from src.config import get_settings

logger = setup_logging()
settings = get_settings()

class RSSFetchError(Exception):
    """Custom exception for RSS fetch errors"""
    pass

class SubstackRSSFetcher:
    def __init__(self, db_session: Session, rss_url: str = None):
            self.db_session = db_session
            self.rss_url = rss_url
            self.html_converter = html2text.HTML2Text()
            self.html_converter.ignore_links = False
            self.html_converter.ignore_images = False
        
    def fetch_posts(self) -> List[BlogPost]:
            try:
                logger.info(f"Fetching RSS feed from: {self.rss_url}")
                feed = feedparser.parse(self.rss_url)
                
                if feed.bozo:
                    logger.error(f"Error parsing feed: {feed.bozo_exception}")
                    return []
                
                logger.info(f"Found {len(feed.entries)} entries in feed")
                new_posts = []
                
                for entry in feed.entries:
                    post = self._process_feed_entry(entry)
                    if post:
                        new_posts.append(post)
                
                return new_posts
                
            except Exception as e:
                logger.error(f"Error fetching posts: {str(e)}")
                return []
    


    def _process_feed_entry(self, entry) -> Optional[BlogPost]:
        try:
            # Check if post already exists
            existing_post = self.db_session.query(BlogPost).filter_by(
                url=entry.link
            ).first()

            if existing_post:
                return None

            # Debug logging
            logger.info("=== Debug Info ===")
            logger.info(f"Raw entry: {entry}")
            logger.info(f"Published date: {entry.published}")
            logger.info(f"Type of published date: {type(entry.published)}")

            try:
                # Parse published date using parsedate_to_datetime
                published_at = parsedate_to_datetime(entry.published)
                logger.info(f"Successfully parsed date: {published_at}")
            except Exception as e:
                logger.error(f"Failed to parse date: {e}")
                raise

            # Create new blog post
            new_post = BlogPost(
                title=entry.title,
                url=entry.link,
                content=entry.description,
                content_html=entry.description,
                published_at=published_at,
                author=getattr(entry, 'author', None),
                is_processed=False
            )

            # Save new post to database
            self.db_session.add(new_post)
            self.db_session.commit()

            return new_post

        except Exception as e:
            logger.error(f"Error processing feed entry: {e}")
            return None
