import streamlit as st
from utils.api_client import trigger_sync

st.set_page_config(page_title="Fitness Dashboard", layout="wide")
st.title("Fitness Dashboard")
st.write("Select a page from the sidebar to view detailed stats.")

with st.sidebar:
    st.divider()
    if st.button("🔄 Sync Now", use_container_width=True):
        with st.spinner("Syncing from Notion..."):
            result = trigger_sync()
            if result:
                synced = result.get("synced", {})
                st.success(f"Synced {synced.get('synced', 0)} activities")
                if synced.get("skipped"):
                    st.warning(f"{len(synced['skipped'])} skipped")