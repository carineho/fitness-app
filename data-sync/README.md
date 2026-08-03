# Project Structure
This fitness application provides the following functionalities:
1. Activity logging
2. Progress dashboard
3. Weekly AI-generated workout plan
4. Weekly progress summary

### App Directory
- `main.py` is the entry point to the application
- `sync.py` provides methods to sync the data from notion database to Neon DB
- `stats.py` provides methods to obtain statistics of workouts
- `property_mapper.py` extracts the values from notion database
- `models.py` has the DB schema
- `notion_client.py` provides the connection to the notion database


### Docs Directory
- `alembic.md` provides details on using the versioned SQL scripts, as detailed by the schema in models
- `schema.md` provides details on the DB schema, including the primary keys, foreign keys and the data type
- `notion-integration.md` provides details on running the FastAPI server


### Tests Directory
- `test_connection.py` tests the connection to the Neon DB
- `test_seed.py` tests the seeding of data into the DB
- `test_notion.py` tests the connection to the notion DB
- `test_mapper.py` tests the extraction of values from notion DB


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