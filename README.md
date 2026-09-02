# fitness-app
Fitness tracker synced to Notion, with an LLM-generated weekly workout plan based on logged progress

<br>

# Core Functionalities:
- Activity logging: log workout sessions
- Progress dashboard: notion page showing workout history over time
- Weekly AI generated workout plan: tailored plan based on past performance
- System reliability: logging and notification service

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

The scheduler has a narrow requirement: queue and execute a single task type (`run_sync`) on a fixed daily schedule, or on demand. This corresponds to a single producer and a single consumer. Kafka and Azure Event Hub are designed for high-throughput, durable, and replayable event streams consumed independently by multiple consumer groups, none of which apply to this use case. Introducing either would add considerable operational overhead without a corresponding benefit at this scale.

Within this design, Redis functions as the Celery message broker rather than as a cache. Its list and publish/subscribe primitives are sufficient to implement a basic task queue, which is the specific function Celery requires. Caching is the most common use case for Redis, but it is not the only one.

Upstash was selected as the Redis provider specifically because it is serverless and billed on a pay-per-request basis, which aligns better with a Railway deployment than provisioning and maintaining a persistent, self-hosted Redis instance.

**Neon over a self-hosted PostgreSQL instance**

Neon removes the operational responsibility of provisioning, patching, and scaling a database server. Its ability to scale to zero when idle is well suited to an application with intermittent traffic, such as a personal fitness tracker.


<br>

# Local Development
### data-sync
- Run `source venv/bin/activate` in the data-sync directory to activate the virtual environment
- Run `uvicorn app.main:app --reload` to start the server
- To call the sync endpoint: run `curl -X POST http://127.0.0.1:8000/sync` in another terminal
- If port is already in use:
    - Run `lsof -i :8000` to find the running pid
    - Kill the process `kill -9 <pid>`

### dashboard
- Run `source venv/bin/activate` in the dashboard directory to activate the virtual environment
- Run `streamlit run app.py` to launch the streamlit application

### ai-service
- Run `source venv/bin/activate` in the ai-service directory to activate the virtual environment
- Run `uvicorn app.main:app --reload --port 8001` to start the server
- If port is already in use:
    - Run `lsof -i :8001` to find the running pid
    - Kill the process `kill -9 <pid>`

### scheduler
- Run `source venv/bin/activate` in the scheduler directory to activate the virtual environment
- To test, open 2 terminals
    - Terminal 1 - worker
        - `cd scheduler` and `source venv/bin/activate`
        - `celery -A app.celery_app worker --loglevel=info`
    - Terminal 2 - trigger manually to test
        - `cd scheduler` and `source venv/bin/activate`
        - `python -c "from app.tasks import run_sync; run_sync.delay()"`
        - In terminal 1 (worker), the /sync endpoint is called
    - Terminal 3 - test Beat separately once above 2 are completed
        - `celery -A app.celery_app beat --loglevel=info`