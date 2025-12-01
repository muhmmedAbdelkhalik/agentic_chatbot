"""Search service interface."""
from abc import ABC, abstractmethod
from typing import List
from ..entities.news_article import NewsArticle
from ..constants import NewsFrequency


class ISearchService(ABC):
    """
    Interface for search services.
    
    Defines the contract for news/web search operations.
    """
    
    @abstractmethod
    def search_news(
        self,
        query: str,
        frequency: NewsFrequency,
        max_results: int = 20
    ) -> List[NewsArticle]:
        """
        Search for news articles.
        
        Args:
            query: Search query
            frequency: Time range for news (daily, weekly, etc.)
            max_results: Maximum number of results
            
        Returns:
            List of news articles
            
        Raises:
            SearchServiceError: If search fails
        """
        pass
    
    @abstractmethod
    def search_web(self, query: str, max_results: int = 5) -> List[dict]:
        """
        Perform a web search.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results
            
        Raises:
            SearchServiceError: If search fails
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the search service is available.
        
        Returns:
            True if service is ready to use
        """
        pass

