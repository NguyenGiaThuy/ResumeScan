"""
Processing page for JD and Resume matching analysis
"""

import streamlit as st
from components.ui import (
    display_main_header, 
    display_match_result, 
    display_analysis_details, 
    display_centered_button
)
from services.matching import MatchingService


class ProcessingPage:
    """Page for handling JD-Resume matching processing"""
    
    def __init__(self, matching_service: MatchingService):
        self.matching_service = matching_service
    
    def render(self):
        """Render the processing page"""
        display_main_header("🔍 Analyzing Compatibility", "")
        
        # Check if we already have a match result
        if st.session_state.match_result is None:
            # Only run matching if we don't have results yet
            result = self.matching_service.match_jd_resume(
                st.session_state.jd_file,
                st.session_state.resume_file
            )
            
            if result:
                st.session_state.match_result = result
                st.rerun()  # Rerun to display results
            else:
                # If processing failed, show back button
                self._show_back_button()
        else:
            # We already have results, display them
            self._display_results()
    
    def _display_results(self):
        """Display the matching results"""
        result = st.session_state.match_result
        match_percentage = result.get("final_match_percentage", 0)
        
        # Display results
        qualified = display_match_result(match_percentage, result)
        
        # Show detailed analysis
        if "llm_analysis" in result:
            analysis = result["llm_analysis"]
            display_analysis_details(analysis, qualified)
        
        # Initialize interview if qualifying
        if qualified:
            if display_centered_button("🎯 Start Interview"):
                # The interview initialization will be handled by the interview page
                st.session_state.step = "interview"
                st.rerun()
        
        # Always show back button when we have results
        self._show_back_button()
    
    def _show_back_button(self):
        """Show back button to return to upload"""
        if display_centered_button("⬅️ Upload Different Files", button_type="secondary"):
            self._reset_to_upload()
            st.rerun()
    
    def _reset_to_upload(self):
        """Reset the app to upload state"""
        st.session_state.step = "upload"
        st.session_state.jd_file = None
        st.session_state.resume_file = None
        st.session_state.match_result = None
        st.session_state.messages = []
        st.session_state.vector_store = None
        st.session_state.reset_requested = True
