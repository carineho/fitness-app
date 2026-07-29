from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    notion_page_id: str = Field(unique=True, index=True)
    date: date
    sport_type: str
    notes: Optional[str] = None

class ClimbSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    gym: str

class Climb(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    climb_session_id: int = Field(foreign_key="climbsession.id")
    grade_raw: str
    grade_normalized: Optional[float] = None
    attempts: Optional[int] = None
    sent: Optional[bool] = None # climb completed (True / False)

class RunDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    distance_km: float
    pace_min_per_km: float

class YogaDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    yoga_type: str
    duration_minutes: int

class DiveDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    dive_site: str
    duration_minutes: int
    max_depth_m: float

class StrengthSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    body_area: str

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    strength_session_id: int = Field(foreign_key="strengthsession.id")
    exercise_name: str
    exercise_type: str          # "reps" or "time"
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None   # for time-based, e.g. planks

class GradingSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gym: str
    raw_grade: str
    normalized_value: float