# Setup
### Verifying DB Connection String
- After creating a Neon project, there will be a connection string
- Run `brew install postgresql` and then `psql --version` to verify the installation
- Connect to the database with `psql "postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"`
- When the connection in successful, there will be the database name
- Run `SELECT version();` to verify
- Create .env file in the data-sync folder, putting the variable
    - DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
- Run `python test-connection.py` to verify connection


### Create VENV
- Change directory into the data-sync folder `cd data-sync`
- Create a virtual environment `python3 -m venv venv`
- Activate the virtual environment
    - `source venv/bin/activate`       # macOS/Linux
    - `venv\Scripts\activate`       # Windows
- Install dependencies `pip install fastapi sqlmodel uvicorn psycopg2-binary python-dotenv`


