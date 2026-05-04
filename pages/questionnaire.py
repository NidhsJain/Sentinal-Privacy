import streamlit as st

# Import your questions - adjust path if necessary based on your structure
try:
    from utils.questions import QUESTIONS, OPTIONS
except ImportError:
    # Fallback dummy data just in case the import path fails
    QUESTIONS = [("GEOSPATIAL PRIVACY", "Are you comfortable with applications accessing your precise location even when not in active use?")]
    OPTIONS = ["Yes", "No", "Not Sure"]

try:
    from utils.scoring import calculate_total_score, calculate_risk_level
except ImportError:
    def calculate_total_score(answers): return 0
    def calculate_risk_level(score): return "Low"

def render_questionnaire():
    st.markdown("""
    <style>
    .nav-container { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #1e293b; margin-bottom: 40px;}
    .nav-logo { font-size: 1.2rem; font-weight: 700; color: #a5b4fc; }
    .nav-links { display: flex; gap: 30px; color: #94a3b8; font-size: 0.9rem; font-weight: 500;}
    .active-nav { color: #fff; border-bottom: 2px solid #818cf8; padding-bottom: 5px;}
    
    .q-card { background-color: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 40px; margin-bottom: 30px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);}
    .q-category { display: inline-block; background-color: #1e293b; color: #6366f1; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; border: 1px solid #312e81; font-weight: 600; margin-bottom: 20px; text-transform: uppercase;}
    .q-text { font-size: 1.6rem; color: #f8fafc; font-weight: 600; line-height: 1.4; margin-bottom: 30px;}
    
    .audit-status { text-align: center; font-size: 0.75rem; color: #64748b; font-weight: 500; margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

    total_q = len(QUESTIONS)
    idx = st.session_state.q_index

    # Top Navigation
    st.markdown("""
    <style>
    .st-key-nav_home_q_btn > button, .st-key-nav_about_q_btn > button {
        background: transparent !important; border: none !important; box-shadow: none !important; color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.85rem !important; padding: 0 10px !important; margin-top: 5px !important;
    }
    .st-key-nav_home_q_btn > button:hover, .st-key-nav_about_q_btn > button:hover { color: #e2e8f0 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    n1, spacer, n2, n3 = st.columns([7, 1, 1.5, 1.5])
    with n1:
        st.markdown('<div style="font-size: 1.1rem; font-weight: 700; color: #a5b4fc; padding-top:10px;">Sentinel Privacy</div>', unsafe_allow_html=True)
    with n2:
        if st.button("Home", key="nav_home_q_btn", type="tertiary"):
            st.session_state.page = 'home'
            st.rerun()
    with n3:
        if st.button("About", key="nav_about_q_btn", type="tertiary"):
            st.session_state.page = 'about'
            st.rerun()
    
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # Use columns to center the main content
    left_spacer, center_col, right_spacer = st.columns([1, 2.5, 1])

    with center_col:
        # Header & Progress inside center column
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 15px;">
            <div>
                <div style="font-size: 0.7rem; color: #64748b; font-weight: 600; letter-spacing: 1px;">ANALYSIS IN PROGRESS</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">Data Sovereignty Audit</div>
            </div>
            <div style="color: #f8fafc; font-size: 0.9rem; font-weight: 600;">Question {idx + 1} of {total_q}</div>
        </div>
        <div style="height: 2px; background: #1e293b; margin-bottom: 30px; border-radius: 2px; position: relative;">
            <div style="position: absolute; height: 100%; width: {((idx+1)/total_q)*100}%; background: #6366f1; border-radius: 2px;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Ensure index is safe
        if idx >= total_q: idx = total_q - 1
        category, q_text = QUESTIONS[idx]
        current_answer = st.session_state.answers.get(idx)

        # Main Question Card
        st.markdown(f"""
        <div class="q-card">
            <div class="q-category">🛡️ {category}</div>
            <div class="q-text">{q_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive Answer Buttons wrapped immediately below the text inside the card concept
        ans1, ans2, ans3 = st.columns(3)
        
        # We change button type to "primary" if it's the currently selected answer
        with ans1: 
            if st.button("✔️ Yes", key=f"yes_{idx}", use_container_width=True, type="primary" if current_answer == "Yes" else "secondary"):
                st.session_state.answers[idx] = "Yes"
                st.rerun()
        with ans2: 
            if st.button("✖️ No", key=f"no_{idx}", use_container_width=True, type="primary" if current_answer == "No" else "secondary"):
                st.session_state.answers[idx] = "No"
                st.rerun()
        with ans3: 
            if st.button("❔ Not Sure", key=f"ns_{idx}", use_container_width=True, type="primary" if current_answer == "Not Sure" else "secondary"):
                st.session_state.answers[idx] = "Not Sure"
                st.rerun()

        # Dynamic Audit Status Calculation
        section_mapping = {
            "Location Privacy": "Location Sovereignty",
            "Camera & Microphone": "Identity Protection",
            "Data Access": "Identity Protection",
            "App Behaviour": "General Security",
            "Tracking & Ads": "Network Privacy",
            "Account Security": "General Security",
        }
        
        section_totals = {"Location Sovereignty": 0, "Identity Protection": 0, "General Security": 0, "Network Privacy": 0}
        section_answered = {"Location Sovereignty": 0, "Identity Protection": 0, "General Security": 0, "Network Privacy": 0}
        
        for i, (cat, _) in enumerate(QUESTIONS):
            sec = section_mapping.get(cat, "General Security")
            if sec not in section_totals:
                section_totals[sec] = 0
                section_answered[sec] = 0
            section_totals[sec] += 1
            if i in st.session_state.answers:
                section_answered[sec] += 1
                
        def get_status_icon(section):
            total = section_totals.get(section, 0)
            ans = section_answered.get(section, 0)
            if total == 0 or ans == 0: return "○"
            if ans < total: return "⏳"
            return "✔️"
            
        icon_gen = get_status_icon("General Security")
        icon_loc = get_status_icon("Location Sovereignty")
        icon_id = get_status_icon("Identity Protection")
        icon_net = get_status_icon("Network Privacy")

        # Audit Status (Centered below buttons)
        st.markdown(f"""
        <div class="audit-status">
            <div style="font-size: 0.65rem; text-transform: uppercase; margin-bottom: 10px;">Audit Status</div>
            <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
                <span>General Security <span>{icon_gen}</span></span>
                <span>Location Sovereignty <span>{icon_loc}</span></span>
                <span>Identity Protection <span>{icon_id}</span></span>
                <span>Network Privacy <span>{icon_net}</span></span>
            </div>
        </div>
        <br><br>
        """, unsafe_allow_html=True)

    # Bottom Navigation (Previous / Next)
    st.markdown("<hr style='border-color: #1e293b; margin-top: 20px; margin-bottom: 30px;'>", unsafe_allow_html=True)
    bot_col1, bot_spacer, bot_col2 = st.columns([1, 4, 1])
    
    with bot_col1:
        if st.button("← Previous", type="secondary"):
            if st.session_state.q_index > 0:
                st.session_state.q_index -= 1
            else:
                st.session_state.page = 'home'
            st.rerun()
            
    with bot_col2:
        btn_label = "Complete Audit →" if idx == total_q - 1 else "Next Question →"
        if st.button(btn_label, type="primary"):
            if current_answer is None:
                st.warning("⚠️ Please answer the question before moving forward.", icon="⚠️")
            else:
                if idx < total_q - 1:
                    st.session_state.q_index += 1
                else:
                    st.session_state.questionnaire_completed = True
                    
                    # Calculate and store scores
                    answers_list = []
                    category_scores = {}
                    
                    for i in range(total_q):
                        ans = st.session_state.answers.get(i, "No")
                        answers_list.append(ans)
                        
                        cat = QUESTIONS[i][0]
                        s_val = 3 if ans == "Yes" else (2 if ans == "Not Sure" else 0)
                        
                        if cat not in category_scores:
                            category_scores[cat] = 0
                        category_scores[cat] += s_val
                        
                    st.session_state.category_scores = category_scores
                    st.session_state.total_score = calculate_total_score(answers_list)
                    st.session_state.risk_percentage = (st.session_state.total_score / (total_q * 3)) * 100
                    st.session_state.risk_level = calculate_risk_level(st.session_state.total_score)
                    
                    st.session_state.page = 'analysis' # Move to the next phase
                st.rerun()
