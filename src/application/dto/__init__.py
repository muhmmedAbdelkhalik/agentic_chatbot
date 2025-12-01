"""Data Transfer Objects for application layer."""
from .chat_request import ChatRequest
from .chat_response import ChatResponse
from .news_request import NewsRequest
from .news_response import NewsResponse

__all__ = ["ChatRequest", "ChatResponse", "NewsRequest", "NewsResponse"]

