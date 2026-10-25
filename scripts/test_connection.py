import os
import psycopg

host = os.getenv("PGHOST", "localhost")
port = int(os.getenv("PGPORT", "5432"))
database = os.getenv("PGDATABASE", "healthcare_billing")
username = os.getenv("PGUSER", "postgres")
password = os.getenv("PGPASSWORD")

if not password:
    raise SystemExit(
        "Set the PGPASSWORD environment variable before running this script."
    )

try:
    with psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=username,
        password=password,
        connect_timeout=10,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT current_database(), current_user, version();"
            )
            db_name, db_user, version = cur.fetchone()

            print("\nConnection successful!")
            print("Database:", db_name)
            print("User:", db_user)
            print("PostgreSQL:", version.split(",")[0])

            cur.execute("""
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name IN ('raw', 'staging', 'warehouse', 'reporting')
                ORDER BY schema_name;
            """)
            schemas = ", ".join(row[0] for row in cur.fetchall())
            print("Project schemas:", schemas)

except psycopg.OperationalError:
    raise SystemExit(
        "Connection failed. Check PostgreSQL availability and environment settings."
    )
