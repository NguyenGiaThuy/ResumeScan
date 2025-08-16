"""
Matching service for JD and Resume compatibility analysis
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any


class MatchingService:
    """Service for handling JD-Resume matching operations"""
    
    def __init__(self, service_url: str, configs: dict = None):
        self.service_url = service_url
        self.configs = configs or {}
    
    def match_jd_resume(self, jd_file, resume_file) -> Optional[Dict[Any, Any]]:
        """
        Process JD and Resume matching via API
        
        Args:
            jd_file: Job description file
            resume_file: Resume file
            
        Returns:
            Dict containing match results or None if failed
        """
        if not jd_file or not resume_file:
            st.error("Both JD and Resume files are required")
            return None
        
        try:
            # Prepare files for API call
            files = {
                'jd_file': ('jd.pdf', jd_file.getvalue(), 'application/pdf'),
                'resume_file': ('resume.pdf', resume_file.getvalue(), 'application/pdf')
            }
            
            with st.spinner("Analyzing JD and Resume compatibility..."):
                response = requests.post(
                    f"{self.service_url}/match", 
                    files=files, 
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    st.error(f"Matching service error: {response.text}")
                    return None
                    
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to matching service at {self.service_url}. Please ensure the service is running.")
            return None
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
            return None
