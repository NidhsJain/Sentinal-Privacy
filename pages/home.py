import streamlit as st

def render_home():
    if 'show_learn_more' not in st.session_state:
        st.session_state.show_learn_more = False

    # Page Specific CSS to perfectly match the final screenshot
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
    
    /* Hero Section */
    .hero-badge { background-color: rgba(30, 41, 59, 0.6); color: #94a3b8; padding: 6px 14px; border-radius: 20px; font-size: 0.65rem; font-weight: 600; display: inline-block; margin-bottom: 30px; letter-spacing: 0.5px;}
    .hero-title { font-size: 4.5rem; font-weight: 800; color: #f8fafc; line-height: 1.1; margin-bottom: 25px; text-align: center; letter-spacing: -1px;}
    .hero-desc { color: #94a3b8; text-align: center; max-width: 650px; margin: 0 auto 35px auto; font-size: 1.05rem; line-height: 1.6;}
    
    /* General Streamlit Button Tweaks */
    div[data-testid="stButton"] button {
        border-radius: 8px !important;
    }
    
    /* Primary Button */
    button[kind="primary"] {
        background: #7c3aed !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background: #6d28d9 !important;
    }
    button[kind="secondary"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: white !important;
    }
    button[kind="secondary"]:hover {
        border-color: #64748b !important;
    }
    </style>
    """, unsafe_allow_html=True)



    # Top Navigation Layout - exactly MATCHING
    n1, spacer, n2, n3 = st.columns([7, 1, 1.5, 1.5])
    with n1:
        st.markdown('<div class="nav-logo" style="padding-top:10px;">Sentinel Privacy</div>', unsafe_allow_html=True)
    with n2:
        st.markdown('<div style="color: #e2e8f0; border-bottom: 2px solid #a855f7; padding-bottom: 4px; font-weight: 600; font-size: 0.85rem; padding: 0 10px; margin-top: 10px; text-align: center;">Home</div>', unsafe_allow_html=True)
    with n3:
        if st.button("About", key="nav_about_btn", type="tertiary"):
            st.session_state.page = 'about'
            st.rerun()
            
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div class="hero-badge">🛡️ DEFENSE LEVEL: OPTIMAL</div>
        <h1 class="hero-title">Are you ready to check<br>your <span style="color: #d8b4fe;">Privacy Risk?</span></h1>
        <p class="hero-desc">This privacy audit will analyze your app permissions, tracking settings, and data exposure to calculate your Privacy Risk Score and help you improve your privacy.</p>
    </div>
    """, unsafe_allow_html=True)

    # Action Buttons matching the visual layout exactly
    spacer_left, col_btn1, col_btn2, spacer_right = st.columns([2.5, 1.2, 1.2, 2.5])
    
    with col_btn1:
        if st.button("Start Privacy Check", type="primary", use_container_width=True):
            st.session_state.page = 'questionnaire'
            st.session_state.q_index = 0
            st.rerun()
            
    with col_btn2:
        if st.button("Learn More", type="secondary", use_container_width=True):
            st.session_state.show_learn_more = not st.session_state.show_learn_more
            st.rerun()

    if st.session_state.show_learn_more:
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 30px; margin-bottom: 30px;">
            <div style="background-color: #1e293b; border: 1px solid #334155; padding: 25px 35px; border-radius: 12px; color: #cbd5e1; text-align: left; max-width: 700px; font-size: 0.95rem; line-height: 1.7; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <span style="display:block; margin-bottom: 12px;">SentinelPrivacy is a privacy risk awareness and analysis tool designed to help users understand how their device settings, app permissions, tracking behaviour, and account security settings affect their personal privacy risk.</span>
                <span style="display:block; margin-bottom: 12px;">We do NOT store your personal data.<br>We only store anonymous privacy risk scores for research and improvement purposes.</span>
                <span style="display:block; margin-bottom: 12px;">Your answers are not linked to your identity.<br>No personal identifiers are collected or stored.</span>
                <span style="display:block;">Our goal is only to increase privacy awareness and help users improve their digital privacy settings.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)