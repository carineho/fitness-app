import streamlit as st
import pandas as pd
from utils.api_client import generate_weekly_plan, generate_adhoc_session

st.title("Generate Workout Plan")

plan_mode = st.radio("Plan type", ["Weekly plan", "Single session (ad-hoc)"])

col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox("Difficulty", ["Easy", "Moderate", "Hard"])
    focus_area = st.text_input("Focus area (optional)", placeholder="e.g. core, climbing endurance")
with col2:
    duration = st.number_input("Preferred duration (minutes)", min_value=10, max_value=180, value=45, step=5)
    remarks = st.text_area("Remarks (optional)", placeholder="e.g. rest days Monday/Thursday, training for a half marathon, go easy on left knee") if plan_mode == "Weekly plan" else None

sport_type = None
if plan_mode == "Single session (ad-hoc)":
    sport_type = st.selectbox("Sport", ["Climbing", "Strength", "Running", "Yoga", "Diving"])

if st.button("Generate Plan", type="primary"):
    with st.spinner("Generating..."):
        if plan_mode == "Weekly plan":
            result = generate_weekly_plan(difficulty, focus_area, remarks, duration)
            if result:
                st.success("Weekly plan generated!")
                for session in result["sessions"]:
                    with st.expander(f"{session['day']} — {session['sport_type']} ({session['duration_minutes']} min, {session['intensity']} intensity)"):
                        if session.get("exercises"):
                            ex_df = pd.DataFrame(session["exercises"])
                            st.table(ex_df)
                        st.write(session["notes"])
                st.caption(f"**Rationale:** {result['rationale']}")
        else:
            result = generate_adhoc_session(difficulty, sport_type, focus_area, duration)
            if result:
                st.success("Session generated!")
                session = result["session"]
                df = pd.DataFrame([session])
                st.table(df)
                st.caption(f"**Rationale:** {result['rationale']}")