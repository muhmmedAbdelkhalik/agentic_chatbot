"""News generation use case."""
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from ...domain.interfaces.llm_provider import ILLMProvider
from ...domain.interfaces.search_service import ISearchService
from ...domain.interfaces.storage_service import IStorageService
from ...domain.entities.message import Message
from ...domain.validation.message_validator import MessageValidator
from ...domain.value_objects.model_config import ModelConfig
from ..dto.news_request import NewsRequest
from ..dto.news_response import NewsResponse


class NewsGenerationUseCase:
    """
    Use case for news generation and summarization.
    
    Handles the business logic for fetching news, summarizing, and saving.
    """
    
    def __init__(
        self,
        llm_provider: ILLMProvider,
        search_service: ISearchService,
        storage_service: IStorageService,
        validator: Optional[MessageValidator] = None
    ):
        """
        Initialize news generation use case.
        
        Args:
            llm_provider: LLM provider for summarization
            search_service: Search service for fetching news
            storage_service: Storage service for saving results
            validator: Optional message validator
        """
        self._llm = llm_provider
        self._search = search_service
        self._storage = storage_service
        self._validator = validator or MessageValidator()
    
    def execute(self, request: NewsRequest) -> NewsResponse:
        """
        Execute the news generation use case.
        
        Args:
            request: News request DTO
            
        Returns:
            News response DTO
            
        Raises:
            SearchServiceError: If news search fails
            LLMProviderError: If summarization fails
            StorageError: If saving fails
        """
        # Fetch news articles
        articles = self._search.search_news(
            query=request.query,
            frequency=request.frequency,
            max_results=request.max_results
        )
        
        # Summarize articles
        summary = self._summarize_articles(articles)
        
        # Save summary to file
        filename = f"{request.frequency.value}_summary.md"
        file_path = self._storage.save_file(filename, summary)
        
        # Create response DTO
        return NewsResponse(
            summary=summary,
            file_path=file_path,
            article_count=len(articles)
        )
    
    def _summarize_articles(self, articles: list) -> str:
        """
        Summarize news articles using LLM.
        
        Args:
            articles: List of NewsArticle entities
            
        Returns:
            Markdown summary
        """
        # Create prompt template
        system_prompt = """Summarize Liverpool FC news articles into markdown format. For each item include:
        - Date in **YYYY-MM-DD** format in Egypt timezone
        - Concise sentences summary from latest news
        - Sort news by date wise (latest first)
        - Source URL as link
        Use format:
        ### [Date]
        - [Summary](URL)"""
        
        # Format articles for prompt - truncate content to avoid exceeding limits
        MAX_CONTENT_LENGTH = 500  # Limit each article content
        articles_list = []
        for article in articles:
            # Truncate content if too long
            content = article.content[:MAX_CONTENT_LENGTH] if len(article.content) > MAX_CONTENT_LENGTH else article.content
            date_str = article.published_date.isoformat() if article.published_date else 'Unknown'
            articles_list.append(f"Content: {content}\nURL: {article.url}\nDate: {date_str}")
        
        articles_str = "\n\n".join(articles_list)
        
        # Use raw LLM client to avoid Message validation issues with long content
        from langchain_core.messages import SystemMessage, HumanMessage
        
        raw_client = self._llm.get_raw_client()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Articles:\n{articles_str}")
        ]
        
        response = raw_client.invoke(messages)
        
        return response.content

