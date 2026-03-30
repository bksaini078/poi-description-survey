"""Helper functions for the POI survey application."""

import base64
from pathlib import Path
import streamlit as st
import uuid


def img_to_bytes(img_path: str) -> str:
    """
    Convert image file to bytes.
    
    Args:
        img_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image data
    """
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path: str) -> str:
    """
    Convert image to HTML img tag with base64 encoded data.
    
    Args:
        img_path (str): Path to the image file
        
    Returns:
        str: HTML img tag with base64 encoded image data
    """
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html

def set_page_config() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="POI Survey Application",
        page_icon="logo/icon.ico",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def add_custom_css() -> None:
    """Add custom CSS styles to the application."""
    from config.constants import CUSTOM_CSS
    st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

def initialize_session_state() -> None:
    """Initialize session state variables."""
    if 'page' not in st.session_state:
        st.session_state.page = -2

    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

    if 'ai_content' not in st.session_state:
        st.session_state.ai_content = {}

    if 'survey_responses' not in st.session_state:
        st.session_state.survey_responses = []

    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    if 'consent_given' not in st.session_state:
        st.session_state.consent_given = False


