# main.py (add to your existing FastAPI app)
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from sqlmodel import create_engine, Session
from app.notion_client import query_database
from app.property_mapper import map_page_to_activity_fields
from app.sync import sync_notion_to_db
from app.stats import get_climbing_stats

app = FastAPI()
engine = create_engine(os.environ["DATABASE_URL"])

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