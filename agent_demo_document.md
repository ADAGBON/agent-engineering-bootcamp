# Function Calling Agent Demo Document

This document contains test information for the Agent Engineering Bootcamp function calling agent.

## Agent Capabilities

The function calling agent built for this bootcamp has two powerful tools:

1. **Document Search Tool**: Can search through uploaded documents in the knowledge base using semantic search via Vectorize.io
2. **Web Search Tool**: Can search the internet for current information using DuckDuckGo API

## Example Use Cases

### Document Search Examples
- "What is RAG?" - Should find information about Retrieval-Augmented Generation
- "How does the bootcamp work?" - Should find bootcamp-related information
- "What are the agent capabilities?" - Should find this document

### Web Search Examples  
- "What's the current weather in New York?" - Should use web search
- "Latest news about AI" - Should use web search for current information
- "Current Bitcoin price" - Should use web search for real-time data

## Technical Implementation

The agent uses OpenAI's function calling feature to:
1. Analyze user queries
2. Determine which tools to use
3. Execute the appropriate tools
4. Synthesize results into helpful responses

This demonstrates advanced AI agent capabilities including:
- Function calling
- Tool selection
- Multi-source information retrieval
- Response synthesis

## Assignment Requirements Met

✅ **Tool 1**: RAG document retrieval from Vectorize.io  
✅ **Tool 2**: Web search for current information  
✅ **Function Calling**: Uses OpenAI's function calling API  
✅ **Interactive Chat**: Beautiful CLI interface  
✅ **Error Handling**: Graceful handling of tool failures

Perfect for the Agent Engineering Bootcamp Week 2 assignment! 