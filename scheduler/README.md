# scheduler

The scheduler service is responsible for automatically triggering the Notion-to-database sync on a recurring schedule, in addition to supporting manual, on-demand triggers for testing. It does not expose an HTTP API; it runs as a set of background processes built on Celery.

<br>

# Project Structure
- `app/celery_app.py`: Configures the Celery application, including the broker connection (Redis/Upstash), the timezone, and the Beat schedule that determines when tasks run automatically.
- `app/tasks.py`: Defines the Celery tasks. Currently, this contains a single task, `run_sync`, which sends a `POST` request to the `data-sync` service's `/sync` endpoint.

<br>

# Concepts
- Celery is a distributed task queue. It allows a function to be executed asynchronously, in a separate worker process, rather than synchronously in the calling process.
- Redis (Upstash) acts as the message broker, meaning it is where queued tasks are held until a worker is available to process them. It is not being used as a cache in this context; see the root [README.md](../README.md) for further detail on this distinction.
- The Celery worker (`celery -A app.celery_app worker`) is the process that picks up queued tasks and executes them. This is the process that actually executes `run_sync` and performs the real HTTP call to `/sync`.
- The `@celery_app.task` decorator marks a normal Python function as executable via the queue. This is why calling `run_sync.delay()` enqueues the task for a worker to pick up, rather than executing it immediately in the calling process.
- Beat is a separate scheduler process that periodically adds tasks to the same queue, according to the schedule defined in `celery_app.conf.beat_schedule`. The Beat schedule and the worker are independent processes and must both be running for automatic execution to occur; running Beat alone only enqueues tasks, and running the worker alone only allows manually or externally enqueued tasks to be processed.

Currently, the only scheduled job is `daily-sync`, which runs once per day at 06:00 in the `Asia/Singapore` timezone, as configured in `app/celery_app.py`.

<br>

# Environment Variables
The following variables must be defined in a `.env` file in this directory:
- `REDIS_URL`: The Upstash Redis connection string used as the Celery broker.
- `DATA_SYNC_URL`: The base URL of the data-sync service, called by the `run_sync` task.
- `AI_SERVICE_URL`: The base URL of the ai-service, reserved for future tasks that may need to call it directly; not currently used by any task in `app/tasks.py`.

<br>

# Virtual Environment
Creating the virtual environment:
- Change directory into the scheduler folder: `cd scheduler`
- Create a virtual environment: `python3 -m venv venv`

Activating the virtual environment:
- Activate the virtual environment:
    - `source venv/bin/activate` (macOS/Linux)
    - `venv\Scripts\activate` (Windows)
- Install dependencies (only required the first time, or after `requirements.txt` changes): `pip install -r requirements.txt`

<br>

# Local Development

Note that `data-sync` should already be running locally (see [../data-sync/README.md](../data-sync/README.md)), since `run_sync` calls its `/sync` endpoint directly.

### Worker
In terminal 1, run the following commands:
```
# terminal 1 — worker
cd scheduler
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

<br>

### Trigger Sync Manually
In terminal 2, run the following commands:
```
# terminal 2 — trigger manually, to test the task without waiting for the schedule
cd scheduler
source venv/bin/activate
python -c "from app.tasks import run_sync; run_sync.delay()"
```

This step is verified as successful when terminal 1 (the worker) logs that the task was received and executed, printing a sync result equivalent to a direct `curl -X POST http://127.0.0.1:8000/sync` call.

<br>

### Test Beat
In terminal 3, run the following commands:
```
# terminal 3 — beat scheduler
cd scheduler
source venv/bin/activate
celery -A app.celery_app beat --loglevel=info
```

This step is verified as successful when the log shows the `daily-sync` task registered with the correct next scheduled run time, or when it logs `Scheduler: Sending due task daily-sync` at the scheduled time. This confirms that the automatic daily schedule is registered correctly, separately from the manual trigger verified above.

<br>

# Future Improvements
- **Broker connection over TLS with certificate verification**: `app/celery_app.py` contains a commented-out `broker_use_ssl={"ssl_cert_reqs": ssl.CERT_REQUIRED}` option. This setting, if the broker connection uses the `rediss://` scheme, would enforce verification of the broker's TLS certificate rather than only encrypting the connection without verifying the certificate presented by the server. This would harden the connection to Upstash against interception, and should be revisited once it is confirmed whether `REDIS_URL` is already using the `rediss://` scheme.