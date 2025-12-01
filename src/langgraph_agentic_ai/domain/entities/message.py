"""Message entity."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class MessageRole(str, Enum):
    """Role of the message sender."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """
    Represents a message in a conversation.
    
    This is a rich domain entity with behavior and business rules.
    """
    
    id: str = field(default_factory=lambda: str(uuid4()))
    role: MessageRole = MessageRole.USER
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate message on creation."""
        if not self.content:
            raise ValueError("Message content cannot be empty")
        
        if len(self.content) > 5000:
            raise ValueError("Message content exceeds maximum length")
    
    @classmethod
    def user_message(cls, content: str, metadata: Optional[dict] = None) -> "Message":
        """
        Create a user message.
        
        Args:
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Message instance
        """
        return cls(
            role=MessageRole.USER,
            content=content,
            metadata=metadata or {}
        )
    
    @classmethod
    def assistant_message(cls, content: str, metadata: Optional[dict] = None) -> "Message":
        """
        Create an assistant message.
        
        Args:
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Message instance
        """
        return cls(
            role=MessageRole.ASSISTANT,
            content=content,
            metadata=metadata or {}
        )
    
    @classmethod
    def system_message(cls, content: str, metadata: Optional[dict] = None) -> "Message":
        """
        Create a system message.
        
        Args:
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Message instance
        """
        return cls(
            role=MessageRole.SYSTEM,
            content=content,
            metadata=metadata or {}
        )
    
    def is_user_message(self) -> bool:
        """Check if this is a user message."""
        return self.role == MessageRole.USER
    
    def is_assistant_message(self) -> bool:
        """Check if this is an assistant message."""
        return self.role == MessageRole.ASSISTANT
    
    def is_system_message(self) -> bool:
        """Check if this is a system message."""
        return self.role == MessageRole.SYSTEM
    
    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """
        Create message from dictionary.
        
        Args:
            data: Dictionary with message data
            
        Returns:
            Message instance
        """
        return cls(
            id=data.get("id", str(uuid4())),
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            metadata=data.get("metadata", {})
        )

