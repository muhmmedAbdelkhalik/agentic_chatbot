"""Conversation entity."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from .message import Message
from ..exceptions import ValidationError


@dataclass
class Conversation:
    """
    Represents a conversation with business logic.
    
    Encapsulates conversation state and behavior.
    """
    
    id: str = field(default_factory=lambda: str(uuid4()))
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    max_messages: int = 100
    
    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation.
        
        Args:
            message: Message to add
            
        Raises:
            ValidationError: If conversation limit is reached
        """
        if not self._can_add_message():
            raise ValidationError(
                f"Conversation has reached maximum message limit of {self.max_messages}",
                details={"current_count": len(self.messages), "max": self.max_messages}
            )
        
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
    
    def add_user_message(self, content: str) -> Message:
        """
        Add a user message to the conversation.
        
        Args:
            content: Message content
            
        Returns:
            The created message
        """
        message = Message.user_message(content)
        self.add_message(message)
        return message
    
    def add_assistant_message(self, content: str) -> Message:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: Message content
            
        Returns:
            The created message
        """
        message = Message.assistant_message(content)
        self.add_message(message)
        return message
    
    def get_context_window(self, size: int = 10) -> List[Message]:
        """
        Get the most recent messages for context.
        
        Args:
            size: Number of messages to retrieve
            
        Returns:
            List of recent messages
        """
        return self.messages[-size:] if len(self.messages) > size else self.messages
    
    def get_message_count(self) -> int:
        """Get the total number of messages."""
        return len(self.messages)
    
    def _can_add_message(self) -> bool:
        """Check if a message can be added."""
        return len(self.messages) < self.max_messages
    
    def clear_messages(self) -> None:
        """Clear all messages from the conversation."""
        self.messages.clear()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert conversation to dictionary."""
        return {
            "id": self.id,
            "messages": [msg.to_dict() for msg in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id,
            "metadata": self.metadata,
            "max_messages": self.max_messages
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        """
        Create conversation from dictionary.
        
        Args:
            data: Dictionary with conversation data
            
        Returns:
            Conversation instance
        """
        return cls(
            id=data.get("id", str(uuid4())),
            messages=[Message.from_dict(msg) for msg in data.get("messages", [])],
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.utcnow(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.utcnow(),
            user_id=data.get("user_id"),
            metadata=data.get("metadata", {}),
            max_messages=data.get("max_messages", 100)
        )
    
    @classmethod
    def create(cls, user_id: Optional[str] = None, max_messages: int = 100) -> "Conversation":
        """
        Factory method to create a new conversation.
        
        Args:
            user_id: Optional user identifier
            max_messages: Maximum number of messages allowed
            
        Returns:
            New Conversation instance
        """
        return cls(user_id=user_id, max_messages=max_messages)

