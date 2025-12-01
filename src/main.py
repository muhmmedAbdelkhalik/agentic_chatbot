"""
Main entry point for the LangGraph Agentic AI application.

This module initializes the application using clean architecture principles
with dependency injection and proper separation of concerns.
"""
import streamlit as st
from src.config.config import Config
from src.infrastructure.di.container import DIContainer
from src.presentation.streamlit.config_presenter import ConfigPresenter
from src.presentation.streamlit.chat_presenter import ChatPresenter
from src.domain.constants import UseCase
from src.domain.value_objects.model_config import ModelConfig
from src.domain.exceptions import (
    MissingCredentialError,
    ConfigurationError
)
from src.tools.search_tool import get_tools
from src.graph.graph_builder import GraphBuilder
from langchain_core.messages import HumanMessage


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
            # Tools use case uses graph-based approach with inline display
            llm_provider = container.get_llm_provider(model_config)
            raw_llm = llm_provider.get_raw_client()
            
            user_message = st.chat_input("Enter your message:", key="tools_chat_input")
            if user_message:
                # Build and execute graph
                graph_builder = GraphBuilder(raw_llm)
                graph = graph_builder.setup_graph("Tools")
                
                # Display user message
                with st.chat_message("user"):
                    st.write(user_message)
                
                # Execute graph and display results
                with st.spinner("Thinking..."):
                    events = graph.stream(
                        {"messages": [HumanMessage(content=user_message)]},
                        stream_mode="values"
                    )
                    
                    # Get final state
                    final_state = None
                    for event in events:
                        final_state = event
                    
                    if final_state and "messages" in final_state:
                        # Display assistant response
                        with st.chat_message("assistant"):
                            for message in final_state["messages"]:
                                if hasattr(message, 'content') and message.content:
                                    if not isinstance(message, HumanMessage):
                                        st.write(message.content)
        
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
