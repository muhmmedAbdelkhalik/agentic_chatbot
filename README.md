# 🤖 Agentic Chatbot AI

> **A production-ready LangGraph-powered intelligent chatbot with clean architecture, built on modern agentic AI patterns**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green.svg)](https://python.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-red.svg)](https://streamlit.io/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen.svg)](https://github.com/yourusername/agentic_chatbot)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg)](https://github.com/yourusername/agentic_chatbot)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Use Cases](#-use-cases)
- [Project Structure](#-project-structure)
- [API Keys](#-api-keys)
- [Learning Resources](#-learning-resources)

---

## 🎯 Overview

**Agentic Chatbot AI** is an intelligent conversational system leveraging **LangGraph** to create stateful, multi-step AI workflows. The project demonstrates three distinct use cases showcasing different agent capabilities:

1. **Basic Chatbot** - Simple conversational AI
2. **Tool-Enabled Chatbot** - Agent with web search capabilities
3. **AI News Aggregator** - Automated news fetching and summarization for Liverpool FC

### What is LangGraph?

LangGraph is a framework for building stateful, multi-actor applications with LLMs. It extends LangChain by providing:
- **State management** for complex conversational flows
- **Graph-based workflows** with nodes and edges
- **Conditional routing** for dynamic agent behavior
- **Tool integration** for enhanced agent capabilities

---

## ✨ Features

### Current Capabilities

- 🎨 **Multiple Use Cases**: Basic chat, tool-enabled chat, and news aggregation
- 🔧 **Tool Integration**: Web search via Tavily API
- 🧠 **Flexible LLM Support**: Groq (with OpenAI structure ready)
- 📊 **Stateful Conversations**: LangGraph state management
- 🎭 **Interactive UI**: Streamlit-based interface
- ⚙️ **Configuration-Driven**: INI file-based settings
- 📰 **News Automation**: Fetch and summarize Liverpool FC news (daily/weekly/monthly)
- 💾 **Markdown Export**: Save news summaries to files
- 🔐 **Production-Ready Security**: Secure credential management, input validation, audit logging
- 🏗️ **Clean Architecture**: Layered design with dependency injection
- ✅ **Comprehensive Testing**: 70%+ test coverage with pytest

### Technology Stack

- **AI Framework**: LangChain + LangGraph
- **LLM Providers**: Groq (ChatGroq)
- **Search Integration**: Tavily Search API
- **UI Framework**: Streamlit
- **Architecture**: Clean Architecture with DDD principles
- **Testing**: Pytest with comprehensive coverage
- **Security**: Environment-based credential management

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────┐
│         Streamlit UI (load.py)              │
│  - User input collection                    │
│  - Model/use case selection                 │
│  - Result display                           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Main Orchestrator (main.py)            │
│  - UI initialization                        │
│  - LLM configuration                        │
│  - Graph setup & execution                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│       Graph Builder (graph_builder.py)      │
│  - Use case routing                         │
│  - Graph construction                       │
│  - Node orchestration                       │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
┌──────▼──────┐       ┌───────▼────────┐
│   Nodes     │       │     Tools      │
│             │       │                │
│ - Basic     │       │ - Tavily       │
│ - Tool      │       │   Search       │
│ - News      │       │                │
└─────────────┘       └────────────────┘
```

### LangGraph Workflow Examples

#### Basic Chatbot Flow
```
START → Chatbot Node → END
```

#### Tool-Enabled Chatbot Flow
```
START → Chatbot Node → [Conditional: Needs Tool?]
                ↓ Yes              ↓ No
           Tool Node → Chatbot → END
```

#### News Aggregation Flow
```
START → Fetch News → Summarize → Save Result → END
```

---

## 📦 Prerequisites

- **Python**: 3.11 or higher
- **pip**: Latest version
- **API Keys**:
  - Groq API Key ([Get it here](https://console.groq.com/keys))
  - Tavily API Key ([Get it here](https://www.tavily.com)) - Required for Tool & News use cases

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agentic_chatbot.git
cd agentic_chatbot
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# GROQ_API_KEY=your_groq_api_key_here
# TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies included:**
- `langchain` - Core LangChain framework
- `langchain-community` - Community integrations
- `langchain-core` - Core abstractions
- `langchain-groq` - Groq LLM integration
- `langchain-openai` - OpenAI integration
- `langgraph` - Graph-based workflows
- `faiss-cpu` - Vector similarity search
- `streamlit` - Web UI framework
- `tavily-python` - Tavily search API client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- `bleach` - Input sanitization

---

## ⚙️ Configuration

### Configuration File

The application is configured via `src/langgraph_agentic_ai/config/default.ini`:

```ini
[DEFAULT]
PROJECT_NAME = Agentic Chatbot AI
PAGE_TITLE = Agentic Chatbot AI
LLM_OPTIONS = groq, openai
USECASE_OPTIONS = Basic, Tools, News
GROQ_MODEL_OPTIONS = openai/gpt-oss-120b, llama-3.1-8b-instant
```

### Customization

To add new models or use cases:

1. Edit `default.ini`
2. Add comma-separated values to respective options
3. Implement corresponding logic in `graph_builder.py`

---

## 🎮 Usage

### Running the Application

```bash
# Ensure virtual environment is activated
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Interface

1. **Select LLM Provider**: Choose `groq` (or `openai` if configured)
2. **Select Model**: Pick from available Groq models
3. **API Keys**: Automatically loaded from `.env` file (secure!)
4. **Select Use Case**: Choose Basic, Tools, or News
5. **Interact**: 
   - **Basic/Tools**: Type messages in chat input
   - **News**: Select timeframe (Daily/Weekly/Monthly) and click "Load News"

> **Note**: API keys are now securely managed via environment variables. No need to enter them in the UI!

---

## 📚 Use Cases

### 1. Basic Chatbot 💬

**Description**: Simple conversational AI without external tools

**Use When**: 
- General Q&A
- Creative writing
- Code explanation
- Simple problem-solving

**Example Interactions**:
```
User: What is machine learning?
Bot: Machine learning is a subset of artificial intelligence...

User: Write a haiku about code
Bot: Silent keys typing,
     Logic flows through the machine,
     Bugs flee from my sight.
```

**Graph Structure**: 
- Single node that invokes LLM with user message
- Direct START → Chatbot → END flow

---

### 2. Tool-Enabled Chatbot 🔧

**Description**: AI agent with web search capabilities for up-to-date information

**Use When**:
- Need current information
- Fact-checking
- Research queries
- Real-time data lookup

**Example Interactions**:
```
User: What's the weather in London today?
Bot: [Uses Tavily tool to search] Based on current data, London is experiencing...

User: Who won the latest Premier League match?
Bot: [Searches web] The latest Premier League results show...
```

**Graph Structure**:
- Conditional routing based on whether tool call is needed
- Tools node executes searches and returns results
- Chatbot processes tool results and generates response

**Available Tools**:
- **TavilySearchResults**: Web search with max 2 results per query

---

### 3. AI News Aggregator 📰

**Description**: Automated Liverpool FC news fetching and intelligent summarization

**Use When**:
- Regular news updates needed
- Content curation
- Automated reporting
- Trend monitoring

**Features**:
- **Time Ranges**: Daily, Weekly, Monthly
- **Source**: Tavily News API
- **Processing**: Fetches up to 20 articles
- **Output**: Markdown-formatted summaries with:
  - Date stamps (Egypt timezone)
  - Concise summaries
  - Source URLs
  - Sorted by date (latest first)

**Output Location**: `./md/{timeframe}_summary.md`

**Example Output**:
```markdown
# Daily Liverpool FC News Summary

### 2025-11-30
- Liverpool secures dramatic 3-2 victory against Manchester City with last-minute winner
  [Source](https://example.com/article1)

### 2025-11-29  
- Salah discusses contract extension rumors in pre-match interview
  [Source](https://example.com/article2)
```

**Graph Structure**:
```
Fetch News → Summarize News → Save Result
   (API)        (LLM)           (File I/O)
```

---

## 📁 Project Structure

```
agentic_chatbot/
│
├── app.py                              # Application entry point
├── requirements.txt                    # Python dependencies
├── requirements-dev.txt                # Development dependencies
├── .env.example                        # Environment variables template
├── pytest.ini                          # Test configuration
├── README.md                           # This file
│
├── docs/                               # Documentation
│   └── CODE_REVIEW_4.md                # Comprehensive code review
│
├── md/                                 # News summary outputs
│   ├── daily_summary.md
│   ├── weekly_summary.md
│   └── monthly_summary.md
│
├── logs/                               # Application logs
│   └── app.log
│
├── src/
│   └── langgraph_agentic_ai/
│       │
│       ├── main.py                     # Main orchestration (refactored)
│       │
│       ├── domain/                     # 🆕 Domain layer (business logic)
│       │   ├── entities/               # Rich domain entities
│       │   ├── value_objects/          # Immutable value objects
│       │   ├── interfaces/             # Domain interfaces (ports)
│       │   ├── validation/             # Input validation
│       │   ├── exceptions.py           # Custom exceptions
│       │   └── constants.py            # Application constants
│       │
│       ├── application/                # 🆕 Application layer (use cases)
│       │   ├── use_cases/              # Business use cases
│       │   └── dto/                    # Data transfer objects
│       │
│       ├── infrastructure/             # 🆕 Infrastructure layer (adapters)
│       │   ├── llm/                    # LLM adapters
│       │   ├── search/                 # Search service adapters
│       │   ├── storage/                # File storage adapters
│       │   ├── security/               # Security components
│       │   ├── logging/                # Logging infrastructure
│       │   └── di/                     # Dependency injection
│       │
│       ├── presentation/               # 🆕 Presentation layer (UI)
│       │   └── streamlit/              # Streamlit adapters
│       │
│       ├── config/                     # Configuration management
│       │   ├── config.py               # Config loader (updated)
│       │   └── default.ini             # Default settings
│       │
│       ├── graph/                      # LangGraph builders (legacy)
│       ├── llms/                       # LLM integrations (legacy)
│       ├── nodes/                      # LangGraph nodes (legacy)
│       ├── state/                      # State management
│       ├── tools/                      # External tools
│       └── ui/                         # UI components (legacy)
│
└── tests/                              # 🆕 Test suite
    ├── unit/                           # Unit tests
    ├── integration/                    # Integration tests
    └── fixtures/                       # Test fixtures
```

> **🆕 New in Phase 1**: Clean architecture with domain, application, infrastructure, and presentation layers

### Key Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Entry point that loads the main application |
| `main.py` | Orchestrates UI, LLM config, and graph execution |
| `graph_builder.py` | Routes to correct graph based on use case |
| `state.py` | Defines the state structure for LangGraph |
| `*_node.py` | Individual node implementations for each workflow |
| `load.py` | Streamlit UI with sidebar controls |
| `display_result.py` | Handles different result rendering per use case |

---

## 🔑 API Keys

### Secure Setup (Recommended)

API keys are now managed securely via environment variables:

1. **Get Your Keys**:
   - **Groq**: Visit [Groq Console](https://console.groq.com/keys)
   - **Tavily**: Visit [Tavily](https://www.tavily.com)

2. **Add to `.env` file**:
   ```bash
   GROQ_API_KEY=your_actual_groq_key_here
   TAVILY_API_KEY=your_actual_tavily_key_here
   ```

3. **That's it!** Keys are automatically loaded when you run the app.

**Models Available**:
- `llama-3.1-8b-instant` - Fast, efficient Llama model (default)
- `llama3-70b-8192` - Larger, more capable model
- `mixtral-8x7b-32768` - Mixtral model with large context

**Required Keys**:
- ✅ **GROQ_API_KEY**: Required for all use cases
- ✅ **TAVILY_API_KEY**: Required for Tools and News use cases only

---

## 🧪 Testing

The project includes comprehensive testing:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=src/langgraph_agentic_ai --cov-report=html

# View coverage report
open htmlcov/index.html
```

**Test Coverage**: 70%+ with unit tests for:
- Domain validation
- Security components
- File storage operations
- Credential management

---

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

- **Domain Layer**: Business logic, entities, and validation (framework-independent)
- **Application Layer**: Use cases and business workflows
- **Infrastructure Layer**: External services, databases, and APIs
- **Presentation Layer**: UI adapters (Streamlit, can add FastAPI, CLI, etc.)

**Benefits**:
- ✅ Testable without UI or external services
- ✅ Easy to swap implementations (LLM providers, storage, etc.)
- ✅ Business logic independent of frameworks
- ✅ Maintainable and scalable

---

## 🙏 Acknowledgments

- **LangChain** team for the incredible framework
- **LangGraph** for making stateful agents accessible
- **Groq** for fast LLM inference
- **Tavily** for reliable search API
- **Streamlit** for rapid UI prototyping

---

## ⭐ Star History

If you find this project useful, please consider giving it a star ⭐

---

**Built with ❤️ using LangGraph, Clean Architecture, and Python**

**Version**: 2.0.0 (Phase 1 Complete)  
**Last Updated**: December 1, 2025  
**Status**: ✅ Production-Ready for Demo/Development
