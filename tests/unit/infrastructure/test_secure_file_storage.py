"""Tests for secure file storage."""
import pytest
from pathlib import Path
import tempfile
import shutil
from src.langgraph_agentic_ai.infrastructure.storage.secure_file_storage import SecureFileStorage
from src.langgraph_agentic_ai.domain.exceptions import (
    PathTraversalError,
    InvalidFilenameError,
    StorageError
)


class TestSecureFileStorage:
    """Test suite for SecureFileStorage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary directory for tests
        self.temp_dir = Path(tempfile.mkdtemp())
        self.storage = SecureFileStorage(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_save_file_success(self):
        """Test successful file save."""
        filename = "test.md"
        content = "Test content"
        
        file_path = self.storage.save_file(filename, content)
        
        assert file_path.exists()
        assert file_path.read_text() == content
    
    def test_save_file_invalid_filename_fails(self):
        """Test that invalid filename fails."""
        with pytest.raises(InvalidFilenameError):
            self.storage.save_file("invalid.txt", "content")
    
    def test_save_file_path_traversal_fails(self):
        """Test that path traversal attempts fail."""
        with pytest.raises(InvalidFilenameError):
            self.storage.save_file("../etc/passwd.md", "content")
    
    def test_read_file_success(self):
        """Test successful file read."""
        filename = "test.md"
        content = "Test content"
        
        self.storage.save_file(filename, content)
        read_content = self.storage.read_file(filename)
        
        assert read_content == content
    
    def test_read_file_not_found_fails(self):
        """Test that reading non-existent file fails."""
        with pytest.raises(StorageError, match="File not found"):
            self.storage.read_file("nonexistent.md")
    
    def test_file_exists_true(self):
        """Test checking if file exists when it does."""
        filename = "test.md"
        self.storage.save_file(filename, "content")
        
        assert self.storage.file_exists(filename) is True
    
    def test_file_exists_false(self):
        """Test checking if file exists when it doesn't."""
        assert self.storage.file_exists("nonexistent.md") is False
    
    def test_delete_file_success(self):
        """Test successful file deletion."""
        filename = "test.md"
        self.storage.save_file(filename, "content")
        
        result = self.storage.delete_file(filename)
        
        assert result is True
        assert not self.storage.file_exists(filename)
    
    def test_delete_file_not_found(self):
        """Test deleting non-existent file."""
        result = self.storage.delete_file("nonexistent.md")
        assert result is False
    
    def test_get_base_dir(self):
        """Test getting base directory."""
        assert self.storage.get_base_dir() == self.temp_dir

