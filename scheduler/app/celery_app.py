import os
# import ssl
from pathlib import Path
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# celery_app = Celery(
#     "scheduler",
#     broker=os.environ["REDIS_URL"],
#     include=["app.tasks"],
#     broker_use_ssl={"ssl_cert_reqs": ssl.CERT_REQUIRED},
# )

celery_app = Celery("scheduler", broker=os.environ["REDIS_URL"], include=["app.tasks"])

celery_app.conf.beat_schedule = {
    "daily-sync": {
        "task": "app.tasks.run_sync",
        "schedule": crontab(hour=6, minute=0),
    },
}
celery_app.conf.timezone = "Asia/Singapore"