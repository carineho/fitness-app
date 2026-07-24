### Verifying DB connection
- After creating a Neon project, there will be a connection string
- Run `brew install postgresql` and then `psql --version` to verify the installation
- Connect to the database with `psql "postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"`
- When the connection in successful, there will be the database name
- Run `SELECT version();` to verify