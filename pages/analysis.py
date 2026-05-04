import streamlit as st
import time

def render_analysis():
    # Hide nav and standard elements to make it a pure loading screen
    st.markdown("""
    <style>
    .stApp {background-color: #0b0e14;}
    [data-testid="stSidebar"] {display: none !important;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # If already analyzed, ensure we go straight to dashboard
    if st.session_state.get('analysis_complete', False):
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 5rem; animation: pulse 1.5s infinite; filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.4));">🛡️</div>
            <h2 style="color: white; margin-top: 20px; font-weight: 700;">Analyzing your privacy exposure...</h2>
            <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 30px;">Generating your Privacy Risk Report</p>
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulation loop
        statuses = [
            "Scanning Location & Tracking settings...",
            "Analyzing App permissions...",
            "Evaluating Identity Protection...",
            "Calculating Privacy Risk Score...",
            "Finalizing Report..."
        ]
        
        for i in range(100):
            time.sleep(0.04) # Simulate time (4 seconds total)
            progress_bar.progress(i + 1)
            
            # Update status text periodically
            if i == 0: status_text.markdown(f"<p style='text-align:center; color:#6366f1; font-weight:600;'>{statuses[0]}</p>", unsafe_allow_html=True)
            elif i == 20: status_text.markdown(f"<p style='text-align:center; color:#6366f1; font-weight:600;'>{statuses[1]}</p>", unsafe_allow_html=True)
            elif i == 45: status_text.markdown(f"<p style='text-align:center; color:#6366f1; font-weight:600;'>{statuses[2]}</p>", unsafe_allow_html=True)
            elif i == 70: status_text.markdown(f"<p style='text-align:center; color:#6366f1; font-weight:600;'>{statuses[3]}</p>", unsafe_allow_html=True)
            elif i == 90: status_text.markdown(f"<p style='text-align:center; color:#6366f1; font-weight:600;'>{statuses[4]}</p>", unsafe_allow_html=True)
            
        time.sleep(0.5)
        
        st.session_state.analysis_complete = True
        st.session_state.page = 'dashboard'
        st.rerun()
