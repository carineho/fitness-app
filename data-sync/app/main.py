# main.py (add to your existing FastAPI app)
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from sqlmodel import create_engine, Session
from app.notion_client import query_database
from app.property_mapper import map_page_to_activity_fields
from app.sync import sync_notion_to_db
from app.stats import (
    get_climbing_stats, get_climbing_by_gym,
    get_strength_stats, get_running_stats,
    get_yoga_stats, get_diving_stats,
    get_overview_stats, get_activities,
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