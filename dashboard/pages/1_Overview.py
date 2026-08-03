import streamlit as st
from utils.api_client import get_overview_stats

st.title("Overview")

days = st.selectbox("Time range", [7, 30, 90], index=0)
data = get_overview_stats(days=days)

st.metric("Total sessions", data["total_sessions"])

st.subheader("By sport type")
st.bar_chart(data["by_sport"])