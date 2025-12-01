"""Tests for credential manager."""
import pytest
import os
from unittest.mock import patch
from src.infrastructure.security.credential_manager import CredentialManager


class TestCredentialManager:
    """Test suite for CredentialManager."""
    
    def test_get_groq_api_key_success(self):
        """Test getting Groq API key when it exists."""
        with patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'}):
            manager = CredentialManager()
            assert manager.get_groq_api_key() == 'test_key'
    
    def test_get_groq_api_key_missing(self):
        """Test getting Groq API key when it doesn't exist."""
        with patch.dict(os.environ, {}, clear=True):
            manager = CredentialManager()
            assert manager.get_groq_api_key() is None
    
    def test_get_tavily_api_key_success(self):
        """Test getting Tavily API key when it exists."""
        with patch.dict(os.environ, {'TAVILY_API_KEY': 'test_key'}):
            manager = CredentialManager()
            assert manager.get_tavily_api_key() == 'test_key'
    
    def test_has_groq_api_key_true(self):
        """Test checking for Groq API key when it exists."""
        with patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'}):
            manager = CredentialManager()
            assert manager.has_groq_api_key() is True
    
    def test_has_groq_api_key_false(self):
        """Test checking for Groq API key when it doesn't exist."""
        with patch.dict(os.environ, {}, clear=True):
            manager = CredentialManager()
            assert manager.has_groq_api_key() is False
    
    def test_validate_credentials_all_present(self):
        """Test validating credentials when all are present."""
        with patch.dict(os.environ, {'GROQ_API_KEY': 'key1', 'TAVILY_API_KEY': 'key2'}):
            manager = CredentialManager()
            all_present, missing = manager.validate_credentials(['GROQ_API_KEY', 'TAVILY_API_KEY'])
            assert all_present is True
            assert missing == []
    
    def test_validate_credentials_some_missing(self):
        """Test validating credentials when some are missing."""
        with patch.dict(os.environ, {'GROQ_API_KEY': 'key1'}, clear=True):
            manager = CredentialManager()
            all_present, missing = manager.validate_credentials(['GROQ_API_KEY', 'TAVILY_API_KEY'])
            assert all_present is False
            assert 'TAVILY_API_KEY' in missing

