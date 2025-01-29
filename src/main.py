from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.logging_config import setup_logging
from src.config import get_settings
from src.core.database import get_db
from src.core.init_db import init_database
from src.models.blog_post import BlogPost
from src.tasks.rss_tasks import fetch_substack_posts

logger = setup_logging()
settings = get_settings()

app = FastAPI(
    title="AI Social Media Agent",
    description="An AI-powered social media content manager",
    version="1.0.0",
    debug=settings.DEBUG
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up AI Social Media Agent")
    init_database()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down AI Social Media Agent")

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
@app.post("/fetch-posts")
async def trigger_fetch_posts(db: Session = Depends(get_db)):
    """Manually trigger RSS feed fetch"""
    try:
        task = fetch_substack_posts.delay(settings.SUBSTACK_RSS_URL)
        return {"message": "Feed fetch triggered", "task_id": task.id}
    except Exception as e:
        logger.error(f"Error triggering feed fetch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    """Get all stored blog posts"""
    try:
        posts = db.query(BlogPost).order_by(BlogPost.published_at.desc()).all()
        return [{
            "id": post.id,
            "title": post.title,
            "url": post.url,
            "published_at": post.published_at,
            "is_processed": post.is_processed
        } for post in posts]
    except Exception as e:
        logger.error(f"Error fetching posts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))