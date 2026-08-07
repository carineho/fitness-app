import os
import requests
from dotenv import load_dotenv
from app.celery_app import celery_app

load_dotenv()

DATA_SYNC_URL = os.environ["DATA_SYNC_URL"]

@celery_app.task
def run_sync():
    response = requests.post(f"{DATA_SYNC_URL}/sync")
    print(f"Sync result: {response.status_code} {response.text}")
    return response.json()