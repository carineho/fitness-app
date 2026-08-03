# Alembic
### Database migration:
- After installing alembic, initialize the migrations with `alembic init migrations`
- To update the database schema
    - Edit `models.py`
    - Run the command (in the data-sync directory) `alembic revision --autogenerate -m "describe the change"`
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
