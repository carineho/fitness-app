import os
import requests

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

def query_database(database_id: str) -> list[dict]:
    """Return all pages (rows) in a Notion database."""
    url = f"{BASE_URL}/databases/{database_id}/query"
    results = []
    payload = {}

    while True:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        results.extend(data["results"])

        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]

    return results