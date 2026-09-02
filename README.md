# fitness-app

fitness-app is a personal fitness tracking system that uses Notion as the primary logging interface, while a separate set of services synchronizes that data into a structured database, generates visualizations, and produces LLM-based workout recommendations. The objective is to allow activities to be logged quickly in a familiar tool (Notion), while still supporting the structured querying, historical analysis, and automated planning that a spreadsheet or a Notion page alone cannot easily provide.

The system is composed of four services:

- **data-sync**: A FastAPI service that reads activity entries from a Notion database and synchronizes them into a PostgreSQL database (Neon), normalizing the data into a structured schema and exposing statistics endpoints consumed by the dashboard.
- **ai-service**: A FastAPI service that generates a tailored workout plan using an LLM (Groq), based on recently logged activity retrieved from data-sync.
- **dashboard**: A Streamlit application that visualizes workout history and statistics, and provides a manual sync trigger and a plan generation interface. Access is restricted by a shared password.
- **scheduler**: A Celery-based service that automatically triggers the Notion-to-database sync on a daily schedule, in addition to supporting on-demand triggers.

<br>

# Core Functionalities

- **Activity logging**: Workout sessions are logged directly in Notion, which serves as the source of truth for raw activity data.
- **Automated and on-demand sync**: The scheduler triggers `data-sync` automatically on a daily schedule, and a manual sync can also be triggered at any time from the dashboard.
- **Progress dashboard**: A Streamlit application that queries `data-sync` and renders workout history and statistics as charts, broken down by activity type (climbing, strength, running, yoga, diving).
- **AI-generated workout plan**: `ai-service` generates a tailored workout plan, either as a structured weekly plan or an ad-hoc single session, based on recently logged activity.

### Planned / Roadmap
- **System reliability**: A dedicated logging and notification service is planned but not yet implemented. Currently, service output is limited to standard application logs (for example, Celery worker output and Railway deployment logs).

<br>

# Tech Stack
The following tech stack is used:

- **Neon**: A serverless cloud service built on top of the open-source PostgreSQL database. It scales to zero when idle, which removes the need to provision or maintain a dedicated database server for a personal-scale application. It also supports database branching, which is useful for testing schema changes safely before applying them to production data.
- **Alembic**: A migration tool used alongside SQLModel to apply version-controlled, reversible changes to the database schema. This is particularly important as the schema continues to evolve, since it allows changes to be tracked and rolled back rather than applied manually and irreversibly.
- **Pydantic**: Used to enforce schema validation on data flowing through the FastAPI services. This ensures that malformed data, whether from an external source such as Notion or from an internal API request, fails validation early with a clear error rather than silently entering the database in an inconsistent state.
- **Pydantic AI**: A framework used to structure the interaction with the underlying language model in the AI service. It enforces that the model's output for the generated workout plan conforms to a defined schema, rather than being returned as unstructured free text that would require additional parsing.
- **FastAPI**: An asynchronous Python web framework used to build both the data-sync and ai-service APIs. It was selected primarily for its native integration with Pydantic for request and response validation, along with automatically generated OpenAPI documentation.
- **Groq**: The LLM inference provider used to generate the workout plans. It was selected primarily for its low inference latency, which is significant because the ai-service is called synchronously from the dashboard, meaning the user waits on this call directly.
- **Streamlit**: A Python-native framework used to build the dashboard. It allows a data visualization interface to be built entirely in Python, without requiring a separate frontend stack such as JavaScript or React, which is appropriate for the scale of this internal analytics tool.
- **Celery with Redis (Upstash)**: A background job queue and scheduler used to run the daily Notion-to-database sync automatically, in addition to supporting on-demand manual triggers.

<br>

# Rationale for Key Decisions

**Celery and Redis**
- The scheduler has a narrow requirement: queue and execute a single task type (`run_sync`) on a fixed daily schedule, or on demand. This corresponds to a single producer and a single consumer. Kafka and Azure Event Hub are designed for high-throughput, durable, and replayable event streams consumed independently by multiple consumer groups, none of which apply to this use case. Introducing either would add considerable operational overhead without a corresponding benefit at this scale.
- Within this design, Redis functions as the Celery message broker rather than as a cache. Its list and publish/subscribe primitives are sufficient to implement a basic task queue, which is the specific function Celery requires. Caching is the most common use case for Redis, but it is not the only one.
- Upstash was selected as the Redis provider specifically because it is serverless and billed on a pay-per-request basis, which aligns better with a Railway deployment than provisioning and maintaining a persistent, self-hosted Redis instance.

**Neon over a self-hosted PostgreSQL instance**
- Neon removes the operational responsibility of provisioning, patching, and scaling a database server. Its ability to scale to zero when idle is well suited to an application with intermittent traffic, such as a personal fitness tracker.


<br>

# Local Development

Each service requires its own `.env` file in its respective directory. No `.env.example` files currently exist in this repository, so the required variables are listed explicitly below. None of the services should be committed with real credentials in version control.

Because `dashboard` and `scheduler` call `data-sync` and `ai-service` over HTTP, `data-sync` and `ai-service` should be started first when running the full system locally.

### data-sync
Required environment variables: `DATABASE_URL`, `NOTION_API_KEY`, `NOTION_WORKOUT_LOG_DB_ID`.

- Run `source venv/bin/activate` in the data-sync directory to activate the virtual environment.
- Run `uvicorn app.main:app --reload` to start the server on port 8000.
- To call the sync endpoint, run `curl -X POST http://127.0.0.1:8000/sync` in another terminal.
- If the port is already in use:
    - Run `lsof -i :8000` to find the running process id.
    - Terminate it with `kill -9 <pid>`.

### ai-service
Required environment variables: `GROQ_API_KEY`, `DATA_SYNC_URL`.

- Run `source venv/bin/activate` in the ai-service directory to activate the virtual environment.
- Run `uvicorn app.main:app --reload --port 8001` to start the server.
- If the port is already in use:
    - Run `lsof -i :8001` to find the running process id.
    - Terminate it with `kill -9 <pid>`.

### dashboard
Required environment variables: `DATA_SYNC_URL`, `AI_SERVICE_URL`, `DASHBOARD_PASSWORD` (the password used to access the dashboard locally; this must also be set as an environment variable on the deployed Railway service).

- Ensure `data-sync` and `ai-service` are already running, since every page queries them on load.
- Run `source venv/bin/activate` in the dashboard directory to activate the virtual environment.
- Run `streamlit run app.py` to launch the Streamlit application.
- On first load, enter the value configured in `DASHBOARD_PASSWORD` to access the dashboard.

### scheduler
Required environment variables: `REDIS_URL`, `DATA_SYNC_URL`, `AI_SERVICE_URL`.

- Run `source venv/bin/activate` in the scheduler directory to activate the virtual environment.
- To test, open two terminals:
    - Terminal 1 (worker):
        - `cd scheduler` and `source venv/bin/activate`
        - `celery -A app.celery_app worker --loglevel=info`
    - Terminal 2 (manual trigger, for testing):
        - `cd scheduler` and `source venv/bin/activate`
        - `python -c "from app.tasks import run_sync; run_sync.delay()"`
        - Terminal 1 (worker) should log that the task was received and executed, calling the `/sync` endpoint.
    - Terminal 3 (Beat, tested separately once the above two are confirmed working):
        - `celery -A app.celery_app beat --loglevel=info`
        - This should log the scheduled task with its correct next run time, confirming the automatic daily schedule is registered correctly.