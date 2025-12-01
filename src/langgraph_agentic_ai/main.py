"""
Main entry point for the LangGraph Agentic AI application.

This module initializes the application using clean architecture principles
with dependency injection and proper separation of concerns.
"""
import streamlit as st
from src.langgraph_agentic_ai.config.config import Config
from src.langgraph_agentic_ai.infrastructure.di.container import DIContainer
from src.langgraph_agentic_ai.presentation.streamlit.config_presenter import ConfigPresenter
from src.langgraph_agentic_ai.presentation.streamlit.chat_presenter import ChatPresenter
from src.langgraph_agentic_ai.domain.constants import UseCase
from src.langgraph_agentic_ai.domain.value_objects.model_config import ModelConfig
from src.langgraph_agentic_ai.domain.exceptions import (
    MissingCredentialError,
    ConfigurationError
)
from src.langgraph_agentic_ai.tools.search_tool import get_tools
from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder
from src.langgraph_agentic_ai.ui.streamlit.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    
    This function:
    1. Loads configuration
    2. Initializes DI container
    3. Presents configuration UI
    4. Creates appropriate use case based on selection
    5. Renders chat interface
    
    Uses clean architecture with dependency injection for maintainability
    and testability.
    """
    try:
        # Load configuration
        config_loader = Config()
        app_config = config_loader.load_app_config()
        
        # Initialize DI container
        container = DIContainer(app_config)
        
        # Get credential manager
        credential_manager = container.get_credential_manager()
        
        # Render configuration UI
        config_presenter = ConfigPresenter(app_config, credential_manager)
        user_config = config_presenter.render()
        
        # Check if configuration is complete
        if not user_config:
            return
        
        # Get user selections
        selected_usecase = user_config.get("selected_usecase")
        selected_model = user_config.get("selected_model")
        
        # Create model configuration
        model_config = ModelConfig.create_groq_config(model_name=selected_model)
        
        # Create appropriate use case and presenter
        if selected_usecase == UseCase.BASIC:
            chat_use_case = container.get_chat_use_case(model_config)
            presenter = ChatPresenter(
                use_case=selected_usecase,
                chat_use_case=chat_use_case
            )
            presenter.render()
        
        elif selected_usecase == UseCase.TOOLS:
            # Tools use case still uses the old graph-based approach
            # TODO: Migrate to new architecture in Phase 2
            llm_provider = container.get_llm_provider(model_config)
            raw_llm = llm_provider.get_raw_client()
            
            user_message = st.chat_input("Enter your message:", key="tools_chat_input")
            if user_message:
                graph_builder = GraphBuilder(raw_llm)
                graph = graph_builder.setup_graph("Tools")
                DisplayResultStreamlit("Tools", graph, user_message).display_result_on_ui()
        
        elif selected_usecase == UseCase.NEWS:
            news_use_case = container.get_news_generation_use_case(model_config)
            presenter = ChatPresenter(
                use_case=selected_usecase,
                news_use_case=news_use_case
            )
            presenter.render()
        
        else:
            st.error(f"Unknown use case: {selected_usecase}")
    
    except MissingCredentialError as e:
        st.error(f"❌ Credential Error: {e.message}")
        st.info("Please check your .env file and ensure all required API keys are set.")
    
    except ConfigurationError as e:
        st.error(f"❌ Configuration Error: {e.message}")
        st.info("Please check your configuration file.")
    
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        st.info("An unexpected error occurred. Please check the logs for details.")
