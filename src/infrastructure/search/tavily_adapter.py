"""Tavily search adapter implementing ISearchService interface."""
from typing import List, Optional
from tavily import TavilyClient
from ...domain.interfaces.search_service import ISearchService
from ...domain.entities.news_article import NewsArticle
from ...domain.constants import NewsFrequency, NEWS_TIME_RANGE_MAP, NEWS_DAYS_MAP
from ...domain.exceptions import SearchServiceError, MissingCredentialError
from ..security.credential_manager import CredentialManager
from ..logging.security_audit import SecurityAuditLogger


class TavilySearchAdapter(ISearchService):
    """
    Adapter for Tavily search service.
    
    Implements the ISearchService interface using Tavily's API.
    """
    
    def __init__(
        self,
        credential_manager: CredentialManager,
        audit_logger: Optional[SecurityAuditLogger] = None
    ):
        """
        Initialize Tavily adapter.
        
        Args:
            credential_manager: Manager for API credentials
            audit_logger: Optional security audit logger
            
        Raises:
            MissingCredentialError: If Tavily API key is not available
        """
        self._credential_manager = credential_manager
        self._audit_logger = audit_logger or SecurityAuditLogger()
        
        # Get API key
        api_key = self._credential_manager.get_tavily_api_key()
        if not api_key:
            self._audit_logger.log_credential_access("tavily", success=False)
            raise MissingCredentialError(
                "Tavily API key not found. Please set TAVILY_API_KEY environment variable."
            )
        
        self._audit_logger.log_credential_access("tavily", success=True)
        
        # Initialize Tavily client
        try:
            self._client = TavilyClient(api_key=api_key)
        except Exception as e:
            raise SearchServiceError(
                f"Failed to initialize Tavily client: {str(e)}",
                details={"error": str(e)}
            )
    
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
            frequency: Time range for news
            max_results: Maximum number of results
            
        Returns:
            List of news articles
            
        Raises:
            SearchServiceError: If search fails
        """
        try:
            # Get time range and days from frequency
            time_range = NEWS_TIME_RANGE_MAP.get(frequency, 'd')
            days = NEWS_DAYS_MAP.get(frequency, 1)
            
            # Perform search
            response = self._client.search(
                query=query,
                topic="news",
                time_range=time_range,
                include_answer="advanced",
                max_results=max_results,
                days=days
            )
            
            # Convert results to NewsArticle entities
            articles = []
            for result in response.get('results', []):
                try:
                    article = NewsArticle.from_tavily_result(result)
                    articles.append(article)
                except Exception as e:
                    # Log but don't fail on individual article parsing errors
                    self._audit_logger.log_suspicious_activity(
                        "Failed to parse news article",
                        details={"error": str(e), "result": result}
                    )
            
            return articles
            
        except Exception as e:
            raise SearchServiceError(
                f"Failed to search news: {str(e)}",
                details={"error": str(e), "query": query, "frequency": frequency.value}
            )
    
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
        try:
            response = self._client.search(
                query=query,
                max_results=max_results
            )
            
            return response.get('results', [])
            
        except Exception as e:
            raise SearchServiceError(
                f"Failed to search web: {str(e)}",
                details={"error": str(e), "query": query}
            )
    
    def is_available(self) -> bool:
        """Check if the search service is available."""
        return self._credential_manager.has_tavily_api_key()
    
    def get_raw_client(self):
        """
        Get the raw Tavily client for backward compatibility.
        
        Returns:
            TavilyClient instance
        """
        return self._client

