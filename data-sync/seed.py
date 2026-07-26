# this is a script to add mock data
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
from datetime import date
from models import Activity, ClimbDetail

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"])

with Session(engine) as session:
    activity = Activity(date = date.today(),
                        sport_type = "climbing",
                        notes = "felt strong")
    session.add(activity)
    session.commit()
    session.refresh(activity)

    print(activity.id)

    climb = ClimbDetail(activity_id = activity.id,
                        gym = "BFF Climb Yoha",
                        grade_raw = "6",
                        grade_normalized = 4.0)
    session.add(climb)
    session.commit()

print("Seeded 1 activity + 1 climb detail")