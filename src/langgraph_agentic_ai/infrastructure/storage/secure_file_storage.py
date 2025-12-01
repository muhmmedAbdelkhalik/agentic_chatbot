"""Secure file storage with path traversal prevention."""
import os
import re
from pathlib import Path
from typing import Optional
from ...domain.exceptions import (
    PathTraversalError,
    InvalidFilenameError,
    StorageError
)


class SecureFileStorage:
    """
    Provides secure file storage operations with path traversal prevention.
    
    All file operations are restricted to a base directory, and filenames
    are validated to prevent security issues.
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize secure file storage.
        
        Args:
            base_dir: Base directory for file operations. Defaults to ./md
        """
        if base_dir is None:
            base_dir = Path("./md")
        
        self.base_dir = Path(base_dir).resolve()
        
        # Create base directory if it doesn't exist
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, filename: str, content: str) -> Path:
        """
        Save content to a file securely.
        
        Args:
            filename: Name of the file (must be valid)
            content: Content to write
            
        Returns:
            Path to the saved file
            
        Raises:
            InvalidFilenameError: If filename is invalid
            PathTraversalError: If path traversal is attempted
            StorageError: If file operation fails
        """
        # Validate filename
        validated_filename = self._validate_filename(filename)
        
        # Create safe path
        file_path = (self.base_dir / validated_filename).resolve()
        
        # Prevent path traversal
        if not str(file_path).startswith(str(self.base_dir)):
            raise PathTraversalError(
                "Path traversal attempt detected",
                details={"filename": filename, "resolved_path": str(file_path)}
            )
        
        try:
            # Write file with proper permissions
            file_path.write_text(content, encoding='utf-8')
            
            # Set file permissions (owner read/write only)
            os.chmod(file_path, 0o600)
            
            return file_path
        except Exception as e:
            raise StorageError(
                f"Failed to save file: {str(e)}",
                details={"filename": filename, "error": str(e)}
            )
    
    def read_file(self, filename: str) -> str:
        """
        Read content from a file securely.
        
        Args:
            filename: Name of the file to read
            
        Returns:
            File content
            
        Raises:
            InvalidFilenameError: If filename is invalid
            PathTraversalError: If path traversal is attempted
            StorageError: If file doesn't exist or read fails
        """
        # Validate filename
        validated_filename = self._validate_filename(filename)
        
        # Create safe path
        file_path = (self.base_dir / validated_filename).resolve()
        
        # Prevent path traversal
        if not str(file_path).startswith(str(self.base_dir)):
            raise PathTraversalError(
                "Path traversal attempt detected",
                details={"filename": filename}
            )
        
        try:
            if not file_path.exists():
                raise StorageError(
                    f"File not found: {filename}",
                    details={"filename": filename}
                )
            
            return file_path.read_text(encoding='utf-8')
        except StorageError:
            raise
        except Exception as e:
            raise StorageError(
                f"Failed to read file: {str(e)}",
                details={"filename": filename, "error": str(e)}
            )
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            validated_filename = self._validate_filename(filename)
            file_path = (self.base_dir / validated_filename).resolve()
            
            if not str(file_path).startswith(str(self.base_dir)):
                return False
            
            return file_path.exists()
        except (InvalidFilenameError, PathTraversalError):
            return False
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file securely.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if file was deleted, False if it didn't exist
            
        Raises:
            InvalidFilenameError: If filename is invalid
            PathTraversalError: If path traversal is attempted
            StorageError: If deletion fails
        """
        validated_filename = self._validate_filename(filename)
        file_path = (self.base_dir / validated_filename).resolve()
        
        if not str(file_path).startswith(str(self.base_dir)):
            raise PathTraversalError(
                "Path traversal attempt detected",
                details={"filename": filename}
            )
        
        try:
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            raise StorageError(
                f"Failed to delete file: {str(e)}",
                details={"filename": filename, "error": str(e)}
            )
    
    def _validate_filename(self, filename: str) -> str:
        """
        Validate filename for security.
        
        Args:
            filename: The filename to validate
            
        Returns:
            The validated filename
            
        Raises:
            InvalidFilenameError: If filename is invalid
        """
        if not filename:
            raise InvalidFilenameError("Filename cannot be empty")
        
        # Only allow alphanumeric, underscore, hyphen, and .md extension
        if not re.match(r'^[a-z0-9_-]+\.md$', filename, re.IGNORECASE):
            raise InvalidFilenameError(
                f"Invalid filename: {filename}. Must be alphanumeric with .md extension",
                details={"filename": filename}
            )
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            raise InvalidFilenameError(
                "Filename cannot contain path separators",
                details={"filename": filename}
            )
        
        return filename
    
    def get_base_dir(self) -> Path:
        """Get the base directory for storage."""
        return self.base_dir

