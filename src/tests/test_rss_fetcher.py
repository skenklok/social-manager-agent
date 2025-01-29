import pytest
from unittest.mock import Mock, patch
from src.services.rss_fetcher import SubstackRSSFetcher, RSSFetchError
from src.models.blog_post import BlogPost

@pytest.fixture
def mock_feed_entry():
    return Mock(
        title="Test Post",
        link="https://test.substack.com/p/test-post",
        content=[Mock(value="<p>Test content</p>")],
        published="Mon, 01 Jan 2024 12:00:00 GMT",  # Changed date format
        description="Test description",  # Added description
        author="Test Author"
    )

@pytest.fixture
def mock_db_session():
    return Mock()

def test_process_feed_entry(mock_db_session, mock_feed_entry):
    fetcher = SubstackRSSFetcher(mock_db_session)
    
    # Mock the query to return None (no existing post)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    
    result = fetcher._process_feed_entry(mock_feed_entry)
    
    assert isinstance(result, BlogPost)
    assert result.title == "Test Post"
    assert result.author == "Test Author"
    assert not result.is_processed

def test_fetch_and_store_posts(mock_db_session):
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = Mock(
            bozo=False,
            entries=[mock_feed_entry()]
        )
        
        fetcher = SubstackRSSFetcher(mock_db_session)
        results = fetcher.fetch_and_store_posts("https://test.substack.com/feed")
        
        assert len(results) == 1
        assert isinstance(results[0], BlogPost)

def test_fetch_error_handling(mock_db_session):
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = Mock(
            bozo=True,
            bozo_exception=Exception("Test error")
        )
        
        fetcher = SubstackRSSFetcher(mock_db_session)
        with pytest.raises(RSSFetchError):
            fetcher.fetch_and_store_posts("https://test.substack.com/feed")