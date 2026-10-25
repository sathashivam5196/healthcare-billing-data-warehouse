import os
import psycopg
with psycopg.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=int(os.getenv("PGPORT", "5432")),
    dbname=os.getenv("PGDATABASE", "healthcare_billing"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD") or None,
) as conn:
    with conn.cursor() as cur:
        tables = [
            "patient", "provider", "payer", "encounter", "claim",
            "claim_line", "payment", "denial", "adjustment"
        ]

        for table in tables:
            cur.execute(f'SELECT COUNT(*) FROM warehouse."{table}"')
            print(f"{table}: {cur.fetchone()[0]:,} rows")

