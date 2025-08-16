"""
Interview page for AI-powered interview sessions
"""

import streamlit as st
from components.ui import display_main_header, display_session_header, display_interview_sidebar
from services.interview import InterviewService


class InterviewPage:
    """Page for handling AI interview sessions"""
    
    def __init__(self, interview_service: InterviewService):
        self.interview_service = interview_service
    
    def render(self):
        """Render the interview page"""
        display_main_header("🎤 AI Interview Session", "")
        
        # Top bar with match info and reset button
        if display_session_header(st.session_state.match_result):
            self._reset_to_upload()
            st.rerun()
        
        # Initialize interview if not already done
        if st.session_state.vector_store is None:
            if not self.interview_service.initialize_interview_session(st.session_state.resume_file):
                st.error("Failed to initialize interview session")
                return
        
        # Chat interface
        self._render_chat_interface()
        
        # Sidebar with session info
        display_interview_sidebar(st.session_state.match_result)
    
    def _render_chat_interface(self):
        """Render the chat interface"""
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] != "system":
                st.chat_message(message["role"]).markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your response here..."):
            # Display user message
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "human", "content": prompt})
            
            # Generate and display AI response
            ai_response = self.interview_service.process_user_response(prompt)
            st.chat_message("assistant").markdown(ai_response)
            st.session_state.messages.append({"role": "ai", "content": ai_response})
    
    def _reset_to_upload(self):
        """Reset the app to upload state"""
        st.session_state.step = "upload"
        st.session_state.jd_file = None
        st.session_state.resume_file = None
        st.session_state.match_result = None
        st.session_state.messages = []
        st.session_state.vector_store = None
        st.session_state.reset_requested = True
