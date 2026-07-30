# DB Connection
- After creating a Neon project, there will be a connection string
- Run `brew install postgresql` and then `psql --version` to verify the installation
- Connect to the database with `psql "postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"`
- When the connection in successful, there will be the database name
- Run `SELECT version();` to verify
- Create .env file in the data-sync folder, putting the variable
    - DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
- Run `python test-connection.py` to verify connection


# FastAPI
### Notion to DB Sync
To test the sync:
- In the data-sync directory, start up the server `uvicorn app.main:app --reload`
- In another terminal, call the endpoint `curl -X POST http://127.0.0.1:8000/sync`
- If port is already in use:
    - Run the command to find the pid: `lsof -i :8000`
    - Kill the process: `kill -9 <pid>`

