from dotenv import load_dotenv
import os
import sys
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.notion_client import query_database

pages = query_database(os.environ["NOTION_WORKOUT_LOG_DB_ID"])
print(f"Found {len(pages)} rows")
print(pages[0]["properties"].keys())