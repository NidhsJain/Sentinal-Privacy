"""
pages/recommendations.py – Recommendations Page (Phase 5 placeholder)
"""

import streamlit as st
from utils.config import COLORS, PAGES


def render(navigate_to):
    st.markdown(
        f"""
        <style>
            .stApp {{ background: linear-gradient(135deg, {COLORS["bg"]} 0%, #110D2E 100%); }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align:center; padding: 3rem 2rem;
                        background: {COLORS['card_bg']};
                        border: 1px solid rgba(124,58,237,0.3);
                        border-radius: 16px;">
                <div style="font-size:3rem;">💡</div>
                <h2 style="color:#fff; margin-top:1rem;">Recommendations</h2>
                <p style="color:{COLORS['muted']}; font-size:0.95rem;">
                    Phase 5 — Personalised privacy fix recommendations coming next.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="r_back"):
            navigate_to(PAGES["home"])
