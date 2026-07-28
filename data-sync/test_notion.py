from dotenv import load_dotenv

load_dotenv()

from notion_client import query_database
import os

pages = query_database(os.environ["NOTION_WORKOUT_LOG_DB_ID"])
print(f"Found {len(pages)} rows")
print(pages[0]["properties"].keys())