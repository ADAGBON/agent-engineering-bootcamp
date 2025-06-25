#!/usr/bin/env python3
"""
Web Frontend for Function Calling Agent
Agent Engineering Bootcamp - Week 2 Assignment
"""

import os
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from agent_tools import AgentTools
from function_calling_agent import FunctionCallingAgent
from cli_interface import CLIInterface
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'agent-bootcamp-secret-key-change-in-production')

# Initialize components
cli = CLIInterface()

class WebCLIInterface:
    """Mock CLI interface for web usage."""
    def __init__(self):
        self.messages = []
    
    def print_info(self, message):
        self.messages.append({'type': 'info', 'content': message})
    
    def print_success(self, message):
        self.messages.append({'type': 'success', 'content': message})
    
    def print_error(self, message):
        self.messages.append({'type': 'error', 'content': message})
    
    def print_warning(self, message):
        self.messages.append({'type': 'warning', 'content': message})
    
    def print_question(self, message):
        self.messages.append({'type': 'question', 'content': message})
    
    def print_answer(self, message):
        self.messages.append({'type': 'answer', 'content': message})
    
    def loading_animation(self, message, duration):
        self.messages.append({'type': 'loading', 'content': message})

@app.route('/')
def index():
    """Main chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Please enter a message'
            })
        
        # Create web CLI interface
        web_cli = WebCLIInterface()
        
        # Check if agent can be initialized
        if not os.getenv("OPENAI_API_KEY"):
            return jsonify({
                'success': False,
                'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.'
            })
        
        # Initialize function calling agent
        agent = FunctionCallingAgent(web_cli)
        
        # Get response from agent
        response = agent.chat_with_tools(user_message)
        
        # Get all messages from the web CLI
        messages = web_cli.messages
        
        return jsonify({
            'success': True,
            'response': response,
            'messages': messages,
            'user_message': user_message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        })

@app.route('/api/tools')
def get_tools():
    """Get available tools information."""
    try:
        tools = AgentTools()
        available_tools = tools.get_available_tools()
        
        tool_info = []
        for tool in available_tools:
            tool_info.append({
                'name': tool['function']['name'],
                'description': tool['function']['description']
            })
        
        return jsonify({
            'success': True,
            'tools': tool_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/status')
def get_status():
    """Get system status."""
    try:
        # Check environment variables
        openai_key = bool(os.getenv("OPENAI_API_KEY"))
        vectorize_org = bool(os.getenv("VECTORIZE_ORGANIZATION_ID"))
        vectorize_token = bool(os.getenv("VECTORIZE_PIPELINE_ACCESS_TOKEN"))
        vectorize_pipeline = bool(os.getenv("VECTORIZE_PIPELINE_ID"))
        
        # Check tool availability
        tools = AgentTools()
        rag_available = tools.has_rag
        
        return jsonify({
            'success': True,
            'status': {
                'openai_configured': openai_key,
                'vectorize_configured': vectorize_org and vectorize_token and vectorize_pipeline,
                'rag_available': rag_available,
                'total_tools': len(tools.get_available_tools())
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting Function Calling Agent Web Interface...")
    print(f"🌐 Open your browser to: http://localhost:{port}")
    print("🔧 Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 