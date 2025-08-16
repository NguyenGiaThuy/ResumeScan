"""
Interview service for managing AI-powered interview sessions
"""

import os
import tempfile
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.chains import RetrievalQA
from utils import utils
from typing import Dict, Any


class InterviewService:
    """Service for handling interview session operations"""
    
    def __init__(self, configs: Dict[Any, Any]):
        self.configs = configs
    
    def initialize_interview_session(self, resume_file) -> bool:
        """
        Initialize the interview session with the resume
        
        Args:
            resume_file: The uploaded resume file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not resume_file:
            return False
        
        try:
            # Process the resume for the interview
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(resume_file.getvalue())
                tmp_pdf_path = tmp_file.name
            
            loader = PyPDFLoader(tmp_pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=5000, chunk_overlap=100
            )
            split_docs = text_splitter.split_documents(docs)
            
            embedding_config = {
                "region_name": self.configs["aws"]["bedrock"]["model_region"],
                "model_id": self.configs["aws"]["bedrock"]["embedding_model_id"],
            }
            embeddings = BedrockEmbeddings(**embedding_config)
            vector_store = FAISS.from_documents(split_docs, embeddings)
            
            st.session_state.vector_store = vector_store
            st.session_state.split_docs = split_docs
            st.session_state.docs = docs
            
            # Initialize conversation
            st.session_state.messages = [
                {"role": "system", "content": self.configs["initial_system_message"]},
                {"role": "ai", "content": self.configs["initial_ai_message"]},
            ]
            
            # Generate initial interview question based on resume
            self._generate_initial_question(split_docs)
            
            # Clean up temp file
            os.unlink(tmp_pdf_path)
            
            return True
            
        except Exception as e:
            st.error(f"Error initializing interview: {str(e)}")
            return False
    
    def _generate_initial_question(self, split_docs):
        """Generate the initial interview question based on resume content"""
        model = utils.get_model(
            model_id=self.configs["aws"]["bedrock"]["model_id"],
            region=self.configs["aws"]["bedrock"]["model_region"],
            model_kwargs=self.configs["aws"]["bedrock"]["model_kwargs"],
        )
        
        context = split_docs[0].page_content if split_docs else ""
        initial_interview_q = (
            f"Based on this resume, ask me one specific interview question about my experience or skills. "
            f"Keep it professional and relevant to what's mentioned in the resume.\n\n"
            f"Resume excerpt:\n{context[:1000]}\n\nYour question:"
        )
        ai_msg = model.invoke(initial_interview_q)
        st.session_state.messages.append({"role": "ai", "content": ai_msg.content})
    
    def get_model(self):
        """Get the configured AI model"""
        return utils.get_model(
            model_id=self.configs["aws"]["bedrock"]["model_id"],
            region=self.configs["aws"]["bedrock"]["model_region"],
            model_kwargs=self.configs["aws"]["bedrock"]["model_kwargs"],
        )
    
    def process_user_response(self, prompt: str) -> str:
        """
        Process user response and generate AI reply
        
        Args:
            prompt: User's input message
            
        Returns:
            str: AI response
        """
        prompt += self.configs.get("holding_context_message", "")
        
        # Generate AI response
        if st.session_state.vector_store:
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.get_model(),
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
            )
            res = qa_chain({"query": prompt})
            return res["result"] if "result" in res else res
        else:
            prompt_template = utils.create_prompt(st.session_state.messages)
            chain = prompt_template | self.get_model()
            ai_msg = chain.invoke({})
            return ai_msg.content
