"""LLM provider interface."""
from abc import ABC, abstractmethod
from typing import List, Any
from ..entities.message import Message
from ..value_objects.model_config import ModelConfig


class ILLMProvider(ABC):
    """
    Interface for LLM providers.
    
    This defines the contract that all LLM adapters must implement,
    enabling dependency inversion and easy swapping of providers.
    """
    
    @abstractmethod
    def generate(self, messages: List[Message], config: ModelConfig) -> Message:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of conversation messages
            config: Model configuration
            
        Returns:
            Generated assistant message
            
        Raises:
            LLMProviderError: If generation fails
        """
        pass
    
    @abstractmethod
    def generate_with_tools(
        self,
        messages: List[Message],
        tools: List[Any],
        config: ModelConfig
    ) -> Message:
        """
        Generate a response with tool calling capability.
        
        Args:
            messages: List of conversation messages
            tools: Available tools
            config: Model configuration
            
        Returns:
            Generated assistant message (may include tool calls)
            
        Raises:
            LLMProviderError: If generation fails
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the name of the current model.
        
        Returns:
            Model name
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available and configured.
        
        Returns:
            True if provider is ready to use
        """
        pass

