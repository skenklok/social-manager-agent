from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    content_html = Column(Text, nullable=False)
    published_at = Column(DateTime, nullable=False)
    author = Column(String(255))
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BlogPost(title='{self.title}', published_at='{self.published_at}')>"