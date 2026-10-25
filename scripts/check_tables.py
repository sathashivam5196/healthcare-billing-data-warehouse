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
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'warehouse'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()

        print(f"\nWarehouse tables found: {len(tables)}")
        for (table_name,) in tables:
            print(f" - {table_name}")

