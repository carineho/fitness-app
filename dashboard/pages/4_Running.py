import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_running_stats

st.title("Running")

data = get_running_stats()

if not data:
    st.info("No running data yet — log a session and sync.")
else:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total runs", len(df))
    col2.metric("Total distance (km)", round(df["distance_km"].sum(), 1))
    col3.metric("Avg pace (min/km)", round(df["pace_min_per_km"].mean(), 2))

    fig = px.line(df, x="date", y="pace_min_per_km", title="Pace over time", markers=True)
    st.plotly_chart(fig, width='stretch')

    fig2 = px.bar(df, x="date", y="distance_km", title="Distance per run")
    st.plotly_chart(fig2, width='stretch')

    st.subheader("Run history")
    st.dataframe(df.sort_values("date", ascending=False))