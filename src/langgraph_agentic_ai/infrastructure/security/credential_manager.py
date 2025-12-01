"""Secure credential management using environment variables."""
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


class CredentialManager:
    """
    Manages API keys and credentials securely using environment variables.
    
    This class loads credentials from environment variables (typically from .env file)
    and provides secure access to them without exposing them in session state or logs.
    """
    
    def __init__(self, env_file: Optional[Path] = None):
        """
        Initialize the credential manager.
        
        Args:
            env_file: Optional path to .env file. If None, looks for .env in current directory.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Load from default .env file in project root
            load_dotenv()
    
    def get_groq_api_key(self) -> Optional[str]:
        """
        Get GROQ API key from environment.
        
        Returns:
            The API key if found, None otherwise.
        """
        return os.getenv("GROQ_API_KEY")
    
    def get_tavily_api_key(self) -> Optional[str]:
        """
        Get Tavily API key from environment.
        
        Returns:
            The API key if found, None otherwise.
        """
        return os.getenv("TAVILY_API_KEY")
    
    def validate_credentials(self, required_keys: list[str]) -> tuple[bool, list[str]]:
        """
        Validate that all required credentials are present.
        
        Args:
            required_keys: List of required credential keys (e.g., ['GROQ_API_KEY'])
        
        Returns:
            Tuple of (all_present: bool, missing_keys: list[str])
        """
        missing = []
        for key in required_keys:
            if not os.getenv(key):
                missing.append(key)
        
        return len(missing) == 0, missing
    
    def has_groq_api_key(self) -> bool:
        """Check if GROQ API key is available."""
        key = self.get_groq_api_key()
        return key is not None and len(key.strip()) > 0
    
    def has_tavily_api_key(self) -> bool:
        """Check if Tavily API key is available."""
        key = self.get_tavily_api_key()
        return key is not None and len(key.strip()) > 0

