# data-sync

data-sync is the central FastAPI service of the fitness-app system. It is responsible for reading activity entries from a Notion database, normalizing and persisting them into a PostgreSQL database (Neon), and exposing statistics endpoints that are consumed by the dashboard service. It is also the only service with direct read/write access to the database; both the dashboard and the AI service retrieve activity data through this service rather than querying the database directly.

<br>

# Project Structure

### App Directory (`app/`)
- `main.py`: The FastAPI entry point. Defines every HTTP endpoint exposed by this service, including the sync trigger, the statistics endpoints, and the workout plan storage endpoints.
- `sync.py`: Contains the upsert logic that writes mapped Notion data into the database. Activities are upserted by their Notion page id, and sport-specific detail rows are upserted by their parent activity id.
- `stats.py`: Contains the query functions that compute the statistics served through the API, such as per-sport summaries, weekly summaries, and climbing-specific aggregations.
- `property_mapper.py`: Extracts and normalizes raw values from a Notion page object into the internal field names used elsewhere in this service.
- `constants.py`: Maps internal field keys (for example, `sport_type`) to the corresponding property names actually configured in the Notion database.
- `models.py`: Defines the database schema as SQLModel table classes.
- `notion_client.py`: A thin wrapper around calls to the Notion API.

### Docs Directory (`docs/`)
- `alembic.md`: Explains how to generate and apply versioned schema migrations, and documents cases that require manual review, such as column renames.
- `schema.md`: Documents the database schema, including primary keys, foreign keys, and data types for every table.
- `notion-integration.md`: Documents how to establish the Neon database connection and how to run this FastAPI server locally.

### Tests Directory (`tests/`)
- `test_connection.py`: Verifies the connection to the Neon database.
- `test_seed.py`: Verifies that seed data can be inserted into the database.
- `test_notion.py`: Verifies the connection to the Notion database.
- `test_mapper.py`: Verifies that values are correctly extracted from a raw Notion page object.

<br>

# Environment Variables
The following variables must be defined in a `.env` file in this directory:
- `DATABASE_URL`: The Neon PostgreSQL connection string.
- `NOTION_API_KEY`: The integration token used to authenticate with the Notion API.
- `NOTION_WORKOUT_LOG_DB_ID`: The id of the Notion database containing logged activities.

<br>

# Virtual Environment
Creating the virtual environment:
- Change directory into the data-sync folder: `cd data-sync`
- Create a virtual environment: `python3 -m venv venv`

Activating the virtual environment:
- Activate the virtual environment:
    - `source venv/bin/activate` (macOS/Linux)
    - `venv\Scripts\activate` (Windows)
- Install dependencies (only required the first time, or after `requirements.txt` changes): `pip install -r requirements.txt`

<br>

# API Endpoints
| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | `/sync` | Triggers a sync of all activity pages from Notion into the database. |
| GET | `/stats/weekly` | Returns a summary of activity over the last N days. Implemented, but not yet surfaced in the dashboard UI. |
| GET | `/stats/climbing` | Returns per-climb statistics (date, gym, grade, attempts, sent). |
| GET | `/stats/climbing/by-gym` | Returns aggregated climbing statistics grouped by gym. |
| GET | `/stats/strength` | Returns strength session statistics. |
| GET | `/stats/running` | Returns running session statistics. |
| GET | `/stats/yoga` | Returns yoga session statistics. |
| GET | `/stats/diving` | Returns diving session statistics. |
| GET | `/stats/overview` | Returns a count of sessions per sport over the last N days. |
| GET | `/stats/duration` | Returns aggregated session duration statistics, optionally filtered by sport. |
| GET | `/activities` | Returns raw activity records, optionally filtered by date range or sport type. |
| POST | `/plans` | Persists a generated workout plan (produced by ai-service). |
| GET | `/plans/latest` | Returns the most recently generated plan of a given type. |

<br>

# Potential Errors
1. When running `alembic upgrade head`, `NameError: name 'sqlmodel' is not defined`.
   - Under the affected versioned migration file, add `import sqlmodel`.

<br>

# R&D: Tech Stack
Comparison of the database hosting options considered for this project. See the root [README.md](../README.md) for the final rationale.

|       | Neon | Supabase | Self-hosted Postgres |
| ----- | ---- | -------- | -------------------- |
| What it is | Managed serverless Postgres. | Managed Postgres bundled with auth, storage, and realtime features. | A Postgres server that you provision and operate yourself. |
| Cost at this scale | Free tier is sufficient. | Free tier is sufficient. | Free, if using existing VM resources; otherwise incurs hosting cost. |
| Operational burden | None. | None. | The container must remain running, and backups and upgrades must be handled manually. |
| Auth / extra features | Not included (bare Postgres). | Included: auth, storage, realtime subscriptions, edge functions. | Not included. |
| Availability | Managed and always available. | Managed and always available. | Dependent on the availability of the self-managed host. |