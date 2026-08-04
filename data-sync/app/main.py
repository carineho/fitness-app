# main.py (add to your existing FastAPI app)
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from sqlmodel import create_engine, Session
from datetime import date as date_type
from app.models import GeneratedPlan
from app.notion_client import query_database
from app.property_mapper import map_page_to_activity_fields
from app.sync import sync_notion_to_db
from app.stats import (
    get_duration_stats,
    get_weekly_summary,
    get_climbing_stats,
    get_climbing_by_gym,
    get_strength_stats,
    get_running_stats,
    get_yoga_stats,
    get_diving_stats,
    get_overview_stats,
    get_activities,
)


app = FastAPI()
engine = create_engine(
    os.environ["DATABASE_URL"],
    pool_pre_ping=True,
    pool_recycle=300,   # recycle connections older than 5 min
)

@app.post("/sync")
def sync():
    pages = query_database(os.environ["NOTION_WORKOUT_LOG_DB_ID"])
    with Session(engine) as session:
        count = sync_notion_to_db(session, pages, map_page_to_activity_fields)
    return {"synced": count}


@app.get("/stats/weekly")
def stats_weekly(days: int = 7):
    with Session(engine) as session:
        return get_weekly_summary(session, days)


@app.get("/stats/climbing")
def stats_climbing():
    with Session(engine) as session:
        return get_climbing_stats(session)


@app.get("/stats/climbing/by-gym")
def stats_climbing_by_gym():
    with Session(engine) as session:
        return get_climbing_by_gym(session)


@app.get("/stats/strength")
def stats_strength():
    with Session(engine) as session:
        return get_strength_stats(session)


@app.get("/stats/running")
def stats_running():
    with Session(engine) as session:
        return get_running_stats(session)


@app.get("/stats/yoga")
def stats_yoga():
    with Session(engine) as session:
        return get_yoga_stats(session)


@app.get("/stats/diving")
def stats_diving():
    with Session(engine) as session:
        return get_diving_stats(session)


@app.get("/stats/overview")
def stats_overview(days: int = 7):
    with Session(engine) as session:
        return get_overview_stats(session, days)


@app.get("/activities")
def activities(start_date: str = None, end_date: str = None, sport_type: str = None):
    with Session(engine) as session:
        return get_activities(session, start_date, end_date, sport_type)


@app.get("/stats/duration")
def stats_duration(sport_type: str = None):
    with Session(engine) as session:
        return get_duration_stats(session, sport_type)


@app.post("/plans")
def save_plan(plan: dict):
    with Session(engine) as session:
        record = GeneratedPlan(
            plan_type=plan["plan_type"],
            generated_at=date_type.today(),
            lookback_days=plan.get("lookback_days"),
            difficulty=plan["difficulty"],
            focus_area=plan.get("focus_area"),
            upcoming_event=plan.get("upcoming_event"),
            sessions=plan["sessions"],
            rationale=plan["rationale"],
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return {"id": record.id}


@app.get("/plans/latest")
def get_latest_plan(plan_type: str = "weekly"):
    with Session(engine) as session:
        statement = (
            select(GeneratedPlan)
            .where(GeneratedPlan.plan_type == plan_type)
            .order_by(GeneratedPlan.generated_at.desc())
        )
        result = session.exec(statement).first()
        return result