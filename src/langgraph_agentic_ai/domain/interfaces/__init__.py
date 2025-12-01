"""Domain interfaces (ports) for dependency inversion."""
from .llm_provider import ILLMProvider
from .storage_service import IStorageService
from .search_service import ISearchService

__all__ = ["ILLMProvider", "IStorageService", "ISearchService"]

