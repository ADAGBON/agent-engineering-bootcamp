# Agent Engineering Bootcamp - RAG System with Vectorize

This is a complete RAG (Retrieval-Augmented Generation) system built for the Agent Engineering Bootcamp. It supports multiple document retrieval sources including **Vectorize.io** for semantic search.

## 🚀 Features

- **Multi-source RAG**: Supports Vectorize.io, or OpenAI-only mode
- **Function Calling Agent**: AI agent with 2 tools (Week 2 Assignment!)
- **Web Interface**: Beautiful modern web UI for the agent (BONUS!)
- **Document Upload System**: Upload PDFs, TXT, MD, DOCX, DOC, CSV files
- **Beautiful CLI**: Colored terminal interface with loading animations
- **Flexible Architecture**: Easy to add new RAG sources
- **Production Ready**: Proper error handling and environment management

## 📋 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Choose Your RAG Source

Edit `main.py` and set the `RAG_SOURCE` variable:

```python
# Options: RAGSourceType.VECTORIZE, RAGSourceType.NONE
RAG_SOURCE = RAGSourceType.VECTORIZE  # For Vectorize.io integration
RAG_SOURCE = RAGSourceType.NONE       # For OpenAI-only mode
```

### Step 3: Environment Variables Setup

Create a `.env` file in your project root:

#### For Vectorize.io Integration:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your-openai-api-key

# Vectorize.io Credentials (required for Vectorize RAG)
VECTORIZE_ORGANIZATION_ID=your-org-id
VECTORIZE_PIPELINE_ACCESS_TOKEN=your-access-token
VECTORIZE_PIPELINE_ID=your-pipeline-id
```

#### For OpenAI-Only Mode:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your-openai-api-key
```

## 🔧 Vectorize.io Setup Guide

### 1. Create Vectorize Account

