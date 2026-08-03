# this is a script to add mock data
import os
import sys
from pathlib import Path
from datetime import date

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import Activity, Climb, ClimbSession

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL)

with Session(engine) as session:
    activity = Activity(
        notion_page_id="seed-test-page",
        date=date.today(),
        sport_type="Climbing",
        notes="felt strong",
    )
    session.add(activity)
    session.commit()
    session.refresh(activity)

    print(activity.id)

    climb_session = ClimbSession(activity_id=activity.id, gym="BFF Climb Yoha")
    session.add(climb_session)
    session.commit()
    session.refresh(climb_session)

    climb = Climb(
        climb_session_id=climb_session.id,
        grade_raw="6",
        grade_normalized=4.0,
        attempts=1,
        sent=True,
    )
    session.add(climb)
    session.commit()

print("Seeded 1 activity + 1 climb session + 1 climb")