"""Basic chat use case."""
from typing import Optional
from ...domain.interfaces.llm_provider import ILLMProvider
from ...domain.entities.conversation import Conversation
from ...domain.entities.message import Message
from ...domain.validation.message_validator import MessageValidator
from ...domain.value_objects.model_config import ModelConfig
from ..dto.chat_request import ChatRequest
from ..dto.chat_response import ChatResponse


class ChatUseCase:
    """
    Use case for basic chat functionality.
    
    Handles the business logic for processing chat messages without tools.
    """
    
    def __init__(
        self,
        llm_provider: ILLMProvider,
        validator: Optional[MessageValidator] = None
    ):
        """
        Initialize chat use case.
        
        Args:
            llm_provider: LLM provider for generating responses
            validator: Optional message validator
        """
        self._llm = llm_provider
        self._validator = validator or MessageValidator()
        self._conversations = {}  # In-memory storage for now
    
    def execute(self, request: ChatRequest) -> ChatResponse:
        """
        Execute the chat use case.
        
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
        
        # Generate response
        response_message = self._llm.generate(conversation.messages, config)
        
        # Add assistant message to conversation
        conversation.add_message(response_message)
        
        # Create response DTO
        return ChatResponse(
            content=response_message.content,
            conversation_id=conversation.id,
            metadata={
                "model": config.model_name,
                "message_count": conversation.get_message_count()
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
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """
        Clear a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            True if conversation was cleared
        """
        if conversation_id in self._conversations:
            self._conversations[conversation_id].clear_messages()
            return True
        return False

