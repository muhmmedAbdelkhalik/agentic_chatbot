"""Application constants."""
from enum import Enum


class UseCase(str, Enum):
    """Available use cases for the chatbot."""
    BASIC = "Basic"
    TOOLS = "Tools"
    NEWS = "News"


class NewsFrequency(str, Enum):
    """Valid news frequency options."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "year"


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    GROQ = "groq"
    OPENAI = "openai"


# Validation constants
MAX_MESSAGE_LENGTH = 5000
MIN_MESSAGE_LENGTH = 1

# File storage constants
DEFAULT_STORAGE_DIR = "./md"
ALLOWED_FILE_EXTENSIONS = [".md"]

# News constants
NEWS_TIME_RANGE_MAP = {
    NewsFrequency.DAILY: 'd',
    NewsFrequency.WEEKLY: 'w',
    NewsFrequency.MONTHLY: 'm',
    NewsFrequency.YEARLY: 'y'
}

NEWS_DAYS_MAP = {
    NewsFrequency.DAILY: 1,
    NewsFrequency.WEEKLY: 7,
    NewsFrequency.MONTHLY: 30,
    NewsFrequency.YEARLY: 366
}

# LLM constants
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

