"""News request DTO."""
from dataclasses import dataclass
from ...domain.constants import NewsFrequency


@dataclass
class NewsRequest:
    """
    Data Transfer Object for news generation requests.
    
    Contains all information needed to generate news summary.
    """
    
    frequency: NewsFrequency
    query: str = "Liverpool FC football news"
    max_results: int = 20
    
    def __post_init__(self):
        """Validate request."""
        if not self.query:
            raise ValueError("Query cannot be empty")
        
        if self.max_results <= 0:
            raise ValueError("max_results must be positive")

