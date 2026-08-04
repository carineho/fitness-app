from pydantic import BaseModel, Field
from typing import Literal

class WorkoutSession(BaseModel):
    day: str = Field(description="Day of week, e.g. Monday, or 'Ad-hoc' for single sessions")
    sport_type: Literal["Climbing", "Strength", "Running", "Yoga", "Diving", "Rest"]
    focus_area: str | None = Field(default=None, description="e.g. arms, core, legs — for strength sessions")
    intensity: Literal["Low", "Moderate", "High"]
    duration_minutes: int
    notes: str = Field(description="Specific guidance, e.g. exercises, target pace, target grade")

class WeeklyPlan(BaseModel):
    sessions: list[WorkoutSession]
    rationale: str = Field(description="Brief explanation of why this plan was chosen, referencing past week's activity")

class AdhocSession(BaseModel):
    session: WorkoutSession
    rationale: str

class PlanRequest(BaseModel):
    difficulty: Literal["Easy", "Moderate", "Hard"] = "Moderate"
    focus_area: str | None = Field(default=None, description="e.g. 'core' or 'climbing endurance' — a specific body area or skill to emphasize")
    remarks: str | None = Field(default=None, description="Any other context: upcoming events, scheduling constraints, injuries, preferences")
    preferred_duration_minutes: int | None = None

class AdhocRequest(BaseModel):
    difficulty: Literal["Easy", "Moderate", "Hard"] = "Moderate"
    sport_type: Literal["Climbing", "Strength", "Running", "Yoga", "Diving"] | None = None
    focus_area: str | None = None
    duration_minutes: int | None = None

class ExercisePrescription(BaseModel):
    exercise_name: str
    exercise_type: Literal["reps", "time"]
    sets: int | None = None
    reps: int | None = None
    target_weight_kg: float | None = Field(default=None, description="Suggested weight, if applicable — omit if bodyweight")
    duration_seconds: int | None = None

class WorkoutSession(BaseModel):
    day: str
    sport_type: Literal["Climbing", "Strength", "Running", "Yoga", "Diving", "Rest"]
    focus_area: str | None = None
    intensity: Literal["Low", "Moderate", "High"]
    duration_minutes: int
    exercises: list[ExercisePrescription] | None = Field(default=None, description="Detailed exercise breakdown, mainly for Strength sessions")
    notes: str = Field(description="General guidance — target pace for runs, target grade for climbing, etc.")