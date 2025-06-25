#!/usr/bin/env python3
"""
CLI for Document Upload - Agent Engineering Bootcamp
Quick file upload to your RAG system via Vectorize
"""

import sys
import argparse
from pathlib import Path
from document_uploader import DocumentUploader
from cli_interface import CLIInterface


def main():
    """Main CLI function for document upload."""
    
    parser = argparse.ArgumentParser(
        description="🚀 Fast Document Upload for RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python upload_cli.py file document.pdf           # Upload single file
  python upload_cli.py folder ./documents          # Upload folder
  python upload_cli.py file *.txt                  # Upload all txt files
  
Supported formats: .pdf, .txt, .md, .docx, .doc, .csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Upload commands')
    
    # File upload command
    file_parser = subparsers.add_parser('file', help='Upload single file or files with wildcard')
    file_parser.add_argument('path', nargs='+', help='File path(s) to upload')
    
    # Folder upload command  
    folder_parser = subparsers.add_parser('folder', help='Upload all files from folder')
    folder_parser.add_argument('path', help='Folder path to upload from')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize CLI and uploader
    cli = CLIInterface("Document Upload System")
    
    try:
        uploader = DocumentUploader()
        cli.print_success("Document uploader initialized!")
        
        if args.command == 'file':
            # Handle single file or multiple files
            all_files = []
            for path_pattern in args.path:
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
            
        elif args.command == 'folder':
            # Handle folder upload
            folder_path = Path(args.path)
            
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
        
    except ValueError as e:
        cli.print_error(f"Configuration error: {e}")
        cli.print_info("Make sure your .env file contains:")
        cli.print_info("  VECTORIZE_ORGANIZATION_ID=your-org-id")
        cli.print_info("  VECTORIZE_PIPELINE_ACCESS_TOKEN=your-token")
        return 1
        
    except Exception as e:
        cli.print_error(f"Upload failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 