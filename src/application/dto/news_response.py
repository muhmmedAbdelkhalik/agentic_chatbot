"""News response DTO."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class NewsResponse:
    """
    Data Transfer Object for news generation responses.
    
    Contains the generated news summary and file path.
    """
    
    summary: str
    file_path: Optional[Path] = None
    article_count: int = 0
    
    def __post_init__(self):
        """Validate response."""
        if not self.summary:
            raise ValueError("Summary cannot be empty")

