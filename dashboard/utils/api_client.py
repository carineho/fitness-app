import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.environ["DATA_SYNC_URL"]

def get_climbing_stats():
    response = requests.get(f"{BASE_URL}/stats/climbing")
    response.raise_for_status()
    return response.json()

def get_overview_stats(days: int = 7):
    response = requests.get(f"{BASE_URL}/stats/overview", params={"days": days})
    response.raise_for_status()
    return response.json()