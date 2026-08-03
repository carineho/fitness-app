import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_climbing_stats

st.title("Climbing")

data = get_climbing_stats()

if not data:
    st.info("No climbing data yet — log a session and sync.")
else:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    gyms = st.multiselect("Filter by gym", options=df["gym"].unique(), default=df["gym"].unique())
    filtered = df[df["gym"].isin(gyms)]

    fig = px.scatter(
        filtered, x="date", y="grade_normalized", color="gym",
        symbol="sent", hover_data=["grade_raw", "attempts"],
        title="Grade progression over time"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw data")
    st.dataframe(filtered)