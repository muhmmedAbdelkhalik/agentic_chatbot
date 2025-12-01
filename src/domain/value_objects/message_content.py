"""Message content value object."""
from dataclasses import dataclass
from ..validation.message_validator import MessageValidator


@dataclass(frozen=True)
class MessageContent:
    """
    Immutable value object representing validated message content.
    
    This ensures all message content is validated before use.
    """
    
    content: str
    
    def __post_init__(self):
        """Validate content on creation."""
        validator = MessageValidator()
        # This will raise if validation fails
        object.__setattr__(self, 'content', validator.validate_message(self.content))
    
    def __str__(self) -> str:
        """Return the content string."""
        return self.content
    
    def __len__(self) -> int:
        """Return the length of the content."""
        return len(self.content)
    
    @classmethod
    def create(cls, content: str) -> "MessageContent":
        """
        Factory method to create MessageContent.
        
        Args:
            content: The message content
            
        Returns:
            MessageContent instance
            
        Raises:
            ValidationError: If content is invalid
        """
        return cls(content=content)

