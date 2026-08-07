import os
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from app.schemas import PlanRequest, AdhocRequest, WeeklyPlan, AdhocSession
from app.agent import weekly_agent, adhoc_agent

load_dotenv()
app = FastAPI()

DATA_SYNC_URL = os.environ["DATA_SYNC_URL"]


def build_weekly_prompt(request: PlanRequest, weekly_stats: dict) -> str:
    parts = [f"Past week's activity summary: {weekly_stats}"]
    parts.append(f"Requested difficulty: {request.difficulty}")
    if request.focus_area:
        parts.append(f"Focus area for this week: {request.focus_area}")
    if request.remarks:
        parts.append(f"Additional context/constraints: {request.remarks}")
    if request.preferred_duration_minutes:
        parts.append(f"Preferred session duration: ~{request.preferred_duration_minutes} minutes")
    parts.append("Generate a balanced 7-day plan, including rest days where appropriate.")
    return "\n".join(parts)


def build_adhoc_prompt(request: AdhocRequest) -> str:
    parts = [f"Requested difficulty: {request.difficulty}"]
    if request.sport_type:
        parts.append(f"Sport: {request.sport_type}")
    if request.focus_area:
        parts.append(f"Focus area: {request.focus_area}")
    if request.duration_minutes:
        parts.append(f"Target duration: {request.duration_minutes} minutes")
    parts.append("Generate one single workout session matching these preferences.")
    return "\n".join(parts)


@app.post("/generate-session", response_model=AdhocSession)
def generate_session(request: AdhocRequest):
    prompt = build_adhoc_prompt(request)
    result = adhoc_agent.run_sync(prompt)
    return result.output

@app.post("/generate-plan", response_model=WeeklyPlan)
def generate_plan(request: PlanRequest):
    weekly_stats = requests.get(f"{DATA_SYNC_URL}/stats/weekly").json()
    prompt = build_weekly_prompt(request, weekly_stats)
    result = weekly_agent.run_sync(prompt)
    plan = result.output

    save_payload = {
        "plan_type": "weekly",
        "lookback_days": 7,
        "difficulty": request.difficulty,
        "focus_area": request.focus_area,
        "remarks": request.remarks,
        "sessions": [s.model_dump() for s in plan.sessions],
        "rationale": plan.rationale,
    }
    print(f"Sending payload: {save_payload}")
    save_response = requests.post(f"{DATA_SYNC_URL}/plans", json=save_payload)
    print(f"Save plan response: {save_response.status_code} {save_response.text}")

    return plan