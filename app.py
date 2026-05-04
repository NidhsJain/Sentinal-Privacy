import streamlit as st
from pages.home import render_home
from pages.questionnaire import render_questionnaire

# 1. Page Configuration MUST be the first command
st.set_page_config(
    page_title="Sentinel Privacy", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Global CSS for Theme and Hiding Defaults
st.markdown("""
<style>
    /* Hide the default Streamlit sidebar & header */
    [data-testid="stSidebar"] {display: none !important;}
    header {visibility: hidden;}
    
    /* Global App Background & Padding */
    .stApp {
        background-color: #06080d; 
        background-image: radial-gradient(#1e293b 1px, transparent 1px);
        background-size: 20px 20px;
    }
    [data-testid="stMain"] {
        /* Removed flex-center to prevent top-clipping on tall pages like Questionnaire */
    }
    .block-container {
        background: linear-gradient(145deg, #0d121c, #0a0d14) !important;
        border: 1px solid #1e293b !important;
        border-radius: 16px !important;
        padding: 50px !important;
        margin: 5vh auto 5vh auto !important;
        width: 100% !important;
        max-width: 1100px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Streamlit Button Styling */
    button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        border: none !important; color: white !important; font-weight: 600 !important;
        padding: 0.5rem 2rem !important; border-radius: 8px !important;
    }
    button[kind="secondary"] {
        background-color: #1e293b !important; border: 1px solid #334155 !important;
        color: white !important; font-weight: 600 !important;
        padding: 0.5rem 2rem !important; border-radius: 8px !important;
    }
    button[kind="secondary"]:hover { border-color: #64748b !important; }
    
    /* Absolutely strip all button styling from explicitly named Navigation Buttons globally via Positional Column Index! */
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(2) button,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(3) button,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(4) button {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #94a3b8 !important; /* Match inactive text color */
        padding: 0 10px !important;
        margin-top: 10px !important; /* Align exactly with the active underline div margins */
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        min-height: 0 !important;
        height: auto !important;
        line-height: normal !important;
        text-align: center !important;
    }
    
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(2) button:hover,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(3) button:hover,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(4) button:hover {
        color: #e2e8f0 !important; /* Highlight text color on hover */
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(2) button:active,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(3) button:active,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(4) button:active,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(2) button:focus,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(3) button:focus,
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="column"]:nth-child(4) button:focus {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #e2e8f0 !important;
        outline: none !important;
    }
    
    /* Floating Assistant Button Container */
    .floating-assistant-container {
        position: fixed; bottom: 30px; right: 30px; z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Session State Variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {} # Dictionary to store answers by index
if 'questionnaire_completed' not in st.session_state:
    st.session_state.questionnaire_completed = False

# 4. Page Routing Logic
if st.session_state.page == 'home':
    render_home()
elif st.session_state.page == 'questionnaire':
    render_questionnaire()
elif st.session_state.page == 'about':
    from pages.about import render_about
    render_about()
elif st.session_state.page == 'analysis':
    from pages.analysis import render_analysis
    render_analysis()
elif st.session_state.page == 'dashboard':
    from pages.dashboard import render_dashboard
    render_dashboard()

# 5. Global Floating Components
try:
    from utils.chat_widget import render_chat_widget
    render_chat_widget()
except Exception:
    pass