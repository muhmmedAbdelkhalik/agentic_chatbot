"""Custom exception hierarchy for domain errors."""


class DomainException(Exception):
    """Base exception for all domain-related errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(DomainException):
    """Raised when input validation fails."""
    pass


class PromptInjectionError(ValidationError):
    """Raised when potential prompt injection is detected."""
    pass


class MessageTooLongError(ValidationError):
    """Raised when message exceeds maximum length."""
    pass


class InvalidFrequencyError(ValidationError):
    """Raised when an invalid news frequency is provided."""
    pass


class CredentialError(DomainException):
    """Raised when credential-related issues occur."""
    pass


class MissingCredentialError(CredentialError):
    """Raised when required credentials are missing."""
    pass


class LLMProviderError(DomainException):
    """Raised when LLM provider fails."""
    pass


class StorageError(DomainException):
    """Raised when storage operations fail."""
    pass


class PathTraversalError(StorageError):
    """Raised when path traversal attempt is detected."""
    pass


class InvalidFilenameError(StorageError):
    """Raised when filename is invalid."""
    pass


class UseCaseNotFoundError(DomainException):
    """Raised when requested use case doesn't exist."""
    pass


class ConfigurationError(DomainException):
    """Raised when configuration is invalid."""
    pass


class SearchServiceError(DomainException):
    """Raised when search service fails."""
    pass

