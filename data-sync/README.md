# Database Schema
### Activity
The schema uses a shared Activity table for common fields across all sports, with sports-specific details linked via foreign key.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| date | date | when the activity happened |
| sport_type | str | one of: climbing, running, yoga, diving, strength |
| notes | str, optional | free text remarks |


### ClimbSession
One row per climbing session, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| gym | str | gym / location name |


### Climb
One row per individual climb attempted within a session.
| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| climb_session_id | int, foreign key -> ClimbSession.id | links back to the parent session |
| grade_raw | str | grade as reported by the gym |
| grade_normalized | float, optional | grade converted to a shared numeric scale |
| attempts | int, optional | number of tries on this climb |
| sent | whether climb was successfully completed |


### RunDetail
One row per run, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| distance_km | float | distance covered |
| pace_min_per_km | float | average pace |


### YogaDetail
One row per yoga session, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| yoga_type | str | e.g., aerial, vinyasa |
| duration_minutes | int | session length |


### DiveDetail
One row per dive, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| dive_site | str | dive site name |
| duration_minutes | int | dive time |
| max_depth_m | float | maximum depth reached |


### StrengthSession
One row per strength / general workout session, linked to an Activity.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| activity_id | int, foreign key -> Activity.id | links back to parent activity |
| body_area | str | e.g., arms, core, legs |


### Exercise
One row per individual exercise performed within a session

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| strength_session_id | int, foreign key -> StrengthSession.id | links back to parent session |
| exercise_name | str | e,g., bench press, plank |
| exercise_type | str | "reps" or "time" |
| sets | int, optional | number of sets |
| reps | int, optional | reps per set (for rep-based exercises) |
| weight_kg | float, optional | weight used (for rep-based exercises) |
| duration_seconds | int, optional | duration held / performed (for time-based exercises) |


### GradingSystem
Lookup table for converting each gym's raw grade into a shared normalize scale, so climbing progress is comparable across gyms with different grading systems.

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int, primary key | auto-incrementing unique id |
| gym | str | gym / location name |
| raw_grade | str | grade as the gym labels it |
| normalized_value | float | corresponding value on shared internal scale |


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
- Install dependencies (to be done the first time only) `pip install fastapi sqlmodel uvicorn psycopg2-binary python-dotenv alembic`


# Alembic
### Database migration:
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
    - Renames — Alembic's autogenerate cannot tell "renamed column" from "dropped old column + added new column." It will generate a drop+add, which deletes the data in that column. For a rename, you need to manually edit the generated migration to use `op.alter_column(..., new_column_name=...)` instead.
    - Constraint changes on existing columns (e.g. making a nullable column NOT NULL) — Autogenerate often misses these or generates something that fails if existing rows violate the new constraint. Always review the generated file before running upgrade.
    - Data migrations (e.g. backfilling a new column from existing data) — autogenerate only handles schema, not data. You'd write that logic manually inside the migration file.

### Syntax
1. Unique id is auto-incrementing
- `id: Optional[int] = Field(default=None, primary_key=True)`
- SQLModel translates int + primary_key = True into a Postgres SERIAL / IDENTITY column, and then Postgres handles the auto-incrementing

2. Why Optional[int] for id
- Before we insert a row, we do not have the ID yet
- Postgres inserts it at runtime

3. How foreign key works
- `activity_id: int = Field(foreign_key="activity.id")`
- The string "activity-id" is the tablename.columnname
- Tells SQLModel that the column's values must reference the id column of the activity table
- Alembic reads this at autogenerate time and generates a FOREIGN KEY constraint in the DDL, e.g., 
```
ALTER TABLE climbdetail ADD CONSTRAINT climbdetail_activity_id_fkey
FOREIGN KEY (activity_id) REFERENCES activity(id);
```

# Potential Errors
1. When running `alembic upgrade head`, NameError: name 'sqlmodel' is not defined
- Under the versioned file, add this `import sqlmodel`
