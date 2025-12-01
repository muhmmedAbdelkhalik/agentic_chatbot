"""Configuration presenter for Streamlit."""
import streamlit as st
from typing import Optional, Dict, Any
from ...domain.value_objects.app_config import AppConfig
from ...domain.value_objects.model_config import ModelConfig
from ...domain.constants import UseCase, NewsFrequency, LLMProvider
from ...infrastructure.security.credential_manager import CredentialManager


class ConfigPresenter:
    """
    Presents configuration UI in Streamlit.
    
    Handles user input for model selection, use case, and other settings.
    """
    
    def __init__(self, app_config: AppConfig, credential_manager: CredentialManager):
        """
        Initialize config presenter.
        
        Args:
            app_config: Application configuration
            credential_manager: Credential manager for API keys
        """
        self._app_config = app_config
        self._credential_manager = credential_manager
    
    def render(self) -> Optional[Dict[str, Any]]:
        """
        Render configuration UI.
        
        Returns:
            Dictionary with user selections, or None if incomplete
        """
        # Set page config
        st.set_page_config(page_title=self._app_config.page_title)
        st.header(self._app_config.page_title)
        
        # Initialize session state
        if 'timeframe' not in st.session_state:
            st.session_state.timeframe = ''
        if 'isFetchButtonClicked' not in st.session_state:
            st.session_state.isFetchButtonClicked = False
        
        user_config = {}
        
        with st.sidebar:
            # LLM selection
            llm_options = [provider.value for provider in self._app_config.llm_options]
            selected_llm = st.selectbox("Select LLM", llm_options)
            user_config["selected_llm"] = LLMProvider(selected_llm)
            
            # Model selection (currently only Groq supported)
            if user_config["selected_llm"] == LLMProvider.GROQ:
                selected_model = st.selectbox(
                    "Select Model",
                    self._app_config.groq_model_options
                )
                user_config["selected_model"] = selected_model
                
                # Check for API key
                if not self._credential_manager.has_groq_api_key():
                    st.warning(
                        "⚠️ GROQ API key not found in environment. "
                        "Please set GROQ_API_KEY in your .env file. "
                        "Get your key at: https://console.groq.com/keys"
                    )
                    return None
                else:
                    st.success("✅ GROQ API key loaded from environment")
            
            # Use case selection
            usecase_options = [uc.value for uc in self._app_config.usecase_options]
            selected_usecase = st.selectbox("Select Use Case", usecase_options)
            user_config["selected_usecase"] = UseCase(selected_usecase)
            
            # Tavily API key check for Tools and News
            if user_config["selected_usecase"] in [UseCase.TOOLS, UseCase.NEWS]:
                if not self._credential_manager.has_tavily_api_key():
                    st.warning(
                        "⚠️ Tavily API key not found in environment. "
                        "Please set TAVILY_API_KEY in your .env file. "
                        "Get your key at: https://www.tavily.com"
                    )
                    return None
                else:
                    st.success("✅ Tavily API key loaded from environment")
            
            # News-specific configuration
            if user_config["selected_usecase"] == UseCase.NEWS:
                st.subheader("News Configuration")
                time_frame = st.selectbox(
                    "Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0
                )
                
                if st.button("Load News", use_container_width=True):
                    st.session_state.isFetchButtonClicked = True
                    st.session_state.timeframe = time_frame
                
                user_config["timeframe"] = time_frame
        
        return user_config

