"""Message validation to prevent security issues."""
import re
from typing import Optional
from ..exceptions import (
    ValidationError,
    PromptInjectionError,
    MessageTooLongError,
    InvalidFrequencyError
)


class MessageValidator:
    """
    Validates user messages for security and business rules.
    
    Checks for:
    - Maximum length
    - Prompt injection patterns
    - Malicious content
    - Valid frequency values for news
    """
    
    MAX_MESSAGE_LENGTH = 5000
    MIN_MESSAGE_LENGTH = 1
    
    # Patterns that might indicate prompt injection
    INJECTION_PATTERNS = [
        r'(ignore|forget|disregard|override)\s+(previous|above|prior|all)\s+(instructions|prompts|rules|commands)',
        r'system\s*:\s*you\s+are',
        r'<\s*script\s*>',
        r'javascript\s*:',
        r'on(load|error|click)\s*=',
    ]
    
    VALID_FREQUENCIES = ['daily', 'weekly', 'monthly', 'year']
    
    def validate_message(self, message: str) -> str:
        """
        Validate a user message.
        
        Args:
            message: The message to validate
            
        Returns:
            The sanitized message
            
        Raises:
            ValidationError: If validation fails
            MessageTooLongError: If message is too long
            PromptInjectionError: If prompt injection is detected
        """
        if not message:
            raise ValidationError("Message cannot be empty")
        
        # Check length
        if len(message) > self.MAX_MESSAGE_LENGTH:
            raise MessageTooLongError(
                f"Message exceeds maximum length of {self.MAX_MESSAGE_LENGTH} characters",
                details={"length": len(message), "max_length": self.MAX_MESSAGE_LENGTH}
            )
        
        if len(message) < self.MIN_MESSAGE_LENGTH:
            raise ValidationError("Message is too short")
        
        # Check for prompt injection
        self._check_prompt_injection(message)
        
        # Sanitize whitespace
        sanitized = self._sanitize_whitespace(message)
        
        return sanitized
    
    def validate_frequency(self, frequency: str) -> str:
        """
        Validate news frequency input.
        
        Args:
            frequency: The frequency string to validate
            
        Returns:
            The normalized frequency (lowercase)
            
        Raises:
            InvalidFrequencyError: If frequency is invalid
        """
        if not frequency:
            raise InvalidFrequencyError("Frequency cannot be empty")
        
        normalized = frequency.lower().strip()
        
        if normalized not in self.VALID_FREQUENCIES:
            raise InvalidFrequencyError(
                f"Invalid frequency: {frequency}. Must be one of: {', '.join(self.VALID_FREQUENCIES)}",
                details={"provided": frequency, "valid_options": self.VALID_FREQUENCIES}
            )
        
        return normalized
    
    def _check_prompt_injection(self, message: str) -> None:
        """
        Check for potential prompt injection patterns.
        
        Args:
            message: The message to check
            
        Raises:
            PromptInjectionError: If injection pattern is detected
        """
        message_lower = message.lower()
        
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                raise PromptInjectionError(
                    "Potential prompt injection detected",
                    details={"pattern": pattern}
                )
    
    def _sanitize_whitespace(self, message: str) -> str:
        """
        Sanitize excessive whitespace from message.
        
        Args:
            message: The message to sanitize
            
        Returns:
            Message with normalized whitespace
        """
        # Replace multiple spaces with single space
        sanitized = re.sub(r'\s+', ' ', message)
        # Strip leading/trailing whitespace
        sanitized = sanitized.strip()
        return sanitized
    
    def validate_filename(self, filename: str) -> str:
        """
        Validate filename for security.
        
        Args:
            filename: The filename to validate
            
        Returns:
            The validated filename
            
        Raises:
            ValidationError: If filename is invalid
        """
        if not filename:
            raise ValidationError("Filename cannot be empty")
        
        # Only allow alphanumeric, underscore, hyphen, and .md extension
        if not re.match(r'^[a-z0-9_-]+\.md$', filename):
            raise ValidationError(
                f"Invalid filename: {filename}. Must be alphanumeric with .md extension",
                details={"filename": filename}
            )
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValidationError(
                "Filename cannot contain path separators",
                details={"filename": filename}
            )
        
        return filename

