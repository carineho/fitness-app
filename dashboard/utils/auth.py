import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def require_auth():
    """Gate the current page behind a shared password. Call at the top of every page."""
    if st.session_state.get("authenticated"):
        return

    st.title("🔒 Login required")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        expected = os.environ.get("DASHBOARD_PASSWORD")
        if not expected:
            st.error("DASHBOARD_PASSWORD is not set on the server.")
        elif password == expected:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()
