"""Chat presenter for Streamlit."""
import streamlit as st
from typing import Optional
from ...application.use_cases.chat_use_case import ChatUseCase
from ...application.use_cases.tools_chat_use_case import ToolsChatUseCase
from ...application.use_cases.news_generation_use_case import NewsGenerationUseCase
from ...application.dto.chat_request import ChatRequest
from ...application.dto.news_request import NewsRequest
from ...domain.constants import UseCase, NewsFrequency
from ...domain.exceptions import (
    ValidationError,
    LLMProviderError,
    SearchServiceError,
    StorageError
)


class ChatPresenter:
    """
    Presents chat interface in Streamlit.
    
    Handles message display and user interaction.
    """
    
    def __init__(
        self,
        use_case: UseCase,
        chat_use_case: Optional[ChatUseCase] = None,
        tools_chat_use_case: Optional[ToolsChatUseCase] = None,
        news_use_case: Optional[NewsGenerationUseCase] = None
    ):
        """
        Initialize chat presenter.
        
        Args:
            use_case: Selected use case
            chat_use_case: Basic chat use case
            tools_chat_use_case: Tools chat use case
            news_use_case: News generation use case
        """
        self._use_case = use_case
        self._chat_use_case = chat_use_case
        self._tools_chat_use_case = tools_chat_use_case
        self._news_use_case = news_use_case
    
    def render(self):
        """
        Render chat interface.
        """
        if self._use_case == UseCase.NEWS:
            self._render_news()
        else:
            self._render_chat()
    
    def _render_chat(self):
        """Render chat interface for Basic and Tools use cases."""
        user_message = st.chat_input("Enter your message:", key=f"chat_input_{self._use_case.value}")
        
        if user_message:
            try:
                # Display user message
                with st.chat_message("user"):
                    st.write(user_message)
                
                # Process message
                with st.spinner("Thinking..."):
                    request = ChatRequest(message=user_message)
                    
                    if self._use_case == UseCase.BASIC:
                        response = self._chat_use_case.execute(request)
                    elif self._use_case == UseCase.TOOLS:
                        response = self._tools_chat_use_case.execute(request)
                    else:
                        st.error(f"Unknown use case: {self._use_case}")
                        return
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.write(response.content)
                    
                    # Show metadata in expander
                    if response.metadata:
                        with st.expander("Response Details"):
                            st.json(response.metadata)
            
            except ValidationError as e:
                st.error(f"❌ Validation Error: {e.message}")
                if e.details:
                    with st.expander("Error Details"):
                        st.json(e.details)
            
            except LLMProviderError as e:
                st.error(f"❌ LLM Error: {e.message}")
                st.info("Please check your API key and try again.")
            
            except Exception as e:
                st.error(f"❌ Unexpected Error: {str(e)}")
                st.info("An unexpected error occurred. Please try again.")
    
    def _render_news(self):
        """Render news generation interface."""
        if not st.session_state.get('isFetchButtonClicked', False):
            st.info("👈 Configure news settings in the sidebar and click 'Load News'")
            return
        
        try:
            # Get frequency from session state
            timeframe = st.session_state.get('timeframe', 'Daily')
            frequency = NewsFrequency(timeframe.lower())
            
            # Display progress
            with st.spinner(f"Fetching {timeframe.lower()} news..."):
                # Create request
                request = NewsRequest(frequency=frequency)
                
                # Execute use case
                response = self._news_use_case.execute(request)
            
            # Display success message
            st.success(f"✅ Generated {timeframe.lower()} news summary with {response.article_count} articles")
            
            # Display summary
            st.markdown("## News Summary")
            st.markdown(response.summary)
            
            # Show file path
            if response.file_path:
                st.info(f"📄 Summary saved to: {response.file_path}")
            
            # Reset button state
            st.session_state.isFetchButtonClicked = False
        
        except ValidationError as e:
            st.error(f"❌ Validation Error: {e.message}")
            st.session_state.isFetchButtonClicked = False
        
        except SearchServiceError as e:
            st.error(f"❌ Search Error: {e.message}")
            st.info("Please check your Tavily API key and try again.")
            st.session_state.isFetchButtonClicked = False
        
        except StorageError as e:
            st.error(f"❌ Storage Error: {e.message}")
            st.session_state.isFetchButtonClicked = False
        
        except LLMProviderError as e:
            st.error(f"❌ LLM Error: {e.message}")
            st.info("Please check your API key and try again.")
            st.session_state.isFetchButtonClicked = False
        
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            st.info("An unexpected error occurred. Please try again.")
            st.session_state.isFetchButtonClicked = False

