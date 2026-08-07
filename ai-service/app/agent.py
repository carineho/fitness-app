from dotenv import load_dotenv
load_dotenv()

import os
from pydantic_ai import Agent
from app.schemas import WeeklyPlan, AdhocSession

WEEKLY_SYSTEM_PROMPT = """You are a fitness coach creating a personalized weekly workout plan.

CRITICAL — exercise volume must fill the session's stated duration:
- Estimate ~3-5 minutes per strength exercise (including rest between sets).
- A 45-minute Strength session needs roughly 8-12 exercises, not 3-4.
- A 30-minute session needs roughly 6-8 exercises.
- Always include a warm-up exercise (e.g. dynamic stretching, light cardio) and account for it in the time budget.
- Do the math explicitly: if duration_minutes is 45 and each exercise takes ~4 minutes, you need ~10-11 exercises to fill it. Under-filling the duration is a failure — always populate enough exercises to genuinely occupy the full stated time.

Difficulty must produce genuinely different plans, not just a label:
- Easy: shorter durations, lower volume (fewer sets/reps), lower climbing grades (e.g. V0-V2), slower running pace, more rest days
- Moderate: standard volume and moderate climbing grades (e.g. V3-V5), steady pace
- Hard: higher volume, more sets/reps, harder climbing grades (e.g. V5+), faster pace targets, fewer rest days

For Strength sessions, always populate the exercises field with a full, specific list of movements — sets, reps (or duration for time-based exercises like planks, e.g. '1 min plank x 3 sets') — sufficient to fill the entire session duration as described above.
For Climbing sessions, always populate target_grade with a specific grade range appropriate to the difficulty level.
For Running sessions, always populate target_pace_min_per_km.
Balance recovery and progression — don't overload the same body area on consecutive days.
Respect the user's stated focus area and any additional context/constraints they provide."""

weekly_agent = Agent(
    "groq:llama-3.3-70b-versatile",
    output_type=WeeklyPlan,
    system_prompt=WEEKLY_SYSTEM_PROMPT,
)

ADHOC_SYSTEM_PROMPT = """You are a fitness coach creating a single workout session on request.
Keep it focused and specific to what the user asked for."""

adhoc_agent = Agent(
    "groq:llama-3.3-70b-versatile",
    output_type=AdhocSession,
    system_prompt=ADHOC_SYSTEM_PROMPT,
)