import streamlit as st
import plotly.express as px
import pandas as pd

import uuid
from utils.db import insert_privacy_result


def save_results_to_db():
    if "db_saved" not in st.session_state:
        data = {
            "session_id": str(uuid.uuid4()),
            "answers": dict(st.session_state.get("answers", {})),
            "category_scores": dict(st.session_state.get("category_scores", {})),
            "total_score": st.session_state.get("total_score", 0),
            "risk_percentage": st.session_state.get("risk_percentage", 0),
            "risk_level": st.session_state.get("risk_level", "Unknown"),
        }

        insert_privacy_result(data)
        st.session_state.db_saved = True
def render_dashboard():
    # Insert results into database on load
    save_results_to_db()

    # If no data is available, send user back to start or set fallbacks
    if 'total_score' not in st.session_state or 'answers' not in st.session_state:
        st.session_state.page = 'home'
        st.rerun()

    # Get data with safe fallbacks according to requirements
    total_score = st.session_state.get('total_score', 0)
    risk_level = st.session_state.get('risk_level', "Low")
    risk_percentage = st.session_state.get('risk_percentage', 0)
    category_scores = st.session_state.get('category_scores', {})
    answers = st.session_state.get('answers', {})
    
    # Theme CSS
    st.markdown("""
    <style>
    .stApp {background-color: #0b0e14;}
    [data-testid="stSidebar"] {display: none !important;}
    header {visibility: hidden;}
    
    .nav-container { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #1e293b; margin-bottom: 40px;}
    .nav-logo { font-size: 1.2rem; font-weight: 700; color: #a5b4fc; }
    
    .dash-card { background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 24px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);}
    
    .metric-title { font-size: 0.8rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;}
    .metric-value { font-size: 2.8rem; font-weight: 800; color: #f8fafc; line-height: 1;}
    .metric-sub { font-size: 0.9rem; color: #94a3b8; margin-top: 5px;}
    
    .level-critical { color: #ef4444 !important; }
    .level-medium { color: #f59e0b !important; }
    .level-low { color: #10b981 !important; }
    
    .st-key-nav_home_d_btn > button, .st-key-nav_about_d_btn > button {
        background: transparent !important; border: none !important; box-shadow: none !important; color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.85rem !important; padding: 0 10px !important; margin-top: 5px !important;
    }
    .st-key-nav_home_d_btn > button:hover, .st-key-nav_about_d_btn > button:hover { color: #e2e8f0 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # Top Navigation Layout - exactly MATCHING
    n1, spacer, n2, n3 = st.columns([7, 1, 1.5, 1.5])
    with n1:
        st.markdown('<div class="nav-logo" style="padding-top:10px;">Sentinel Privacy</div>', unsafe_allow_html=True)
    with n2:
        if st.button("Home", key="nav_home_d_btn", type="tertiary"):
            st.session_state.page = 'home'
            st.rerun()
    with n3:
        if st.button("About", key="nav_about_d_btn", type="tertiary"):
            st.session_state.page = 'about'
            st.rerun()
    
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    
    # Helper for risk color
    level_class = "level-low"
    if risk_level == "High": level_class = "level-critical"
    elif risk_level == "Medium": level_class = "level-medium"
    
    # Title
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="color: white; font-size: 1.8rem; font-weight: 700; margin-bottom: 5px;">Intelligence Dashboard</h1>
        <p style="color: #94a3b8; font-size: 0.95rem;">Real-time privacy exposure monitoring and analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Top Row Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="dash-card">
            <div class="metric-title">🛡️ Privacy Risk Score</div>
            <div class="metric-value">{total_score} <span style="font-size: 1rem; color: #64748b; font-weight: 500;">/ 60</span></div>
            <div class="metric-sub">Total compounded risk value</div>
            <div style="margin-top: 15px; height: 4px; background: #1e293b; border-radius: 2px; position: relative;">
                <div style="position: absolute; height: 100%; width: {risk_percentage}%; background: {'#ef4444' if risk_level == 'High' else ('#f59e0b' if risk_level == 'Medium' else '#10b981')}; border-radius: 2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="dash-card">
            <div class="metric-title">⚠️ Risk Level</div>
            <div class="metric-value {level_class}">{risk_level.upper()}</div>
            <div class="metric-sub">Current vulnerability standing</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        # Calculate high risk settings
        high_risk_count = sum(1 for val in answers.values() if val == "Yes")
        st.markdown(f"""
        <div class="dash-card">
            <div class="metric-title">🔥 Critical Exposures</div>
            <div class="metric-value">{high_risk_count}</div>
            <div class="metric-sub">Settings mapped to severe data leakage</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Middle Row: Charts
    chart_col1, chart_col2 = st.columns([2, 1])
    
    # Prepare Data for Charts
    df_cat = pd.DataFrame(list(category_scores.items()), columns=["Category", "Score"])
    # Sort for the bar chart so top risk is at the top
    df_cat = df_cat.sort_values(by="Score", ascending=True)

    with chart_col1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">Risk by Intelligence Category</div>', unsafe_allow_html=True)
        
        # Horizontal Bar Chart
        if not df_cat.empty and df_cat['Score'].sum() > 0:
            fig_bar = px.bar(
                df_cat, x="Score", y="Category", orientation='h',
                color="Score", color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"]
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                coloraxis_showscale=False,
                xaxis=dict(showgrid=True, gridcolor='#1f2937', zeroline=False),
                yaxis=dict(title="")
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='height:300px; display:flex; align-items:center; justify-content:center; color:#64748b;'>No risk data detected (Perfect Score!)</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">Risk Distribution</div>', unsafe_allow_html=True)
        
        # Donut Chart
        if not df_cat.empty and df_cat['Score'].sum() > 0:
            fig_pie = px.pie(df_cat, values='Score', names='Category', hole=0.7)
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                showlegend=False,
                annotations=[dict(text=f"{int(risk_percentage)}%", x=0.5, y=0.5, font_size=30, showarrow=False, font_color="white", font_weight="bold")]
            )
            fig_pie.update_traces(textposition='inside', textinfo='none', hoverinfo='label+percent', marker=dict(colors=["#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f59e0b", "#10b981"]))
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='height:300px; display:flex; align-items:center; justify-content:center; color:#64748b;'>No risks to distribute</div>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row: Factors & Actions
    bot_col1, bot_col2 = st.columns([1, 1])
    
    with bot_col1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Privacy Exposure Factors</div>', unsafe_allow_html=True)
        
        highest_cat = df_cat.iloc[-1]['Category'] if not df_cat.empty and df_cat['Score'].sum() > 0 else "None"
        
        if highest_cat == "None":
            summary_text = "Your privacy profile indicates an optimal, low-risk level of exposure with minimal tracking identified across tested factors."
        else:
            summary_text = f"Your privacy profile indicates a **{risk_level}** level of exposure. The primary area of concern is **{highest_cat}**. Unnecessary background activity and active privileges are accelerating your data footprint."
        
        st.markdown(f"""
        <div style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">
            {summary_text}
        </div>
        <div style="display: flex; gap: 15px; margin-bottom: 15px; align-items: start;">
            <div style="background: rgba(239, 68, 68, 0.1); padding: 8px; border-radius: 8px; color: #ef4444;">🎯</div>
            <div>
                <div style="color: #e2e8f0; font-weight: 600; font-size: 0.9rem;">Cross-Site Tracking Assessment</div>
                <div style="color: #64748b; font-size: 0.8rem;">Ad-networks may map your behavioral analytics depending on current allowances.</div>
            </div>
        </div>
        <div style="display: flex; gap: 15px; align-items: start;">
            <div style="background: rgba(245, 158, 11, 0.1); padding: 8px; border-radius: 8px; color: #f59e0b;">📡</div>
            <div>
                <div style="color: #e2e8f0; font-weight: 600; font-size: 0.9rem;">Device Background Operations</div>
                <div style="color: #64748b; font-size: 0.8rem;">Active background sessions keep potential trackers alive natively.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with bot_col2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Remediation Stack</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; margin-bottom: 30px;">
            Based on your threat vector mapping, we have generated an active remediation stack. These step-by-step actions will algorithmically minimize your exposure footprint.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Recommendations →", type="primary", use_container_width=True):
            st.session_state.show_assistant = True
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

