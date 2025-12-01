"""Configuration loader for the application."""
from configparser import ConfigParser
from pathlib import Path
from typing import Optional
from ..domain.value_objects.app_config import AppConfig


class Config:
    """
    Configuration loader.
    
    Loads configuration from INI file and converts to AppConfig value object.
    """
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration loader.
        
        Args:
            config_file: Path to configuration file. If None, uses default.
        """
        if config_file is None:
            config_file = Path(__file__).parent / "default.ini"
        
        self.config = ConfigParser()
        self.config.read(config_file)
    
    def load_app_config(self) -> AppConfig:
        """
        Load application configuration.
        
        Returns:
            AppConfig value object
        """
        config_dict = {
            'PROJECT_NAME': self.config.get('DEFAULT', 'PROJECT_NAME'),
            'PAGE_TITLE': self.config.get('DEFAULT', 'PAGE_TITLE'),
            'LLM_OPTIONS': self.config.get('DEFAULT', 'LLM_OPTIONS'),
            'USECASE_OPTIONS': self.config.get('DEFAULT', 'USECASE_OPTIONS'),
            'GROQ_MODEL_OPTIONS': self.config.get('DEFAULT', 'GROQ_MODEL_OPTIONS'),
            'STORAGE_BASE_DIR': self.config.get('DEFAULT', 'STORAGE_BASE_DIR', fallback='./md'),
            'LOG_LEVEL': self.config.get('DEFAULT', 'LOG_LEVEL', fallback='INFO')
        }
        
        return AppConfig.from_ini_config(config_dict)
    
    # Legacy methods for backward compatibility
    def get(self, section: str, option: str):
        return self.config.get(section, option)

    def get_project_name(self):
        return self.get('DEFAULT', 'PROJECT_NAME')

    def get_page_title(self):
        return self.get('DEFAULT', 'PAGE_TITLE')

    def get_llm_options(self):
        llm_options = self.get('DEFAULT', 'LLM_OPTIONS')
        return [opt.strip() for opt in llm_options.split(",")]

    def get_usecase_options(self):
        usecase_options = self.get('DEFAULT', 'USECASE_OPTIONS')
        return [opt.strip() for opt in usecase_options.split(",")]

    def get_groq_model_options(self):
        groq_model_options = self.get('DEFAULT', 'GROQ_MODEL_OPTIONS')
        return [opt.strip() for opt in groq_model_options.split(",")]