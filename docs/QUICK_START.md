# Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you set up and run the Agentic Chatbot AI application quickly.

---

## 📋 Prerequisites

- **Python**: 3.11 or higher
- **pip**: Latest version
- **Git**: For cloning the repository
- **API Keys**:
  - Groq API Key ([Get it here](https://console.groq.com/keys))
  - Tavily API Key ([Get it here](https://www.tavily.com)) - Required for Tools & News use cases

---

## ⚡ Quick Setup

### 1. Clone & Navigate

```bash
git clone <your-repo-url>
cd agentic_chatbot
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

Add your API keys to `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎮 Using the Application

### Basic Chat

1. **Select LLM**: Choose `groq`
2. **Select Model**: Pick `llama-3.1-8b-instant` (recommended)
3. **Select Use Case**: Choose `Basic`
4. **Start Chatting**: Type your message in the chat input

**Example**:
```
You: What is machine learning?
Bot: Machine learning is a subset of artificial intelligence...
```

### Tools Chat (with Web Search)

1. **Select Use Case**: Choose `Tools`
2. **Ask Questions**: The bot will search the web when needed

**Example**:
```
You: What's the latest news about AI?
Bot: [Searches web] Based on recent articles, the latest AI news includes...
```

### News Aggregation

1. **Select Use Case**: Choose `News`
2. **Select Time Frame**: Daily, Weekly, or Monthly
3. **Click "Load News"**: Wait for the summary
4. **View Results**: News summary displayed and saved to `md/` folder

**Output**: Markdown file with Liverpool FC news summaries

---

## 🔧 Development Setup

### Install Dev Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/domain/test_message_validator.py

# Run with coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Code Quality

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
pylint src/
```

---

## 📁 Project Structure

```
agentic_chatbot/
├── app.py                  # Entry point
├── .env                    # Your API keys (gitignored)
├── .env.example            # Template
├── src/                    # Source code
│   ├── domain/             # Business logic
│   ├── application/        # Use cases
│   ├── infrastructure/     # External services
│   └── presentation/       # UI layer
├── tests/                  # Test suite
├── docs/                   # Documentation
└── md/                     # News outputs
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"

**Solution**: Make sure you're in the virtual environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Issue: "API key not found"

**Solution**: Check your `.env` file
```bash
# Verify .env exists
ls -la .env

# Check contents (don't share this!)
cat .env
```

### Issue: "Import error"

**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Tests failing

**Solution**: Check if pytest-cov is installed
```bash
pip install pytest-cov
```

### Issue: Streamlit not starting

**Solution**: Check if port 8501 is available
```bash
# Kill any process using port 8501
lsof -ti:8501 | xargs kill -9  # macOS/Linux

# Or use a different port
streamlit run app.py --server.port 8502
```

---

## 🔑 API Keys Guide

### Getting Groq API Key

1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up or log in
3. Click "Create API Key"
4. Copy the key
5. Add to `.env`: `GROQ_API_KEY=your_key_here`

**Available Models**:
- `llama-3.1-8b-instant` - Fast, recommended for most use cases
- `llama3-70b-8192` - More capable, larger context
- `mixtral-8x7b-32768` - Alternative with large context

### Getting Tavily API Key

1. Visit [Tavily](https://www.tavily.com)
2. Sign up for an account
3. Navigate to API Keys section
4. Copy your API key
5. Add to `.env`: `TAVILY_API_KEY=your_key_here`

**Required For**:
- ✅ Tools use case (web search)
- ✅ News use case (news aggregation)
- ❌ Not needed for Basic chat

---

## 📚 Use Cases Explained

### 1. Basic Chat 💬
**What it does**: Simple conversational AI  
**When to use**: General Q&A, creative writing, explanations  
**Requires**: Groq API key only

**Example prompts**:
- "Explain quantum computing in simple terms"
- "Write a haiku about coding"
- "What are the SOLID principles?"

### 2. Tools Chat 🔧
**What it does**: AI with web search capabilities  
**When to use**: Need current information, fact-checking, research  
**Requires**: Groq + Tavily API keys

**Example prompts**:
- "What's the weather in London today?"
- "Who won the latest Premier League match?"
- "What are the current AI trends?"

### 3. News Aggregation 📰
**What it does**: Fetches and summarizes Liverpool FC news  
**When to use**: Regular news updates, content curation  
**Requires**: Groq + Tavily API keys

**Features**:
- Daily, Weekly, or Monthly summaries
- Markdown formatted output
- Saved to `md/` folder
- Sorted by date (latest first)

---

## 🎯 Next Steps

### For Users
1. ✅ Run the application
2. ✅ Try all three use cases
3. ✅ Explore different models
4. ✅ Check the news summaries in `md/` folder

### For Developers
1. ✅ Read `PHASE1_COMPLETE.md` for architecture details
2. ✅ Review `CODE_REVIEW_4.md` for technical deep dive
3. ✅ Run tests to understand the codebase
4. ✅ Explore the clean architecture layers

### For Contributors
1. ✅ Fork the repository
2. ✅ Create a feature branch
3. ✅ Write tests for new features
4. ✅ Submit a pull request

---

## 💡 Tips & Best Practices

### Performance
- Use `llama-3.1-8b-instant` for faster responses
- Use `llama3-70b-8192` for more complex tasks
- News aggregation takes 10-30 seconds (fetches 20 articles)

### Security
- Never commit your `.env` file
- Rotate API keys regularly
- Use different keys for dev/prod environments

### Development
- Run tests before committing
- Use `black` for consistent formatting
- Check `logs/app.log` for debugging
- Keep dependencies updated

---

## 📞 Getting Help

### Documentation
- **PHASE1_COMPLETE.md** - Complete refactoring summary
- **CODE_REVIEW_4.md** - Technical deep dive
- **README.md** - Project overview

### Common Commands
```bash
# Start app
streamlit run app.py

# Run tests
pytest

# Format code
black src/ tests/

# Check logs
tail -f logs/app.log

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Logs Location
- Application logs: `logs/app.log`
- News summaries: `md/daily_summary.md`, `md/weekly_summary.md`

---

## ✅ Checklist

Before running the application, make sure:

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`requirements.txt`)
- [ ] `.env` file created with API keys
- [ ] GROQ_API_KEY added to `.env`
- [ ] TAVILY_API_KEY added to `.env` (if using Tools/News)

---

## 🎉 You're Ready!

Everything is set up! Run the application:

```bash
streamlit run app.py
```

**Enjoy your production-ready Agentic Chatbot! 🚀**

---

**Need more help?**
- Check the logs: `logs/app.log`
- Review documentation in `docs/`
- Run tests to verify setup: `pytest`

**Happy coding! 💻**
