"""Application configuration value object."""
from dataclasses import dataclass
from typing import List
from pathlib import Path
from ..constants import UseCase, LLMProvider, DEFAULT_STORAGE_DIR


@dataclass(frozen=True)
class AppConfig:
    """
    Immutable application configuration.
    
    Contains all application-level settings.
    """
    
    project_name: str
    page_title: str
    llm_options: List[LLMProvider]
    usecase_options: List[UseCase]
    groq_model_options: List[str]
    storage_base_dir: Path
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Validate configuration."""
        if not self.project_name:
            raise ValueError("project_name cannot be empty")
        
        if not self.page_title:
            raise ValueError("page_title cannot be empty")
        
        if not self.llm_options:
            raise ValueError("llm_options cannot be empty")
        
        if not self.usecase_options:
            raise ValueError("usecase_options cannot be empty")
        
        # Convert storage_base_dir to Path if it's a string
        if isinstance(self.storage_base_dir, str):
            object.__setattr__(self, 'storage_base_dir', Path(self.storage_base_dir))
    
    @classmethod
    def from_ini_config(cls, config_dict: dict) -> "AppConfig":
        """
        Create AppConfig from configuration dictionary.
        
        Args:
            config_dict: Dictionary with configuration values
            
        Returns:
            AppConfig instance
        """
        return cls(
            project_name=config_dict.get('PROJECT_NAME', 'Agentic Chatbot AI'),
            page_title=config_dict.get('PAGE_TITLE', 'Agentic Chatbot AI'),
            llm_options=[
                LLMProvider(opt.strip()) 
                for opt in config_dict.get('LLM_OPTIONS', 'groq').split(',')
            ],
            usecase_options=[
                UseCase(opt.strip()) 
                for opt in config_dict.get('USECASE_OPTIONS', 'Basic,Tools,News').split(',')
            ],
            groq_model_options=[
                opt.strip() 
                for opt in config_dict.get('GROQ_MODEL_OPTIONS', 'llama-3.1-8b-instant').split(',')
            ],
            storage_base_dir=Path(config_dict.get('STORAGE_BASE_DIR', DEFAULT_STORAGE_DIR)),
            log_level=config_dict.get('LOG_LEVEL', 'INFO')
        )

