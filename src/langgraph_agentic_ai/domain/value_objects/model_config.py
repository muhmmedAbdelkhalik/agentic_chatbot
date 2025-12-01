"""Model configuration value object."""
from dataclasses import dataclass
from typing import Optional
from ..constants import LLMProvider, DEFAULT_GROQ_MODEL


@dataclass(frozen=True)
class ModelConfig:
    """
    Immutable configuration for LLM model.
    
    Contains all necessary information to initialize and use an LLM.
    """
    
    provider: LLMProvider
    model_name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: int = 30
    max_retries: int = 3
    
    def __post_init__(self):
        """Validate configuration."""
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
    
    @classmethod
    def create_groq_config(
        cls,
        model_name: str = DEFAULT_GROQ_MODEL,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> "ModelConfig":
        """
        Create configuration for Groq provider.
        
        Args:
            model_name: Name of the Groq model
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            ModelConfig instance
        """
        return cls(
            provider=LLMProvider.GROQ,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    @classmethod
    def create_openai_config(
        cls,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> "ModelConfig":
        """
        Create configuration for OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            ModelConfig instance
        """
        return cls(
            provider=LLMProvider.OPENAI,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

