#!/usr/bin/env python3
"""
Agent Tools - Function Calling for Agent Engineering Bootcamp
Tool 1: RAG Document Retrieval 
Tool 2: Web Search
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from vectorize_wrapper import VectorizeWrapper
from dotenv import load_dotenv

load_dotenv()


class AgentTools:
    """
    Function calling tools for the AI agent.
    """
    
    def __init__(self):
        """Initialize the agent tools."""
        # Initialize RAG source if available
        try:
            self.rag_source = VectorizeWrapper()
            self.has_rag = True
        except:
            self.rag_source = None
            self.has_rag = False
    
    def get_available_tools(self) -> List[Dict]:
        """Get the list of available tools for the AI agent."""
        tools = []
        
        # Tool 1: RAG Document Retrieval
        if self.has_rag:
            tools.append({
                "type": "function",
                "function": {
                    "name": "search_documents",
                    "description": "Search through uploaded documents to find relevant information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find relevant documents"
                            },
                            "num_results": {
                                "type": "integer", 
                                "description": "Number of documents to retrieve",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            })
        
        # Tool 2: Web Search  
        tools.append({
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the internet for current information and news.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query for web search"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of search results",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        })
        
        return tools
    
    def search_documents(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Tool 1: Search through RAG documents.
        
        Args:
            query (str): Search query
            num_results (int): Number of results to return
            
        Returns:
            Dict with search results
        """
        if not self.has_rag:
            return {
                "success": False,
                "error": "RAG source not available",
                "results": []
            }
        
        try:
            documents = self.rag_source.retrieve_documents(query, num_results)
            
            # Format results for the agent
            formatted_results = []
            for doc in documents:
                formatted_results.append({
                    "content": doc.get("content", ""),
                    "score": doc.get("metadata", {}).get("score", "N/A"),
                    "source": "knowledge_base"
                })
            
            return {
                "success": True,
                "query": query,
                "results": formatted_results,
                "total_found": len(formatted_results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error searching documents: {str(e)}",
                "results": []
            }
    
    def search_web(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Tool 2: Search the web for current information.
        
        Args:
            query (str): Search query
            max_results (int): Maximum results to return
            
        Returns:
            Dict with search results
        """
        try:
            # Using DuckDuckGo API (free, no API key needed)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Extract useful information
            results = []
            
            # Main answer
            if data.get("Abstract"):
                results.append({
                    "title": "Quick Answer",
                    "content": data["Abstract"],
                    "url": data.get("AbstractURL", ""),
                    "source": "web_search"
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results-1]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append({
                        "title": topic.get("Text", "")[:50] + "...",
                        "content": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                        "source": "web_search"
                    })
            
            # If no results, try a different approach
            if not results:
                results.append({
                    "title": "Search performed",
                    "content": f"Searched for '{query}' - check web manually for latest info",
                    "url": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
                    "source": "web_search"
                })
            
            return {
                "success": True,
                "query": query,
                "results": results[:max_results],
                "total_found": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error searching web: {str(e)}",
                "results": []
            }
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name with given parameters.
        
        Args:
            tool_name (str): Name of the tool to execute
            **kwargs: Tool parameters
            
        Returns:
            Dict with tool execution results
        """
        if tool_name == "search_documents":
            return self.search_documents(**kwargs)
        elif tool_name == "search_web":
            return self.search_web(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "results": []
            } 