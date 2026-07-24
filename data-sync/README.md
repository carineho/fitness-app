# Setup
### DB Connection
- After creating a Neon project, there will be a connection string
- Run `brew install postgresql` and then `psql --version` to verify the installation
- Connect to the database with `psql "postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"`
- When the connection in successful, there will be the database name
- Run `SELECT version();` to verify
- Create .env file in the data-sync folder, putting the variable
    - DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
- Run `python test-connection.py` to verify connection


### Virtual Environment
Creating virtual environment:
- Change directory into the data-sync folder `cd data-sync`
- Create a virtual environment `python3 -m venv venv`

Activating virtual environment:
- Activate the virtual environment
    - `source venv/bin/activate`       # macOS/Linux
    - `venv\Scripts\activate`       # Windows
- Install dependencies `pip install fastapi sqlmodel uvicorn psycopg2-binary python-dotenv alembic`


### Alembic
Database migration:
- After installing alembic, initialize the migrations with `alembic init migrations`
- To update the database schema
    - Edit `models.py`
    - Run the command `alembic revision --autogenerate -m "describe the change"`
    - Review the generated file in `migrations/versions/`
    - Run the command `alembic upgrade head`
    - Verify the tables are created / altered
- To revert the last migration, run `alembic downgrade -1`
- Autogenerate handles well for
    - Adding new tables / columns
    - Adding constraints (foreign key, unique, not null on new columns)
    - Deleting tables / columns
- Where we need to be involved:
    - Renames — Alembic's autogenerate can't tell "renamed column" from "dropped old column + added new column." It'll generate a drop+add, which deletes the data in that column. For a rename, you need to manually edit the generated migration to use `op.alter_column(..., new_column_name=...)` instead.
    - Constraint changes on existing columns (e.g. making a nullable column NOT NULL) — autogenerate often misses these or generates something that fails if existing rows violate the new constraint. Always review the generated file before running upgrade.
    - Data migrations (e.g. backfilling a new column from existing data) — autogenerate only handles schema, not data. You'd write that logic manually inside the migration file.


# DB Tables
- To be updated


# Potential Errors
1. When running `alembic upgrade head`, NameError: name 'sqlmodel' is not defined
- Under the versioned file, add this `import sqlmodel`
