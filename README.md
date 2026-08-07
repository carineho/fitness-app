# fitness-app
Fitness tracker synced to Notion, with an LLM-generated weekly workout plan based on logged progress

<br>

# Core Functionalities:
- Activity logging: log workout sessions
- Progress dashboard: notion page showing workout history over time
- Weekly AI generated workout plan: tailored plan based on past performance
- System reliability: logging and notification service

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

<br>

# Tech Stack
The following tech stack is used:
- Neon: serverless cloud service built on top of the open-source PostgreSQL database
- Alembic: for database migration
- Pydantic: enforce schema
- Pydantic AI
- FastAPI
- Groq
- Streamlit