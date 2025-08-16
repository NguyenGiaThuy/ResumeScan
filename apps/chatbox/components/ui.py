"""
Common UI components for the AI Elevate Interview System
"""

import streamlit as st
from typing import Optional


def display_main_header(title: str, subtitle: str):
    """Display the main header with title and subtitle"""
    st.markdown(f'<h1 class="main-title">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 18px; color: #7f8c8d;">{subtitle}</p>', unsafe_allow_html=True)


def display_file_uploader(title: str, description: str, file_type: str, key: str, help_text: str) -> Optional[object]:
    """Display a file uploader component with consistent styling"""
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    st.markdown(f"### {title}")
    st.markdown(description)
    
    uploaded_file = st.file_uploader(
        f"Choose {file_type} PDF file",
        type=["pdf"],
        key=key,
        help=help_text
    )
    
    if uploaded_file:
        st.success(f"✅ {file_type} uploaded: {uploaded_file.name}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_file


def display_match_result(match_percentage: float, analysis: dict):
    """Display matching results with appropriate styling"""
    if match_percentage >= 50:
        st.markdown(f"""
        <div class="match-result match-success">
            <h2>🎉 Great Match!</h2>
            <h3>Compatibility Score: {match_percentage:.1f}%</h3>
            <p>You qualify for the interview! The AI has found strong alignment between your profile and the job requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        return True
    else:
        st.markdown(f"""
        <div class="match-result match-failure">
            <h2>📊 Compatibility Analysis</h2>
            <h3>Compatibility Score: {match_percentage:.1f}%</h3>
            <p>Unfortunately, the match score is below the 50% threshold required for the interview process.</p>
            <p>Consider reviewing the job requirements and updating your resume to better align with the position.</p>
        </div>
        """, unsafe_allow_html=True)
        return False


def display_analysis_details(analysis: dict, qualified: bool):
    """Display detailed analysis results"""
    col1, col2 = st.columns(2)
    
    with col1:
        if qualified:
            st.subheader("✅ Matching Skills")
        else:
            st.subheader("✅ Your Strengths")
        
        for skill in analysis.get("matching_skills", []):
            st.write(f"• {skill}")
    
    with col2:
        if qualified:
            st.subheader("📝 Areas to Improve")
        else:
            st.subheader("📈 Areas to Develop")
        
        for req in analysis.get("missing_requirements", []):
            st.write(f"• {req}")
    
    if analysis.get("assessment"):
        if qualified:
            st.subheader("🤖 AI Assessment")
        else:
            st.subheader("💡 Recommendations")
        st.write(analysis["assessment"])


def display_centered_button(text: str, key: str = None, button_type: str = "primary") -> bool:
    """Display a centered button"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        return st.button(text, type=button_type, use_container_width=True, key=key)


def display_interview_sidebar(match_result: dict):
    """Display interview session sidebar"""
    with st.sidebar:
        st.header("📊 Session Info")
        if match_result:
            st.metric("Match Score", f"{match_result.get('final_match_percentage', 0):.1f}%")
            st.write(f"**JD:** {match_result.get('jd_filename', 'N/A')}")
            st.write(f"**Resume:** {match_result.get('resume_filename', 'N/A')}")
        
        st.header("💡 Interview Tips")
        st.write("• Be specific with examples")
        st.write("• Explain your thought process")
        st.write("• Ask clarifying questions if needed")
        st.write("• Take your time to think")


def display_session_header(match_result: dict):
    """Display session header with match info and reset button"""
    col1, col2 = st.columns([3, 1])
    with col1:
        if match_result:
            match_score = match_result.get("final_match_percentage", 0)
            st.success(f"✅ Qualified candidate (Match: {match_score:.1f}%)")
    with col2:
        return st.button("🔄 New Session")
