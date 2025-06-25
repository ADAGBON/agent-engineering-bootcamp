#!/usr/bin/env python3
"""
Agent Engineering Bootcamp - RAG System with Vectorize Integration

This is the main entry point for the RAG (Retrieval-Augmented Generation) system.
It supports multiple RAG sources including Vectorize.io for document retrieval.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Import our RAG system components
from rag_source_base import RAGSourceType
from vectorize_wrapper import VectorizeWrapper
from rag_chat import RAGChat
from cli_interface import CLIInterface
from document_uploader import DocumentUploader
from function_calling_agent import FunctionCallingAgent

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


def run_chat_mode(cli):
    """Run the interactive chat mode."""
    
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


def run_upload_mode(cli, upload_args):
    """Run the document upload mode."""
    try:
        # Check upload-specific environment variables
        required_vars = ["VECTORIZE_ORGANIZATION_ID", "VECTORIZE_PIPELINE_ACCESS_TOKEN"]
        missing_vars = check_environment_variables(required_vars)
        
        if missing_vars:
            cli.print_error("Missing required environment variables for upload:")
            for var in missing_vars:
                cli.print_error(f"  - {var}")
            cli.print_info("\nUpload requires Vectorize credentials. Set up:")
            cli.print_info("  VECTORIZE_ORGANIZATION_ID=your-org-id")
            cli.print_info("  VECTORIZE_PIPELINE_ACCESS_TOKEN=your-token")
            return 1
        
        # Initialize uploader
        uploader = DocumentUploader()
        cli.print_success("Document uploader initialized!")
        
        # Handle upload based on arguments
        if upload_args.command == 'file':
            from pathlib import Path
            
            # Handle file upload
            all_files = []
            for path_pattern in upload_args.path:
                path = Path(path_pattern)
                if '*' in path_pattern or '?' in path_pattern:
                    # Handle wildcards
                    parent = path.parent if path.parent != Path('.') else Path.cwd()
                    pattern = path.name
                    matched_files = list(parent.glob(pattern))
                    all_files.extend(matched_files)
                else:
                    all_files.append(path)
            
            if not all_files:
                cli.print_error("No files found matching the pattern(s)")
                return 1
            
            # Upload files
            cli.print_info(f"Uploading {len(all_files)} file(s)...")
            successful = 0
            
            for file_path in all_files:
                if uploader.upload_file(str(file_path)):
                    successful += 1
            
            cli.print_success(f"Upload complete: {successful}/{len(all_files)} files uploaded")
            
        elif upload_args.command == 'folder':
            from pathlib import Path
            
            # Handle folder upload
            folder_path = Path(upload_args.path)
            
            if not folder_path.exists() or not folder_path.is_dir():
                cli.print_error(f"Folder not found: {folder_path}")
                return 1
            
            cli.print_info(f"Uploading files from folder: {folder_path}")
            results = uploader.upload_folder(str(folder_path))
            
            if results:
                successful = sum(results.values())
                cli.print_success(f"Folder upload complete: {successful}/{len(results)} files uploaded")
            else:
                cli.print_warning("No supported files found in folder")
        
        return 0
        
    except Exception as e:
        cli.print_error(f"Upload failed: {e}")
        return 1


def run_agent_mode(cli):
    """Run the function calling agent mode."""
    try:
        # Check required environment variables for agent
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = check_environment_variables(required_vars)
        
        if missing_vars:
            cli.print_error("Missing required environment variables for agent:")
            for var in missing_vars:
                cli.print_error(f"  - {var}")
            cli.print_info("\nAgent mode requires OpenAI API key:")
            cli.print_info("  OPENAI_API_KEY=your-openai-api-key")
            return 1
        
        # Initialize function calling agent
        agent = FunctionCallingAgent(cli)
        cli.print_success("Function calling agent initialized!")
        
        # Start interactive agent chat
        agent.interactive_chat()
        
        return 0
        
    except Exception as e:
        cli.print_error(f"Agent initialization failed: {e}")
        return 1


def main():
    """Main function to run the RAG chat system or document upload."""
    
    parser = argparse.ArgumentParser(
        description="🚀 Agent Engineering Bootcamp - RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  chat                                    # Start interactive RAG chat
  upload file document.pdf               # Upload single file
  upload folder ./documents              # Upload folder
  agent                                   # Start function calling agent (Assignment!)
  
Examples:
  python main.py chat                     # Start chat mode
  python main.py upload file *.pdf       # Upload all PDF files
  python main.py upload folder docs/     # Upload all files from docs folder
  python main.py agent                    # Start agent with tools (ASSIGNMENT)
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='Operating modes')
    
    # Chat mode (default)
    chat_parser = subparsers.add_parser('chat', help='Start interactive RAG chat')
    
    # Agent mode (NEW - for assignment)
    agent_parser = subparsers.add_parser('agent', help='Start function calling agent with tools')
    
    # Upload mode
    upload_parser = subparsers.add_parser('upload', help='Upload documents to RAG system')
    upload_subparsers = upload_parser.add_subparsers(dest='command', help='Upload commands')
    
    # Upload file command
    file_parser = upload_subparsers.add_parser('file', help='Upload single file or files with wildcard')
    file_parser.add_argument('path', nargs='+', help='File path(s) to upload')
    
    # Upload folder command  
    folder_parser = upload_subparsers.add_parser('folder', help='Upload all files from folder')
    folder_parser.add_argument('path', help='Folder path to upload from')
    
    args = parser.parse_args()
    
    # Default to chat mode if no arguments
    if not args.mode:
        args.mode = 'chat'
    
    # Initialize CLI interface
    cli = CLIInterface("Agent Engineering Bootcamp - RAG System")
    
    if args.mode == 'chat':
        return run_chat_mode(cli)
    elif args.mode == 'upload':
        if not args.command:
            cli.print_error("Upload mode requires a command (file or folder)")
            upload_parser.print_help()
            return 1
        return run_upload_mode(cli, args)
    elif args.mode == 'agent':
        return run_agent_mode(cli)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())