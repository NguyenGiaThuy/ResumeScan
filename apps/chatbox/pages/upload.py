"""
Upload page for JD and Resume file uploads
"""

import streamlit as st
from components.ui import display_main_header, display_file_uploader, display_centered_button


class UploadPage:
    """Page for handling file uploads"""
    
    def render(self):
        """Render the upload page"""
        display_main_header(
            "🤖 AI Elevate Interview System",
            "Upload your Job Description and Resume to start the AI-powered interview process"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            jd_file = display_file_uploader(
                title="📄 Job Description",
                description="Upload the job description you're applying for",
                file_type="JD",
                key="jd_uploader",
                help_text="Upload the job description as a PDF file"
            )
            if jd_file:
                st.session_state.jd_file = jd_file
        
        with col2:
            resume_file = display_file_uploader(
                title="📋 Resume/CV",
                description="Upload your resume or CV",
                file_type="Resume",
                key="resume_uploader",
                help_text="Upload your resume as a PDF file"
            )
            if resume_file:
                st.session_state.resume_file = resume_file
        
        # Process button
        st.markdown("<br>", unsafe_allow_html=True)
        
        if display_centered_button("🔍 Analyze Compatibility"):
            if st.session_state.jd_file and st.session_state.resume_file:
                st.session_state.step = "processing"
                st.rerun()
            else:
                st.error("Please upload both JD and Resume files before proceeding.")
