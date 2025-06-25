#!/usr/bin/env python3
"""
Function Calling Agent - Agent Engineering Bootcamp Assignment
An AI agent that can use tools to search documents and the web
"""

import os
import json
from typing import List, Dict, Any, Optional
from litellm import completion
from dotenv import load_dotenv
from agent_tools import AgentTools
from cli_interface import CLIInterface

load_dotenv()


class FunctionCallingAgent:
    """
    AI Agent with function calling capabilities.
    
    This agent can:
    1. Search through RAG documents (Tool 1)
    2. Search the web for current information (Tool 2)
    """
    
    def __init__(self, cli: CLIInterface):
        """Initialize the function calling agent."""
        self.cli = cli
        self.tools = AgentTools()
        self.available_tools = self.tools.get_available_tools()
        
        # Check OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    def chat_with_tools(self, user_message: str) -> str:
        """
        Main chat method that can use tools.
        
        Args:
            user_message (str): User's message/question
            
        Returns:
            str: AI response (potentially using tools)
        """
        try:
            self.cli.print_question(user_message)
            
            # System message to guide the agent
            system_message = """You are a helpful AI assistant with access to tools:

1. search_documents: Search through uploaded documents
2. search_web: Search the internet for current information

Use tools when appropriate to provide better answers."""

            # First call to get tool usage
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            
            self.cli.loading_animation("Thinking", 1.5)
            
            # Call OpenAI with function calling
            response = completion(
                model="openai/gpt-4o",
                messages=messages,
                tools=self.available_tools,
                tool_choice="auto",
                temperature=0.7
            )
            
            response_message = response.choices[0].message
            
            # Check if the model wants to call functions
            tool_calls = getattr(response_message, 'tool_calls', None)
            
            if tool_calls:
                # Execute tool calls
                messages.append(response_message)
                
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    self.cli.print_info(f"Using tool: {function_name}")
                    self.cli.loading_animation(f"Executing {function_name}", 2.0)
                    
                    # Execute the tool
                    tool_result = self.tools.execute_tool(function_name, **function_args)
                    
                    # Display tool results
                    self._display_tool_results(function_name, tool_result)
                    
                    # Add tool result to conversation
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(tool_result)
                    })
                
                # Get final response from the model
                self.cli.loading_animation("Generating final response", 1.5)
                
                final_response = completion(
                    model="openai/gpt-4o",
                    messages=messages,
                    temperature=0.7
                )
                
                final_answer = final_response.choices[0].message.content
                
            else:
                # No tools needed, just return the response
                final_answer = response_message.content
            
            # Display the final answer
            self.cli.print_answer(final_answer)
            return final_answer
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.cli.print_error(error_msg)
            return "Sorry, I encountered an error."
    
    def _display_tool_results(self, tool_name: str, tool_result: Dict[str, Any]):
        """Display tool execution results in a nice format."""
        if tool_result.get("success"):
            results = tool_result.get("results", [])
            
            if tool_name == "search_documents":
                self.cli.print_success(f"Found {len(results)} documents")
                
            elif tool_name == "search_web":
                self.cli.print_success(f"Found {len(results)} web results")
        else:
            error = tool_result.get("error", "Unknown error")
            self.cli.print_warning(f"Tool {tool_name} failed: {error}")
    
    def interactive_chat(self):
        """Start an interactive chat session with tool capabilities."""
        self.cli.print_info("🔧 Function Calling Agent Ready!")
        self.cli.print_info("Type 'quit' to exit.")
        
        # Show available tools
        tool_names = [tool["function"]["name"] for tool in self.available_tools]
        self.cli.print_success(f"Available tools: {', '.join(tool_names)}")
        
        while True:
            try:
                question = self.cli.get_user_input("What would you like to know")
                
                if question.lower() in ['quit', 'exit', 'q']:
                    self.cli.print_success("Chat session ended!")
                    break
                
                if not question.strip():
                    self.cli.print_warning("Please enter a question.")
                    continue
                
                self.chat_with_tools(question)
                self.cli.print_separator()
                
            except KeyboardInterrupt:
                self.cli.print_success("\nGoodbye!")
                break
            except Exception as e:
                self.cli.print_error(f"Error: {e}")
                continue 