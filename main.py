#!/usr/bin/env python3
"""
Agent Engineering Bootcamp - RAG System with Vectorize Integration

This is the main entry point for the RAG (Retrieval-Augmented Generation) system.
It supports multiple RAG sources including Vectorize.io for document retrieval.
"""

import os
import sys
from dotenv import load_dotenv

# Import our RAG system components
from rag_source_base import RAGSourceType
from vectorize_wrapper import VectorizeWrapper
from rag_chat import RAGChat
from cli_interface import CLIInterface

# Load environment variables
load_dotenv()

# Choose your RAG source - CHANGE THIS to switch between sources
RAG_SOURCE = RAGSourceType.NONE  # Options: VECTORIZE, NONE


def check_environment_variables(required_vars):
    """Check if all required environment variables are set."""
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return missing_vars


def get_rag_source():
    """Get the RAG source and required environment variables based on configuration."""
    if RAG_SOURCE == RAGSourceType.VECTORIZE:
        wrapper = VectorizeWrapper()
        return wrapper, wrapper.get_required_env_vars()
    elif RAG_SOURCE == RAGSourceType.NONE:
        return None, ["OPENAI_API_KEY"]
    else:
        raise ValueError(f"Unsupported RAG source: {RAG_SOURCE}")


def main():
    """Main function to run the RAG chat system."""
    
    # Initialize CLI interface
    cli = CLIInterface("Agent Engineering Bootcamp - RAG System")
    
    try:
        # Get RAG source and required environment variables
        rag_source, required_env_vars = get_rag_source()
        
        # Check environment variables
        missing_vars = check_environment_variables(required_env_vars)
        if missing_vars:
            cli.print_error("Missing required environment variables:")
            for var in missing_vars:
                cli.print_error(f"  - {var}")
            
            cli.print_info("\nPlease set the following environment variables:")
            cli.print_info("1. Create a .env file in your project root")
            cli.print_info("2. Add the required variables:")
            
            if RAG_SOURCE == RAGSourceType.VECTORIZE:
                cli.print_info("""
# Required for Vectorize RAG Source:
OPENAI_API_KEY=your-openai-api-key
VECTORIZE_ORGANIZATION_ID=your-org-id
VECTORIZE_PIPELINE_ACCESS_TOKEN=your-access-token
VECTORIZE_PIPELINE_ID=your-pipeline-id

# Get these from:
# - OpenAI API: https://platform.openai.com/api-keys
# - Vectorize: https://vectorize.io (sign up and create a pipeline)
                """)
            else:
                cli.print_info("""
# Required for OpenAI only:
OPENAI_API_KEY=your-openai-api-key

# Get this from: https://platform.openai.com/api-keys
                """)
            
            return 1
        
        # Initialize RAG chat system
        cli.print_success("Environment variables verified!")
        
        if rag_source:
            cli.print_success(f"RAG source initialized: {RAG_SOURCE.value}")
        else:
            cli.print_info("Running in OpenAI-only mode (no document retrieval)")
        
        rag_chat = RAGChat(cli, rag_source)
        
        # Start interactive chat
        rag_chat.interactive_chat()
        
        return 0
        
    except Exception as e:
        cli.print_error(f"Failed to initialize RAG system: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())