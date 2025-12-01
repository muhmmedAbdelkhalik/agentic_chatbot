"""File storage adapter implementing IStorageService interface."""
from pathlib import Path
from typing import Optional
from ...domain.interfaces.storage_service import IStorageService
from .secure_file_storage import SecureFileStorage
from ..logging.security_audit import SecurityAuditLogger


class FileStorageAdapter(IStorageService):
    """
    Adapter for file storage service.
    
    Implements the IStorageService interface using secure file operations.
    """
    
    def __init__(
        self,
        base_dir: Optional[Path] = None,
        audit_logger: Optional[SecurityAuditLogger] = None
    ):
        """
        Initialize file storage adapter.
        
        Args:
            base_dir: Base directory for file operations
            audit_logger: Optional security audit logger
        """
        self._storage = SecureFileStorage(base_dir)
        self._audit_logger = audit_logger or SecurityAuditLogger()
    
    def save_file(self, filename: str, content: str) -> Path:
        """
        Save content to a file.
        
        Args:
            filename: Name of the file
            content: Content to save
            
        Returns:
            Path to the saved file
            
        Raises:
            StorageError: If save operation fails
        """
        try:
            path = self._storage.save_file(filename, content)
            self._audit_logger.log_file_operation(
                operation="write",
                filename=filename,
                success=True
            )
            return path
        except Exception as e:
            self._audit_logger.log_file_operation(
                operation="write",
                filename=filename,
                success=False,
                error=str(e)
            )
            raise
    
    def read_file(self, filename: str) -> str:
        """
        Read content from a file.
        
        Args:
            filename: Name of the file
            
        Returns:
            File content
            
        Raises:
            StorageError: If read operation fails
        """
        try:
            content = self._storage.read_file(filename)
            self._audit_logger.log_file_operation(
                operation="read",
                filename=filename,
                success=True
            )
            return content
        except Exception as e:
            self._audit_logger.log_file_operation(
                operation="read",
                filename=filename,
                success=False,
                error=str(e)
            )
            raise
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if file exists
        """
        return self._storage.file_exists(filename)
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if file was deleted
            
        Raises:
            StorageError: If delete operation fails
        """
        try:
            result = self._storage.delete_file(filename)
            self._audit_logger.log_file_operation(
                operation="delete",
                filename=filename,
                success=True
            )
            return result
        except Exception as e:
            self._audit_logger.log_file_operation(
                operation="delete",
                filename=filename,
                success=False,
                error=str(e)
            )
            raise
    
    def get_base_dir(self) -> Path:
        """Get the base directory for storage."""
        return self._storage.get_base_dir()

