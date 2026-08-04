from dotenv import load_dotenv
load_dotenv()

import os
from pydantic_ai import Agent
from app.schemas import WeeklyPlan, AdhocSession

WEEKLY_SYSTEM_PROMPT = """You are a fitness coach creating a personalized weekly workout plan.
You will be given the user's activity from the past week and their preferences for the upcoming week.
Balance recovery and progression — don't overload the same body area on consecutive days.
Respect the user's stated difficulty, focus area, and any upcoming event they're training for."""

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