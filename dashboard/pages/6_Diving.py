import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_diving_stats
from utils.auth import require_auth

require_auth()

st.title("Diving")

data = get_diving_stats()

if not data:
    st.info("No diving data yet — log a session and sync.")
else:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total dives", len(df))
    col2.metric("Max depth reached (m)", round(df["max_depth_m"].max(), 1))
    col3.metric("Dive sites visited", df["dive_site"].nunique())

    sites = st.multiselect("Filter by dive site", options=df["dive_site"].unique(), default=df["dive_site"].unique())
    filtered = df[df["dive_site"].isin(sites)]

    fig = px.scatter(filtered, x="date", y="max_depth_m", color="dive_site", size_max=20, title="Depth over time")
    st.plotly_chart(fig, width='stretch')

    st.subheader("Dive history")
    st.dataframe(filtered.sort_values("date", ascending=False))