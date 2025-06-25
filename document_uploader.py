#!/usr/bin/env python3
"""
Document Uploader for Agent Engineering Bootcamp RAG System
Supports multiple file formats and uploads to Vectorize
"""

import os
import json
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional
import vectorize_client as v
from dotenv import load_dotenv

load_dotenv()


class DocumentUploader:
    """Fast document uploader for the RAG system."""
    
    SUPPORTED_FORMATS = {
        '.pdf': 'application/pdf',
        '.txt': 'text/plain', 
        '.md': 'text/markdown',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.csv': 'text/csv'
    }
    
    def __init__(self):
        """Initialize uploader with Vectorize credentials."""
        self.org_id = os.getenv("VECTORIZE_ORGANIZATION_ID")
        self.access_token = os.getenv("VECTORIZE_PIPELINE_ACCESS_TOKEN")
        
        if not self.org_id or not self.access_token:
            raise ValueError("Missing Vectorize credentials!")
        
        # Initialize API
        self.api = v.ApiClient(v.Configuration(access_token=self.access_token))
        self.files_api = v.FilesApi(self.api)
    
    def upload_file(self, file_path: str) -> bool:
        """Upload a single file to Vectorize."""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                return False
            
            suffix = file_path.suffix.lower()
            if suffix not in self.SUPPORTED_FORMATS:
                print(f"❌ Unsupported format: {suffix}")
                return False
            
            content_type = self.SUPPORTED_FORMATS[suffix]
            
            print(f"📤 Uploading: {file_path.name}")
            
            # Start file upload
            response = self.files_api.start_file_upload(
                self.org_id,
                start_file_upload_request=v.StartFileUploadRequest(
                    content_type=content_type,
                    name=file_path.name
                )
            )
            
            # Upload file data
            import urllib3
            http = urllib3.PoolManager()
            
            with open(file_path, "rb") as f:
                upload_response = http.request(
                    "PUT", 
                    response.upload_url, 
                    body=f,
                    headers={
                        "Content-Type": content_type,
                        "Content-Length": str(file_path.stat().st_size)
                    }
                )
            
            if upload_response.status == 200:
                print(f"✅ Upload successful: {file_path.name}")
                return True
            else:
                print(f"❌ Upload failed: {upload_response.status}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading {file_path}: {e}")
            return False
    
    def upload_folder(self, folder_path: str) -> Dict[str, bool]:
        """Upload all supported files from folder."""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"❌ Folder not found: {folder_path}")
            return {}
        
        results = {}
        files_found = []
        
        # Find all supported files
        for suffix in self.SUPPORTED_FORMATS.keys():
            files_found.extend(folder_path.glob(f"*{suffix}"))
        
        if not files_found:
            print(f"❌ No supported files found in {folder_path}")
            return {}
        
        print(f"📁 Found {len(files_found)} files to upload")
        
        # Upload each file
        for file_path in files_found:
            success = self.upload_file(str(file_path))
            results[str(file_path)] = success
        
        # Summary
        successful = sum(results.values())
        print(f"📊 Uploaded {successful}/{len(files_found)} files successfully")
        
        return results 