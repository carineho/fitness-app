# Virtual Environment
Creating virtual environment:
- Change directory into the data-sync folder `cd data-sync`
- Create a virtual environment `python3 -m venv venv`

Activating virtual environment:
- Activate the virtual environment
    - `source venv/bin/activate`       # macOS/Linux
    - `venv\Scripts\activate`       # Windows
- Install dependencies (to be done the first time only) `pip install fastapi sqlmodel uvicorn psycopg2-binary python-dotenv alembic`

<br>

# Potential Errors
1. When running `alembic upgrade head`, NameError: name 'sqlmodel' is not defined
- Under the versioned file, add this `import sqlmodel`

<br>

# R&D: Tech Stack
Comparison between the different solutions:

|       | Neon | Supabase | Self-hosted Postgres |
| ----- | ---- | -------- | -------------------- |
| what it is | managed serverless Postgres | managed Postgres + auth / storage / realtime bundle | you run the postgres server |
| cost at your scale | free | free | free (use your own VM resources) |
| ops burden | none | none | container must stay up, you handle backups / upgrades |
| auth / extra features | no (bare Postgres) | yes - auth, storage, realtime, edge functions | no |
| availability | always available | always available | down if your host is down |