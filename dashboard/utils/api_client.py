import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.environ["DATA_SYNC_URL"]
AI_SERVICE_URL = os.environ["AI_SERVICE_URL"]

def _get(path: str, params: dict = None):
    """Shared GET helper — handles errors consistently across all endpoints."""
    response = requests.get(f"{BASE_URL}{path}", params=params)
    if response.status_code != 200:
        st.error(f"data-sync returned {response.status_code}: {response.text}")
        return []
    return response.json()


def get_overview_stats(days: int = 7):
    return _get("/stats/overview", params={"days": days})


def get_climbing_stats():
    return _get("/stats/climbing")


def get_climbing_by_gym():
    return _get("/stats/climbing/by-gym")


def get_strength_stats():
    return _get("/stats/strength")


def get_running_stats():
    return _get("/stats/running")


def get_yoga_stats():
    return _get("/stats/yoga")


def get_diving_stats():
    return _get("/stats/diving")


def get_duration_stats(sport_type: str = None):
    params = {"sport_type": sport_type} if sport_type else {}
    return _get("/stats/duration", params=params)


def get_activities(start_date: str = None, end_date: str = None, sport_type: str = None):
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if sport_type:
        params["sport_type"] = sport_type
    return _get("/activities", params=params)


def generate_weekly_plan(difficulty, focus_area, upcoming_event, duration):
    payload = {
        "difficulty": difficulty,
        "focus_area": focus_area or None,
        "upcoming_event": upcoming_event or None,
        "preferred_duration_minutes": duration,
    }
    response = requests.post(f"{AI_SERVICE_URL}/generate-plan", json=payload)
    if response.status_code != 200:
        st.error(f"ai-service returned {response.status_code}: {response.text}")
        return None
    return response.json()


def generate_adhoc_session(difficulty, sport_type, focus_area, duration):
    payload = {
        "difficulty": difficulty,
        "sport_type": sport_type or None,
        "focus_area": focus_area or None,
        "duration_minutes": duration,
    }
    response = requests.post(f"{AI_SERVICE_URL}/generate-session", json=payload)
    if response.status_code != 200:
        st.error(f"ai-service returned {response.status_code}: {response.text}")
        return None
    return response.json()