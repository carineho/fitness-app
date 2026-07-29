from dotenv import load_dotenv
import os
import sys
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.notion_client import query_database
from app.property_mapper import map_page_to_activity_fields

pages = query_database(os.environ["NOTION_WORKOUT_LOG_DB_ID"])
mapped = map_page_to_activity_fields(pages[0])
print(mapped)