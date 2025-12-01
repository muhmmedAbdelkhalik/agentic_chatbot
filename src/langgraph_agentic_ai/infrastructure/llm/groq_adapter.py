"""Groq LLM adapter implementing ILLMProvider interface."""
from typing import List, Any, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from ...domain.interfaces.llm_provider import ILLMProvider
from ...domain.entities.message import Message, MessageRole
from ...domain.value_objects.model_config import ModelConfig
from ...domain.exceptions import LLMProviderError, MissingCredentialError
from ..security.credential_manager import CredentialManager
from ..logging.security_audit import SecurityAuditLogger
import time


class GroqLLMAdapter(ILLMProvider):
    """
    Adapter for Groq LLM provider.
    
    Implements the ILLMProvider interface using Groq's API.
    """
    
    def __init__(
        self,
        credential_manager: CredentialManager,
        config: ModelConfig,
        audit_logger: Optional[SecurityAuditLogger] = None
    ):
        """
        Initialize Groq adapter.
        
        Args:
            credential_manager: Manager for API credentials
            config: Model configuration
            audit_logger: Optional security audit logger
            
        Raises:
            MissingCredentialError: If Groq API key is not available
        """
        self._credential_manager = credential_manager
        self._config = config
        self._audit_logger = audit_logger or SecurityAuditLogger()
        
        # Get API key
        api_key = self._credential_manager.get_groq_api_key()
        if not api_key:
            self._audit_logger.log_credential_access("groq", success=False)
            raise MissingCredentialError(
                "Groq API key not found. Please set GROQ_API_KEY environment variable."
            )
        
        self._audit_logger.log_credential_access("groq", success=True)
        
        # Initialize Groq client
        try:
            self._client = ChatGroq(
                api_key=api_key,
                model=config.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout,
                max_retries=config.max_retries
            )
        except Exception as e:
            raise LLMProviderError(
                f"Failed to initialize Groq client: {str(e)}",
                details={"error": str(e)}
            )
    
    def generate(self, messages: List[Message], config: ModelConfig) -> Message:
        """
        Generate a response from Groq.
        
        Args:
            messages: List of conversation messages
            config: Model configuration (overrides default)
            
        Returns:
            Generated assistant message
            
        Raises:
            LLMProviderError: If generation fails
        """
        start_time = time.time()
        
        try:
            # Convert domain messages to LangChain format
            lc_messages = self._convert_to_langchain_messages(messages)
            
            # Generate response
            response = self._client.invoke(lc_messages)
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Log successful request
            self._audit_logger.log_llm_request(
                model=config.model_name,
                success=True,
                latency_ms=latency_ms
            )
            
            # Convert response to domain message
            # Handle empty content
            content = response.content if response.content else "[Empty response]"
            
            return Message.assistant_message(
                content=content,
                metadata={"model": config.model_name, "latency_ms": latency_ms}
            )
            
        except Exception as e:
            # Log failed request
            self._audit_logger.log_llm_request(
                model=config.model_name,
                success=False,
                error=str(e)
            )
            
            raise LLMProviderError(
                f"Failed to generate response from Groq: {str(e)}",
                details={"error": str(e), "model": config.model_name}
            )
    
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
            Generated assistant message
            
        Raises:
            LLMProviderError: If generation fails
        """
        start_time = time.time()
        
        try:
            # Bind tools to the model
            llm_with_tools = self._client.bind_tools(tools)
            
            # Convert domain messages to LangChain format
            lc_messages = self._convert_to_langchain_messages(messages)
            
            # Generate response
            response = llm_with_tools.invoke(lc_messages)
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Log successful request
            self._audit_logger.log_llm_request(
                model=config.model_name,
                success=True,
                latency_ms=latency_ms
            )
            
            # Convert response to domain message
            # Handle empty content when tool calls are present
            content = response.content if hasattr(response, 'content') and response.content else ""
            
            # If content is empty and there are tool calls, use a placeholder
            tool_calls = getattr(response, 'tool_calls', None)
            if not content and tool_calls:
                content = "[Tool calls in progress]"
            elif not content:
                content = "[Empty response]"
            
            return Message.assistant_message(
                content=content,
                metadata={
                    "model": config.model_name,
                    "latency_ms": latency_ms,
                    "tool_calls": tool_calls
                }
            )
            
        except Exception as e:
            # Log failed request
            self._audit_logger.log_llm_request(
                model=config.model_name,
                success=False,
                error=str(e)
            )
            
            raise LLMProviderError(
                f"Failed to generate response with tools from Groq: {str(e)}",
                details={"error": str(e), "model": config.model_name}
            )
    
    def get_model_name(self) -> str:
        """Get the name of the current model."""
        return self._config.model_name
    
    def is_available(self) -> bool:
        """Check if the provider is available."""
        return self._credential_manager.has_groq_api_key()
    
    def get_raw_client(self):
        """
        Get the raw LangChain client for backward compatibility.
        
        Returns:
            ChatGroq client
        """
        return self._client
    
    def _convert_to_langchain_messages(self, messages: List[Message]) -> List:
        """
        Convert domain messages to LangChain format.
        
        Args:
            messages: Domain messages
            
        Returns:
            LangChain messages
        """
        lc_messages = []
        
        for msg in messages:
            if msg.role == MessageRole.USER:
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.ASSISTANT:
                lc_messages.append(AIMessage(content=msg.content))
            elif msg.role == MessageRole.SYSTEM:
                lc_messages.append(SystemMessage(content=msg.content))
        
        return lc_messages

