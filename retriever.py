from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv
import logging
import random
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalChatbot:
    """
    Professional Legal AI Assistant with enhanced capabilities
    """
    
    def __init__(self):
        self.qa_chain = self._initialize_qa_chain()
        
    def _initialize_qa_chain(self) -> Optional[ConversationalRetrievalChain]:
        """Initialize the QA chain with your existing Chroma vector store"""
        try:
            # Secure configuration loading
            load_dotenv(dotenv_path=r"C:\Users\HP\Desktop\rag_project\file.env")
            open_ai_key = os.getenv("OPEN_AI_KEY")
            
            if not open_ai_key:
                raise ValueError("OPEN_AI_KEY not found in environment variables")
            
            # Initialize embeddings with your existing configuration
            embeddings = OpenAIEmbeddings(
                openai_api_key=open_ai_key,
                model="text-embedding-3-small",
                request_timeout=30,
                max_retries=3
            )
            
            # Connect to your existing Chroma vector store
            vector_store = Chroma(
                collection_name="project",
                embedding_function=embeddings,
                persist_directory="legal"
            )
            
            # Professional-grade LLM configuration
            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.3,
                max_tokens=1500,
                api_key=open_ai_key,
                model_kwargs={
                    "top_p": 0.9,
                    "frequency_penalty": 0.1,
                    "presence_penalty": 0.1
                }
            )
            
            # Configure retriever with your existing vector store
            base_retriever = vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={
                    'k': 5,  # Matching your existing setup
                    'fetch_k': 20,
                    'lambda_mult': 0.5
                }
            )
            
            # Enhanced with multi-query retrieval
            multi_query_retriever = MultiQueryRetriever.from_llm(
                retriever=base_retriever,
                llm=llm
            )
            
            # Context-aware compression
            compressor = LLMChainExtractor.from_llm(llm)
            compression_retriever = ContextualCompressionRetriever(
                base_retriever=multi_query_retriever,
                base_compressor=compressor,
                return_source_documents=True
            )
            
            # Professional legal prompt template
            prompt_template = """**Legal AI Assistant Protocol**
Role: Senior Legal Consultant AI
Objective: Provide accurate, professional legal guidance while maintaining approachability

**Response Guidelines**:
1. Contextual Accuracy: Strictly base responses on provided legal documents
2. Professional Tone: Formal yet client-friendly language
3. Clarity: Break complex concepts into digestible points
4. Engagement: Natural conversation flow with:
   - Appropriate follow-up questions
   - Clarification requests when needed
   - Structured information delivery

**Conversation Context**:
{chat_history}

**Relevant Legal Documents**:
{context}

**Client Query**: {question}

**Response Strategy**:
1. Acknowledge query appropriately
2. Provide legally sound response
3. Highlight key considerations
4. Offer next steps or additional assistance

**Assistant's Response**:"""
            
            qa_prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "chat_history", "question"]
            )
            
            # Conversation memory
            memory = ConversationBufferWindowMemory(
                memory_key="chat_history",
                k=5,
                return_messages=True,
                output_key="answer",
                human_prefix="Client",
                ai_prefix="Legal Assistant"
            )
            
            # Configure QA chain
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=compression_retriever,
                memory=memory,
                combine_docs_chain_kwargs={"prompt": qa_prompt},
                return_source_documents=True,
                output_key="answer",
                max_tokens_limit=4000,
                rephrase_question=True,
                get_chat_history=lambda h: h,
                verbose=False
            )
            
            logger.info("QA chain initialized successfully with existing Chroma store")
            return qa_chain
            
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise RuntimeError(f"Failed to initialize legal assistant system: {str(e)}")

    def generate_response(self, query: str) -> Dict[str, Any]:
        """Generate a professional legal response with error handling"""
        try:
            if not query or not isinstance(query, str):
                raise ValueError("Invalid query format")
                
            response = self.qa_chain({"question": query})
            
            # Post-process for professional presentation
            response["answer"] = self._polish_response(response["answer"])
            
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return {
                "answer": "Apologies, I encountered an issue processing your request. Please try again.",
                "source_documents": []
            }
    
    def _polish_response(self, response: str) -> str:
        """Enhance raw response for professional presentation"""
        # Standardize legal references
        response = response.replace("the context", "our legal documents")
        response = response.replace("I don't know", "This specific detail isn't covered in the available documents")
        
        # Ensure professional closing
        if not response.strip().endswith(('.', '?', '!')):
            response = response.rstrip() + '.'
            
        if "?" not in response[-15:]:  # Add follow-up if none exists
            follow_ups = [
                "\n\nWould you like me to elaborate on any aspect?",
                "\n\nShould I research any related legal provisions?",
                "\n\nIs there another legal matter I can assist with?"
            ]
            response += random.choice(follow_ups)
            
        return response


if __name__ == "__main__":
    try:
        legal_assistant = LegalChatbot()
        print("Legal Assistant initialized successfully with existing Chroma database.")
        print("Ready to handle legal queries.")
    except Exception as e:
        print(f"Failed to initialize Legal Assistant: {str(e)}")