"""Chat request DTO."""
from dataclasses import dataclass
from typing import Optional
from ...domain.value_objects.model_config import ModelConfig


@dataclass
class ChatRequest:
    """
    Data Transfer Object for chat requests.
    
    Contains all information needed to process a chat message.
    """
    
    message: str
    conversation_id: Optional[str] = None
    model_config: Optional[ModelConfig] = None
    use_tools: bool = False
    
    def __post_init__(self):
        """Validate request."""
        if not self.message:
            raise ValueError("Message cannot be empty")

