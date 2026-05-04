import streamlit as st
import requests

def render_chat_widget():
    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    # Check for trigger from "View Recommendations"
    if st.session_state.get("show_assistant", False):
        st.session_state.chat_open = True
        st.session_state.show_assistant = False # Reset trigger
        if not st.session_state.messages:
            st.session_state.messages.append({"role": "assistant", "content": "Hello! I am your Privacy Assistant. Based on your risk report, how can I help you improve your privacy settings today?"})

    # Base Floating Button
    if not st.session_state.chat_open:
        st.markdown("""
        <style>
        .st-key-open_chat {
            position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 9999 !important; width: auto !important; 
        }
        .st-key-open_chat button {
            border-radius: 30px !important; padding: 0.6rem 1.5rem !important; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important; background: linear-gradient(90deg, #8b5cf6, #7c3aed) !important; color: white !important; border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Privacy Assistant", key="open_chat", use_container_width=False):
            if st.session_state.get('questionnaire_done', False) or st.session_state.get('questionnaire_completed', False) or st.session_state.get('total_score') is not None:
                st.session_state.chat_open = True
                if not st.session_state.messages:
                    st.session_state.messages.append({"role": "assistant", "content": "I am your Privacy Assistant. I will help you improve your privacy settings based on your risk report. What would you like to know?"})
                st.rerun()
            else:
                st.info("Please complete the Privacy Risk Test first so I can give personalized recommendations.")
    else:
        st.markdown("""
        <style>
        .st-key-close_chat button {
            background: transparent !important; color: #fca5a5 !important; border: none !important; box-shadow: none !important; font-size: 1.2rem;
        }
        .st-key-close_chat button:hover {
            color: #ef4444 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown("### ✨ Privacy Assistant")
            with col2:
                if st.button("✖", key="close_chat"):
                    st.session_state.chat_open = False
                    st.rerun()

            # Chat Window Inner Body
            chat_box = st.container(height=350, border=False)
            with chat_box:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            # Input Field placed effectively using standard markdown wrap
            if prompt := st.chat_input("Ask about your privacy risks..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.rerun()

            # Processing logic sequentially
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                with chat_box:
                    with st.chat_message("assistant"):
                        with st.spinner("Analyzing..."):
                            # Package Context payload for backend
                            context_payload = {
                                "query": st.session_state.messages[-1]["content"],
                                "dashboard_context": {
                                    "total_score": st.session_state.get("total_score", 0),
                                    "risk_level": st.session_state.get("risk_level", "Unknown"),
                                    "category_scores": st.session_state.get("category_scores", {})
                                }
                            }
                            
                            # API Backend request trigger
                            try:
                                res = requests.post("http://127.0.0.1:8000/chat", json=context_payload, timeout=60)
                                if res.status_code == 200:
                                    bot_reply = res.json().get("response", "Error generating response.")
                                else:
                                    bot_reply = f"System Error: Backend returned {res.status_code}"
                            except Exception as e:
                                bot_reply = f"I cannot connect to the backend logic engine right now. Ensure the FastAPI instance is running on port 8000. Error: {e}"
                            
                            st.markdown(bot_reply)
                            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                            st.rerun()


