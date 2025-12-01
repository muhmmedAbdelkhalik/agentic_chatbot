"""News article entity."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class NewsArticle:
    """
    Represents a news article.
    
    Domain entity for news content.
    """
    
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    content: str = ""
    url: str = ""
    published_date: Optional[datetime] = None
    source: Optional[str] = None
    score: Optional[float] = None
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate article on creation."""
        if not self.content and not self.title:
            raise ValueError("Article must have either title or content")
    
    def has_url(self) -> bool:
        """Check if article has a URL."""
        return bool(self.url)
    
    def has_published_date(self) -> bool:
        """Check if article has a published date."""
        return self.published_date is not None
    
    def get_summary(self, max_length: int = 200) -> str:
        """
        Get a summary of the article.
        
        Args:
            max_length: Maximum length of summary
            
        Returns:
            Article summary
        """
        if len(self.content) <= max_length:
            return self.content
        
        return self.content[:max_length] + "..."
    
    def to_dict(self) -> dict:
        """Convert article to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "source": self.source,
            "score": self.score,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "NewsArticle":
        """
        Create article from dictionary.
        
        Args:
            data: Dictionary with article data
            
        Returns:
            NewsArticle instance
        """
        published_date = None
        if data.get("published_date"):
            try:
                published_date = datetime.fromisoformat(data["published_date"])
            except (ValueError, TypeError):
                # If parsing fails, leave as None
                pass
        
        return cls(
            id=data.get("id", str(uuid4())),
            title=data.get("title", ""),
            content=data.get("content", ""),
            url=data.get("url", ""),
            published_date=published_date,
            source=data.get("source"),
            score=data.get("score"),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_tavily_result(cls, result: dict) -> "NewsArticle":
        """
        Create article from Tavily API result.
        
        Args:
            result: Tavily search result dictionary
            
        Returns:
            NewsArticle instance
        """
        # Parse published date if available
        published_date = None
        if result.get("published_date"):
            try:
                published_date = datetime.fromisoformat(result["published_date"])
            except (ValueError, TypeError):
                pass
        
        return cls(
            title=result.get("title", ""),
            content=result.get("content", ""),
            url=result.get("url", ""),
            published_date=published_date,
            source=result.get("source"),
            score=result.get("score"),
            metadata={"raw_result": result}
        )

