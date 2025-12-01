"""Security audit logging."""
import logging
from datetime import datetime
from typing import Any, Optional
from .config import get_logger


class SecurityAuditLogger:
    """
    Logs security-related events for audit purposes.
    
    This logger tracks:
    - API key access attempts
    - Validation failures
    - File operations
    - Suspicious activity
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize security audit logger.
        
        Args:
            logger: Optional logger instance. If None, creates a new one.
        """
        self._logger = logger or get_logger("security_audit")
    
    def log_credential_access(
        self,
        service: str,
        success: bool,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log API key/credential access attempt.
        
        Args:
            service: Service name (e.g., 'groq', 'tavily')
            success: Whether access was successful
            user_id: Optional user identifier
        """
        self._logger.info(
            "Credential access",
            extra={
                "event": "credential_access",
                "service": service,
                "success": success,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_validation_failure(
        self,
        validation_type: str,
        reason: str,
        details: Optional[dict] = None
    ) -> None:
        """
        Log input validation failure.
        
        Args:
            validation_type: Type of validation (e.g., 'message', 'filename')
            reason: Reason for failure
            details: Optional additional details
        """
        self._logger.warning(
            f"Validation failure: {validation_type} - {reason}",
            extra={
                "event": "validation_failure",
                "validation_type": validation_type,
                "reason": reason,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_file_operation(
        self,
        operation: str,
        filename: str,
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """
        Log file operation.
        
        Args:
            operation: Operation type (e.g., 'read', 'write', 'delete')
            filename: Name of the file
            success: Whether operation was successful
            error: Optional error message
        """
        log_level = logging.INFO if success else logging.ERROR
        self._logger.log(
            log_level,
            f"File operation: {operation} - {filename}",
            extra={
                "event": "file_operation",
                "operation": operation,
                "target_file": filename,  # Changed from 'filename' to avoid conflict
                "success": success,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_suspicious_activity(
        self,
        activity: str,
        details: Any,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log suspicious activity.
        
        Args:
            activity: Description of suspicious activity
            details: Details about the activity
            user_id: Optional user identifier
        """
        self._logger.warning(
            f"Suspicious activity: {activity}",
            extra={
                "event": "suspicious_activity",
                "activity": activity,
                "details": details,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_prompt_injection_attempt(
        self,
        message: str,
        pattern: str,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log potential prompt injection attempt.
        
        Args:
            message: The message that triggered detection
            pattern: The pattern that was matched
            user_id: Optional user identifier
        """
        self._logger.warning(
            "Prompt injection attempt detected",
            extra={
                "event": "prompt_injection_attempt",
                "message_preview": message[:100],  # Only log preview
                "pattern": pattern,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_path_traversal_attempt(
        self,
        filename: str,
        resolved_path: str,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log path traversal attempt.
        
        Args:
            filename: The filename that was attempted
            resolved_path: The resolved path that was blocked
            user_id: Optional user identifier
        """
        self._logger.warning(
            "Path traversal attempt detected",
            extra={
                "event": "path_traversal_attempt",
                "attempted_filename": filename,  # Changed from 'filename' to avoid conflict
                "resolved_path": resolved_path,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_llm_request(
        self,
        model: str,
        success: bool,
        latency_ms: Optional[float] = None,
        error: Optional[str] = None
    ) -> None:
        """
        Log LLM API request.
        
        Args:
            model: Model name
            success: Whether request was successful
            latency_ms: Request latency in milliseconds
            error: Optional error message
        """
        log_level = logging.INFO if success else logging.ERROR
        self._logger.log(
            log_level,
            f"LLM request: {model}",
            extra={
                "event": "llm_request",
                "model": model,
                "success": success,
                "latency_ms": latency_ms,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

