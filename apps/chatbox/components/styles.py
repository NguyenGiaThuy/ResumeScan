"""
Custom CSS styles for the AI Elevate Interview System
"""

import streamlit as st

def load_custom_css():
    """Load custom CSS styles for the application"""
    st.markdown("""
    <style>
    .upload-box {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        background-color: #f9f9f9;
    }

    .success-box {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        background-color: #e8f5e8;
    }

    .match-result {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }

    .match-success {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
    }

    .match-failure {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
    }

    .main-title {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
