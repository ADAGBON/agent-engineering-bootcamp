import os
from typing import List, Dict, Any, Optional
from litellm import completion
from dotenv import load_dotenv
from rag_source_base import RAGSourceBase
from cli_interface import CLIInterface

# Load environment variables
load_dotenv()


class RAGChat:
    """
    Main RAG Chat system that combines document retrieval with LLM generation.
    
    This class orchestrates the entire RAG pipeline:
    1. Takes user questions
    2. Retrieves relevant documents (if RAG source is provided)
    3. Generates context-aware responses using LLM
    """
    
    def __init__(self, cli: CLIInterface, rag_source: Optional[RAGSourceBase] = None):
        """
        Initialize the RAG Chat system.
        
        Args:
            cli (CLIInterface): CLI interface for user interaction
            rag_source (RAGSourceBase, optional): RAG source for document retrieval
        """
        self.cli = cli
        self.rag_source = rag_source
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    def retrieve_documents(self, question: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for the question.
        
        Args:
            question (str): User's question
            num_results (int): Number of documents to retrieve
            
        Returns:
            List[Dict[str, Any]]: Retrieved documents or empty list if no RAG source
        """
        if not self.rag_source:
            return []
        
        try:
            self.cli.loading_animation("Searching knowledge base", 1.5)
            documents = self.rag_source.retrieve_documents(question, num_results)
            return documents
        except Exception as e:
            self.cli.print_error(f"Failed to retrieve documents: {e}")
            return []
    
    def format_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context for the LLM.
        
        Args:
            documents (List[Dict[str, Any]]): Retrieved documents
            
        Returns:
            str: Formatted context string
        """
        if not documents:
            return ""
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.get('content', 'No content available')
            context_parts.append(f"Document {i}: {content}")
        
        return "\n\n".join(context_parts)
    
    def generate_response(self, question: str, context: str = "") -> str:
        """
        Generate AI response using LLM with optional context.
        
        Args:
            question (str): User's question
            context (str): Retrieved document context
            
        Returns:
            str: AI-generated response
        """
        try:
            # Prepare the prompt
            if context:
                system_message = """You are a helpful AI assistant. Use the provided context to answer the user's question. 
                If the context doesn't contain relevant information, say so and provide a general response based on your knowledge.
                
                Context:
                {context}"""
                
                messages = [
                    {"role": "system", "content": system_message.format(context=context)},
                    {"role": "user", "content": question}
                ]
            else:
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Answer the user's question to the best of your ability."},
                    {"role": "user", "content": question}
                ]
            
            self.cli.loading_animation("Generating response", 2.0)
            
            # Call LiteLLM
            response = completion(
                model="openai/gpt-4o",
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.cli.print_error(f"Failed to generate response: {e}")
            return "I apologize, but I'm having trouble generating a response right now."
    
    def chat(self, question: str) -> str:
        """
        Main chat method that handles the full RAG pipeline.
        
        Args:
            question (str): User's question
            
        Returns:
            str: AI-generated response
        """
        self.cli.print_question(question)
        
        # Step 1: Retrieve documents (if RAG source available)
        documents = self.retrieve_documents(question)
        
        # Step 2: Display retrieved documents
        if documents:
            self.cli.print_documents(documents)
        
        # Step 3: Format context
        context = self.format_context(documents)
        
        # Step 4: Generate response
        response = self.generate_response(question, context)
        
        # Step 5: Display response
        self.cli.print_answer(response)
        
        return response
    
    def interactive_chat(self):
        """
        Start an interactive chat session.
        """
        self.cli.print_info("Welcome to the interactive RAG chat!")
        self.cli.print_info("Type 'quit', 'exit', or press Ctrl+C to end the session.")
        
        if self.rag_source:
            self.cli.print_success("RAG source connected - I can search your knowledge base!")
        else:
            self.cli.print_warning("No RAG source - Using general AI knowledge only.")
        
        while True:
            try:
                question = self.cli.get_user_input()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    self.cli.print_success("Chat session ended. Goodbye!")
                    break
                
                if not question.strip():
                    self.cli.print_warning("Please enter a question.")
                    continue
                
                self.chat(question)
                self.cli.print_separator()
                
            except KeyboardInterrupt:
                self.cli.print_success("\nChat session ended. Goodbye!")
                break
            except Exception as e:
                self.cli.print_error(f"An error occurred: {e}")
                continue 