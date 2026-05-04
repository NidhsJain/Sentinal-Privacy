import streamlit as st

def render_about():
    # Page Specific CSS to perfectly match Home Page
    st.markdown("""
    <style>
    /* Global App Background & Padding */
    .stApp {background-color: #0b0e14;}
    [data-testid="stSidebar"] {display: none !important;}
    header {visibility: hidden;}
    
    /* Navigation Bar */
    .nav-container { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; margin-bottom: 70px;}
    .nav-logo { font-size: 1.1rem; font-weight: 700; color: #a5b4fc; }
    
    .st-key-nav_home_btn > button, .st-key-nav_about_btn > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0 10px !important;
        margin-top: 5px !important;
    }
    .st-key-nav_home_btn > button:hover, .st-key-nav_about_btn > button:hover {
        color: #e2e8f0 !important;
    }
    
    /* General Streamlit Button Tweaks */
    div[data-testid="stButton"] button {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Top Navigation Layout - exactly MATCHING Home Page
    n1, spacer, n2, n3 = st.columns([7, 1, 1.5, 1.5])
    with n1:
        st.markdown('<div class="nav-logo" style="padding-top:10px;">Sentinel Privacy</div>', unsafe_allow_html=True)
    with n2:
        if st.button("Home", key="nav_home_btn", type="tertiary"):
            st.session_state.page = 'home'
            st.rerun()
    with n3:
        st.markdown('<div style="color: #e2e8f0; border-bottom: 2px solid #a855f7; padding-bottom: 4px; font-weight: 600; font-size: 0.85rem; padding: 0 10px; margin-top: 10px; text-align: center;">About</div>', unsafe_allow_html=True)
            
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # About Content inside a styled container matching Home theme
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 30px;'>About SentinelPrivacy</h1>", unsafe_allow_html=True)
    
    # Pure Streamlit Container to avoid Raw HTML escaping issues
    with st.container():
        st.markdown("""
        **SentinelPrivacy** is a Privacy Risk Analysis and Awareness Tool designed to help users understand how their device settings, app permissions, tracking behaviour, and account security settings affect their personal privacy risk.

        Many users are unaware of how everyday digital settings such as location tracking, app permissions, advertisement tracking, and weak account security can expose their personal data. SentinelPrivacy helps users identify these risks through a structured privacy audit and provides a Privacy Risk Score along with personalized recommendations to improve their digital privacy.

        The system analyzes multiple privacy-related factors including:
        * Location tracking permissions
        * Microphone and camera access
        * App data access and permissions
        * Advertisement and tracking settings
        * Account security settings like password strength and two-factor authentication
        * Network and browsing privacy behaviour

        Based on the user's responses, the system calculates a Privacy Risk Score and categorizes the risk level as Low, Medium, or High. The dashboard then provides insights and recommendations to help users reduce their privacy risk.
        """)
        
        st.info("""
        **Privacy Notice:**
        - SentinelPrivacy does **NOT** store personal data.
        - We only store anonymous privacy risk scores for analysis and improvement purposes.
        - No personal identifiers such as name, email, or device data are collected.
        - All responses are used only to calculate the privacy risk score.
        
        **Our goal is to increase privacy awareness and help users make safer digital decisions.**
        """)

