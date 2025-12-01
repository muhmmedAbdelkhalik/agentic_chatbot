"""Chat response DTO."""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ChatResponse:
    """
    Data Transfer Object for chat responses.
    
    Contains the response from the chatbot.
    """
    
    content: str
    conversation_id: str
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}