1. Go to [https://vectorize.io](https://vectorize.io)
2. Sign up for a free account
3. Navigate to your dashboard

### 2. Get Organization ID

1. Look at your browser URL after logging in
2. Extract the UUID from the URL after `/organization/`
3. This is your `VECTORIZE_ORGANIZATION_ID`

### 3. Generate Access Token

1. Go to the "Access Tokens" section in your dashboard
2. Click "Generate New Token"
3. Copy the token - this is your `VECTORIZE_PIPELINE_ACCESS_TOKEN`

### 4. Create a Pipeline

1. Click "Create Pipeline" in your dashboard
2. Choose "File Upload" as your source
3. Configure your pipeline settings
4. Note the Pipeline ID - this is your `VECTORIZE_PIPELINE_ID`

### 5. Upload Documents

You can upload documents to your pipeline via:
- **Web Interface**: Drag and drop files in the Vectorize dashboard
- **API**: Use the Vectorize API to programmatically upload documents

## 🖥️ Usage

### Run the Interactive Chat

```bash
python main.py chat
```

### Run the Function Calling Agent (Assignment!)

**Command Line:**
```bash
python main.py agent
```

**Web Interface:**
```bash
python main.py web
```
Then open: http://localhost:5000

The agent has **2 Tools**:
1. **Document Search**: Searches your uploaded documents using Vectorize.io
2. **Web Search**: Searches the internet for current information

### Upload Documents

```bash
# Upload single file
python main.py upload file document.pdf

# Upload multiple files
python main.py upload file *.pdf

# Upload entire folder
python main.py upload folder ./documents
```

### Example Conversation

```
============================================================
  Agent Engineering Bootcamp - RAG System
  Agent Engineering Bootcamp - RAG Integration
============================================================

✅ SUCCESS: Environment variables verified!
✅ SUCCESS: RAG source initialized: vectorize
ℹ️  INFO: Welcome to the interactive RAG chat!
ℹ️  INFO: Type 'quit', 'exit', or press Ctrl+C to end the session.

💬 Enter your question: What is machine learning?

🤔 Question: What is machine learning?

📚 Retrieved Documents:
--------------------------------------------------

Document 1:
Score: 0.89
Content: Machine learning is a subset of artificial intelligence that...

🤖 AI Answer:
--------------------------------------------------
Based on the retrieved documents, machine learning is a subset of artificial intelligence...
```

## 📁 Project Structure

```
agent-engineering-bootcamp/
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore file
├── main.py                 # Main entry point
├── rag_chat.py            # Core RAG logic
├── rag_source_base.py     # Base interface for RAG sources
├── vectorize_wrapper.py   # Vectorize.io integration
├── cli_interface.py       # Beautiful CLI interface
├── agent_tools.py         # Function calling tools (Week 2)
├── function_calling_agent.py # Main agent with tools (Week 2)
├── web_app.py             # Flask web interface (BONUS)
├── templates/             # Web interface templates
│   └── index.html         # Main chat interface
├── requirements.txt       # Dependencies
├── README.md             # This file
└── my_project/           # Original project structure
    ├── src/
    └── tests/
```

## 🔄 Switching Between RAG Sources

To switch between different RAG sources, simply change the `RAG_SOURCE` in `main.py`:

```python
# For Vectorize.io
RAG_SOURCE = RAGSourceType.VECTORIZE

# For OpenAI-only (no document retrieval)
RAG_SOURCE = RAGSourceType.NONE
```

## 🌟 Advanced Features

### Custom Document Upload to Vectorize

You can programmatically upload documents to your Vectorize pipeline:

```python
from vectorize_wrapper import VectorizeWrapper

# Initialize wrapper
vectorize = VectorizeWrapper()

# Upload documents via API
# (Implementation depends on your specific use case)
```

### Adding New RAG Sources

To add a new RAG source (like Pinecone, Weaviate, etc.):

1. Create a new wrapper class inheriting from `RAGSourceBase`
2. Implement the required methods: `retrieve_documents()` and `get_required_env_vars()`
3. Add the new source type to `RAGSourceType` enum
4. Update the `get_rag_source()` function in `main.py`

## 🛠️ Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Make sure your `.env` file exists and contains all required variables
   - Double-check your API keys and Vectorize credentials

2. **"Failed to retrieve documents from Vectorize"**
   - Verify your Vectorize pipeline ID is correct
   - Ensure your access token has the right permissions
   - Check that your pipeline has documents uploaded

3. **"Failed to generate response"**
   - Verify your OpenAI API key is valid
   - Check your OpenAI account has sufficient credits

### Getting Help

- Check the [Vectorize.io Documentation](https://vectorize.io/introducing-the-vectorize-api/)
- Review the [Agent Engineering Bootcamp materials](https://github.com/trancethehuman/rag-python)
- Ensure all environment variables are properly set

## 📚 Learning Resources

- [Vectorize.io API Documentation](https://vectorize.io/introducing-the-vectorize-api/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 🎯 Assignment Submission

This project fulfills the Agent Engineering Bootcamp assignments:

### Week 1: Basic RAG System ✅
- ✅ **LiteLLM Integration**: Uses LiteLLM for LLM calls
- ✅ **RAG Implementation**: Complete retrieval-augmented generation  
- ✅ **Vectorize Integration**: Connects to Vectorize.io for document search
- ✅ **CLI Interface**: Beautiful command-line interaction

### Week 2: Function Calling Agent ✅  
- ✅ **Tool 1**: RAG document retrieval from Vectorize.io
- ✅ **Tool 2**: Web search for current information  
- ✅ **Function Calling**: Uses OpenAI's function calling API
- ✅ **Agent Architecture**: Intelligent tool selection and execution
- ✅ **Professional Structure**: Clean, documented, and modular code
- ✅ **Error Handling**: Graceful handling of tool failures

**Ready for submission!** 🚀

---

**Built for the Agent Engineering Bootcamp** 🤖✨ 

Commands:
  chat                                    # Start interactive RAG chat
  upload file document.pdf               # Upload single file
  upload folder ./documents              # Upload folder
  agent                                   # Start function calling agent (Week 2 Assignment!)
  
Examples:
  python main.py chat                     # Start chat mode
  python main.py upload file *.pdf       # Upload all PDF files
  python main.py upload folder docs/     # Upload all files from docs folder
  python main.py agent                    # Start agent with tools (WEEK 2 ASSIGNMENT) 