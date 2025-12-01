"""Tools chat use case."""
from typing import Optional, List, Any
from ...domain.interfaces.llm_provider import ILLMProvider
from ...domain.entities.conversation import Conversation
from ...domain.validation.message_validator import MessageValidator
from ...domain.value_objects.model_config import ModelConfig
from ..dto.chat_request import ChatRequest
from ..dto.chat_response import ChatResponse


class ToolsChatUseCase:
    """
    Use case for chat with tool calling capability.
    
    Handles the business logic for processing chat messages with tools.
    """
    
    def __init__(
        self,
        llm_provider: ILLMProvider,
        tools: List[Any],
        validator: Optional[MessageValidator] = None
    ):
        """
        Initialize tools chat use case.
        
        Args:
            llm_provider: LLM provider for generating responses
            tools: Available tools for the LLM
            validator: Optional message validator
        """
        self._llm = llm_provider
        self._tools = tools
        self._validator = validator or MessageValidator()
        self._conversations = {}  # In-memory storage for now
    
    def execute(self, request: ChatRequest) -> ChatResponse:
        """
        Execute the tools chat use case.
        
        Args:
            request: Chat request DTO
            
        Returns:
            Chat response DTO
            
        Raises:
            ValidationError: If message validation fails
            LLMProviderError: If LLM generation fails
        """
        # Validate message
        validated_message = self._validator.validate_message(request.message)
        
        # Get or create conversation
        conversation = self._get_or_create_conversation(request.conversation_id)
        
        # Add user message
        conversation.add_user_message(validated_message)
        
        # Get model config
        config = request.model_config or ModelConfig.create_groq_config()
        
        # Generate response with tools
        response_message = self._llm.generate_with_tools(
            conversation.messages,
            self._tools,
            config
        )
        
        # Add assistant message to conversation
        conversation.add_message(response_message)
        
        # Create response DTO
        return ChatResponse(
            content=response_message.content,
            conversation_id=conversation.id,
            metadata={
                "model": config.model_name,
                "message_count": conversation.get_message_count(),
                "tools_available": len(self._tools)
            }
        )
    
    def _get_or_create_conversation(self, conversation_id: Optional[str]) -> Conversation:
        """
        Get existing conversation or create a new one.
        
        Args:
            conversation_id: Optional conversation ID
            
        Returns:
            Conversation instance
        """
        if conversation_id and conversation_id in self._conversations:
            return self._conversations[conversation_id]
        
        conversation = Conversation.create()
        self._conversations[conversation.id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation if found, None otherwise
        """
        return self._conversations.get(conversation_id)

