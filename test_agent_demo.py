#!/usr/bin/env python3
"""
Demo script to test the Function Calling Agent tools
Agent Engineering Bootcamp - Week 2 Assignment
"""

from agent_tools import AgentTools
from cli_interface import CLIInterface

def test_tools():
    """Test both tools with sample queries."""
    cli = CLIInterface()
    tools = AgentTools()
    
    cli.print_info("🔧 Testing Function Calling Agent Tools")
    cli.print_separator()
    
    # Test Tool 1: Document Search
    cli.print_info("Testing Tool 1: Document Search")
    result1 = tools.search_documents("What is RAG?", 3)
    if result1["success"]:
        cli.print_success(f"Found {len(result1['results'])} documents")
        for i, doc in enumerate(result1["results"][:2], 1):
            content = doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"]
            cli.print_info(f"Document {i}: {content}")
    else:
        cli.print_warning(f"Document search failed: {result1['error']}")
    
    cli.print_separator()
    
    # Test Tool 2: Web Search (Weather)
    cli.print_info("Testing Tool 2: Web Search (Weather)")
    result2 = tools.search_web("weather in Lagos Nigeria", 3)
    if result2["success"]:
        cli.print_success(f"Found {len(result2['results'])} web results")
        for i, result in enumerate(result2["results"][:2], 1):
            cli.print_info(f"Result {i}: {result['title']}")
            content = result["content"][:150] + "..." if len(result["content"]) > 150 else result["content"]
            cli.print_info(f"  Content: {content}")
    else:
        cli.print_warning(f"Web search failed: {result2['error']}")
    
    cli.print_separator()
    
    # Test Tool 2: Web Search (General)
    cli.print_info("Testing Tool 2: Web Search (AI News)")
    result3 = tools.search_web("latest artificial intelligence news", 3)
    if result3["success"]:
        cli.print_success(f"Found {len(result3['results'])} web results")
        for i, result in enumerate(result3["results"][:2], 1):
            cli.print_info(f"Result {i}: {result['title']}")
            content = result["content"][:150] + "..." if len(result["content"]) > 150 else result["content"]
            cli.print_info(f"  Content: {content}")
    else:
        cli.print_warning(f"Web search failed: {result3['error']}")
    
    cli.print_separator()
    cli.print_success("✅ Tool testing complete!")
    cli.print_info("🌐 Start the web interface: python main.py web")
    cli.print_info("💻 Start the CLI agent: python main.py agent")

if __name__ == "__main__":
    test_tools() 