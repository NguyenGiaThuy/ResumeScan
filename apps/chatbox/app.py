"""
Main application class for the AI Elevate Interview System
"""

import os
import json
import streamlit as st
from components.styles import load_custom_css
from pages.upload import UploadPage
from pages.processing import ProcessingPage
from pages.interview import InterviewPage
from services.matching import MatchingService
from services.interview import InterviewService


class InterviewApp:
    """Main application class for managing the interview system"""
    
    def __init__(self):
        self.configs = self._load_config()
        self.matching_service = MatchingService(
            os.environ.get("MATCHING_SERVICE_URL", "http://matching:8001"),
            self.configs
        )
        self.interview_service = InterviewService(self.configs)
        
        # Initialize pages
        self.upload_page = UploadPage()
        self.processing_page = ProcessingPage(self.matching_service)
        self.interview_page = InterviewPage(self.interview_service)
    
    def _load_config(self) -> dict:
        """Load application configuration"""
        config_path = os.environ.get("CONFIG_FILE", "configs/ai-elevate-dev.json")
        configs = {}
        if config_path and os.path.isfile(config_path):
            with open(config_path, "r") as f:
                configs = json.load(f)
        return configs
    
    def _configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="AI Elevate Interview Session",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if "step" not in st.session_state:
            st.session_state.step = "upload"  # "upload", "processing", "interview"
        if "jd_file" not in st.session_state:
            st.session_state.jd_file = None
        if "resume_file" not in st.session_state:
            st.session_state.resume_file = None
        if "match_result" not in st.session_state:
            st.session_state.match_result = None
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = None
        if "reset_requested" not in st.session_state:
            st.session_state.reset_requested = False
    
    def _handle_reset_request(self):
        """Handle reset requests"""
        if st.session_state.reset_requested:
            st.session_state.reset_requested = False
            st.session_state.step = "upload"
    
    def run(self):
        """Run the main application"""
        self._configure_page()
        load_custom_css()
        self._initialize_session_state()
        self._handle_reset_request()
        
        # Route to appropriate page based on current step
        if st.session_state.step == "upload":
            self.upload_page.render()
        elif st.session_state.step == "processing":
            self.processing_page.render()
        elif st.session_state.step == "interview":
            self.interview_page.render()
        else:
            st.error(f"Unknown step: {st.session_state.step}")
            st.session_state.step = "upload"
            st.rerun()
