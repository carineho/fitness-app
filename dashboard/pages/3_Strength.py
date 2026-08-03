import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_strength_stats

st.title("Strength")

data = get_strength_stats()

if not data:
    st.info("No strength data yet — log a session and sync.")
else:
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    st.subheader("Sessions by body area")
    counts = df["body_area"].value_counts().reset_index()
    counts.columns = ["body_area", "count"]
    fig = px.bar(counts, x="body_area", y="count")
    st.plotly_chart(fig, width='stretch')

    st.subheader("Session history")
    st.dataframe(df.sort_values("date", ascending=False))