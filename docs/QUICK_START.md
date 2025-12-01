# Quick Start Guide

## Phase 1 Refactoring - Getting Started

### Prerequisites
- Python 3.11+
- Virtual environment activated
- API keys for Groq and Tavily

### Setup (5 minutes)

#### 1. Create Environment File
```bash
cp .env.example .env
```

#### 2. Add Your API Keys
Edit `.env` and add your keys:
```env
GROQ_API_KEY=your_actual_groq_key_here
TAVILY_API_KEY=your_actual_tavily_key_here
```

Get your keys:
- Groq: https://console.groq.com/keys
- Tavily: https://www.tavily.com

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
streamlit run app.py
```

### Testing the Refactoring

#### Run Unit Tests
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=src/langgraph_agentic_ai --cov-report=html

# View coverage report
open htmlcov/index.html
```

#### Test Each Use Case

1. **Basic Chat**
   - Select "Basic" use case
   - Enter a message
   - Verify response

2. **Tools Chat**
   - Select "Tools" use case
   - Ask a question requiring web search
   - Verify tool usage

3. **News Generation**
   - Select "News" use case
   - Choose frequency (Daily/Weekly/Monthly)
   - Click "Load News"
   - Verify summary generation

### What Changed?

#### Before Phase 1
- API keys in UI input fields
- No input validation
- Tight coupling to Streamlit
- Generic error handling
- No tests

#### After Phase 1
- ✅ API keys in `.env` file (secure)
- ✅ Comprehensive input validation
- ✅ Clean architecture (testable)
- ✅ Custom exceptions with context
- ✅ Unit tests with 70%+ coverage target
- ✅ **All use cases tested and working**

### Testing Status

All three use cases have been tested and verified:

1. ✅ **Basic Chat** - Working with new architecture
2. ✅ **Tools Chat** - Working with legacy graph (backward compatible)
3. ✅ **News Generation** - Working with new architecture

See `TESTING_RESULTS.md` for detailed test results.

### Troubleshooting

#### "API key not found"
- Check `.env` file exists
- Verify API keys are set correctly
- Ensure no quotes around keys in `.env`

#### "Module not found"
- Run: `pip install -r requirements.txt`
- Ensure virtual environment is activated

#### "Tests failing"
- Run: `pip install -r requirements-dev.txt`
- Check Python version (3.11+ required)

### Project Structure

```
agentic_chatbot/
├── .env                    # Your API keys (create this)
├── .env.example           # Template
├── app.py                 # Entry point
├── requirements.txt       # Dependencies
├── requirements-dev.txt   # Dev dependencies
├── pytest.ini            # Test configuration
│
├── src/langgraph_agentic_ai/
│   ├── domain/           # Business logic
│   ├── application/      # Use cases
│   ├── infrastructure/   # External services
│   └── presentation/     # UI adapters
│
└── tests/
    ├── unit/            # Unit tests
    └── integration/     # Integration tests
```

### Key Files

- **Entry Point:** `src/langgraph_agentic_ai/main.py`
- **Config:** `src/langgraph_agentic_ai/config/default.ini`
- **DI Container:** `src/langgraph_agentic_ai/infrastructure/di/container.py`
- **Use Cases:** `src/langgraph_agentic_ai/application/use_cases/`

### Development Workflow

1. **Make changes** in appropriate layer:
   - Domain logic → `domain/`
   - Use cases → `application/use_cases/`
   - Infrastructure → `infrastructure/`
   - UI → `presentation/`

2. **Write tests** for new functionality:
   ```bash
   # Create test file
   touch tests/unit/domain/test_my_feature.py
   
   # Run specific test
   pytest tests/unit/domain/test_my_feature.py -v
   ```

3. **Run all tests** before committing:
   ```bash
   pytest
   ```

4. **Check code quality** (optional):
   ```bash
   black src/
   mypy src/
   pylint src/
   ```

### Next Steps

After Phase 1, you can:

1. **Add new use cases** - Follow the pattern in `application/use_cases/`
2. **Add new LLM providers** - Implement `ILLMProvider` interface
3. **Add new storage backends** - Implement `IStorageService` interface
4. **Add more tests** - Expand test coverage
5. **Proceed to Phase 2** - Performance & scalability improvements

### Documentation

- **Full Refactoring Details:** `PHASE1_REFACTORING.md`
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.md`
- **Original Code Review:** `CODE_REVIEW_4.md`

### Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the documentation files
3. Check test files for usage examples
4. Verify `.env` file is configured correctly

---

**Status:** ✅ Phase 1 Complete
**Ready to use:** Yes
**Tests passing:** Run `pytest` to verify

