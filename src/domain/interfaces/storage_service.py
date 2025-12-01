"""Storage service interface."""
from abc import ABC, abstractmethod
from pathlib import Path


class IStorageService(ABC):
    """
    Interface for storage services.
    
    Defines the contract for file/data storage operations.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if file exists
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_base_dir(self) -> Path:
        """
        Get the base directory for storage.
        
        Returns:
            Base directory path
        """
        pass

