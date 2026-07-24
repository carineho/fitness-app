from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    sport_type: str
    notes: Optional[str] = None

class ClimbDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    gym: str
    grade_raw: str
    grade_normalized: Optional[float] = None

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

class StrengthDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    duration_minutes: int
    body_area: str

class GradingSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gym: str
    raw_grade: str
    normalized_value: float