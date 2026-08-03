import streamlit as st
from utils.api_client import get_overview_stats
import requests
import os

st.title("Overview")

days = st.selectbox("Time range", [7, 30, 90], index=0)
data = get_overview_stats(days=days)

st.metric("Total sessions", data["total_sessions"])

st.subheader("By sport type")
st.bar_chart(data["by_sport"])

st.subheader("Exercise Duration")

sport_filter = st.selectbox("Filter by sport", ["All", "Climbing", "Strength", "Running", "Yoga", "Diving"])
params = {} if sport_filter == "All" else {"sport_type": sport_filter}

duration_data = requests.get(f"{os.environ['DATA_SYNC_URL']}/stats/duration", params=params).json()

col1, col2, col3 = st.columns(3)
col1.metric("Total minutes", duration_data["total_minutes"])
col2.metric("Average minutes/session", duration_data["average_minutes"])
col3.metric("Sessions with duration logged", duration_data["count"])

if duration_data["by_sport"]:
    st.bar_chart({sport: v["total_minutes"] for sport, v in duration_data["by_sport"].items()})