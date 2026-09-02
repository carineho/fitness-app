import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_yoga_stats
from utils.auth import require_auth

require_auth()

st.title("Yoga")

data = get_yoga_stats()

if not data:
    st.info("No yoga data yet — log a session and sync.")
else:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    col1, col2 = st.columns(2)
    col1.metric("Total sessions", len(df))
    col2.metric("Most common type", df["yoga_type"].mode()[0] if not df["yoga_type"].mode().empty else "—")

    yoga_types = st.multiselect("Filter by type", options=df["yoga_type"].unique(), default=df["yoga_type"].unique())
    filtered = df[df["yoga_type"].isin(yoga_types)]

    fig = px.bar(filtered, x="date", y="date", color="yoga_type", title="Sessions over time")
    counts = filtered.groupby("yoga_type").size().reset_index(name="count")
    fig = px.pie(counts, names="yoga_type", values="count", title="Sessions by type")
    st.plotly_chart(fig, width='stretch')

    st.subheader("Session history")
    st.dataframe(filtered.sort_values("date", ascending=False))