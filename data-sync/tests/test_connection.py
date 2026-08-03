import os
from pathlib import Path

from dotenv import load_dotenv
import psycopg2

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
cur = conn.cursor()

# Purge all data in the tables
cur.execute("DELETE FROM climb; DELETE FROM climbsession;")
cur.execute("DELETE FROM exercise; DELETE FROM strengthsession;")
cur.execute("DELETE FROM rundetail; DELETE FROM yogadetail; DELETE FROM divedetail;")
cur.execute("DELETE FROM activity;")
conn.commit()

# Count the number of rows in Activity table
cur.execute("SELECT COUNT(*) FROM activity;")

# Execute simple command to get SQL version
cur.execute("SELECT version();")

print(cur.fetchone())
conn.close()