"""Dependency injection container."""
from typing import Dict, Any, Optional
from pathlib import Path
from ...domain.value_objects.model_config import ModelConfig
from ...domain.value_objects.app_config import AppConfig
from ...domain.interfaces.llm_provider import ILLMProvider
from ...domain.interfaces.storage_service import IStorageService
from ...domain.interfaces.search_service import ISearchService
from ..security.credential_manager import CredentialManager
from ..logging.security_audit import SecurityAuditLogger
from ..logging.config import setup_logging
from ..llm.groq_adapter import GroqLLMAdapter
from ..storage.file_storage_adapter import FileStorageAdapter
from ..search.tavily_adapter import TavilySearchAdapter
from ...application.use_cases.chat_use_case import ChatUseCase
from ...application.use_cases.tools_chat_use_case import ToolsChatUseCase
from ...application.use_cases.news_generation_use_case import NewsGenerationUseCase


class DIContainer:
    """
    Dependency Injection Container.
    
    Manages the creation and lifecycle of application dependencies.
    Implements singleton pattern for shared services.
    """
    
    def __init__(self, app_config: AppConfig):
        """
        Initialize DI container.
        
        Args:
            app_config: Application configuration
        """
        self._config = app_config
        self._singletons: Dict[str, Any] = {}
        
        # Initialize logging
        setup_logging(
            log_level=app_config.log_level,
            log_file=Path("logs/app.log"),
            log_to_console=True
        )
    
    def _get_singleton(self, key: str, factory):
        """
        Get or create a singleton instance.
        
        Args:
            key: Singleton key
            factory: Factory function to create the instance
            
        Returns:
            Singleton instance
        """
        if key not in self._singletons:
            self._singletons[key] = factory()
        return self._singletons[key]
    
    def get_credential_manager(self) -> CredentialManager:
        """Get credential manager singleton."""
        return self._get_singleton(
            'credential_manager',
            lambda: CredentialManager()
        )
    
    def get_security_audit_logger(self) -> SecurityAuditLogger:
        """Get security audit logger singleton."""
        return self._get_singleton(
            'security_audit_logger',
            lambda: SecurityAuditLogger()
        )
    
    def get_llm_provider(self, model_config: Optional[ModelConfig] = None) -> ILLMProvider:
        """
        Get LLM provider.
        
        Args:
            model_config: Optional model configuration
            
        Returns:
            LLM provider instance
        """
        if model_config is None:
            model_config = ModelConfig.create_groq_config()
        
        # Create new instance with specific config (not singleton)
        return GroqLLMAdapter(
            credential_manager=self.get_credential_manager(),
            config=model_config,
            audit_logger=self.get_security_audit_logger()
        )
    
    def get_storage_service(self) -> IStorageService:
        """Get storage service singleton."""
        return self._get_singleton(
            'storage_service',
            lambda: FileStorageAdapter(
                base_dir=self._config.storage_base_dir,
                audit_logger=self.get_security_audit_logger()
            )
        )
    
    def get_search_service(self) -> ISearchService:
        """Get search service singleton."""
        return self._get_singleton(
            'search_service',
            lambda: TavilySearchAdapter(
                credential_manager=self.get_credential_manager(),
                audit_logger=self.get_security_audit_logger()
            )
        )
    
    def get_chat_use_case(self, model_config: Optional[ModelConfig] = None) -> ChatUseCase:
        """
        Get chat use case.
        
        Args:
            model_config: Optional model configuration
            
        Returns:
            ChatUseCase instance
        """
        return ChatUseCase(
            llm_provider=self.get_llm_provider(model_config)
        )
    
    def get_tools_chat_use_case(
        self,
        tools: list,
        model_config: Optional[ModelConfig] = None
    ) -> ToolsChatUseCase:
        """
        Get tools chat use case.
        
        Args:
            tools: Available tools
            model_config: Optional model configuration
            
        Returns:
            ToolsChatUseCase instance
        """
        return ToolsChatUseCase(
            llm_provider=self.get_llm_provider(model_config),
            tools=tools
        )
    
    def get_news_generation_use_case(
        self,
        model_config: Optional[ModelConfig] = None
    ) -> NewsGenerationUseCase:
        """
        Get news generation use case.
        
        Args:
            model_config: Optional model configuration
            
        Returns:
            NewsGenerationUseCase instance
        """
        return NewsGenerationUseCase(
            llm_provider=self.get_llm_provider(model_config),
            search_service=self.get_search_service(),
            storage_service=self.get_storage_service()
        )
    
    def get_app_config(self) -> AppConfig:
        """Get application configuration."""
        return self._config
    
    def clear_singletons(self):
        """Clear all singleton instances (useful for testing)."""
        self._singletons.clear()

