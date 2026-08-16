# Celery
- Celery is a distributed task queue
- Redis (Upstash) is the message broker — where tasks get queued
- The Celery worker (celery -A app.celery_app worker) is the process that actually picks up queued tasks and runs them — this is what executed run_sync and made the real /sync HTTP call
- @celery_app.task is just a decorator marking a normal Python function as "runnable via the queue," which is why run_sync.delay() queues it instead of running it immediately in your terminal
- Beat is a scheduler that periodically adds tasks to that same queue, based on a schedule you define

<br>

# Local Development
### Worker
In terminal 1, run the following commands:
```
# terminal 1 — worker
cd scheduler
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

<br>

### Trigger Sync
In terminal 2, run the following commands:
```
# terminal 2 — trigger manually to test
cd scheduler
source venv/bin/activate
python -c "from app.tasks import run_sync; run_sync.delay()"
```

It is completed when terminal 1 shows the task received and executed, printing the sync result matching a normal curl -X POST http://127.0.0.1:8000/sync response.


<br>

### Test Beat
In terminal 3, run the following commands:
```
# terminal 3
cd scheduler
source venv/bin/activate
celery -A app.celery_app beat --loglevel=info
```

It is completed when it logs something like Scheduler: Sending due task daily-sync at the right time, or at minimum shows the task registered with the correct next-run time in its startup log — confirms the automatic schedule is wired correctly, separate from the manual trigger you just verified.