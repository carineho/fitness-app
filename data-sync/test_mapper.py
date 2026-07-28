from dotenv import load_dotenv
load_dotenv()

import os
from notion_client import query_database
from property_mapper import map_page_to_activity_fields

pages = query_database(os.environ["NOTION_WORKOUT_LOG_DB_ID"])
mapped = map_page_to_activity_fields(pages[0])
print(mapped)