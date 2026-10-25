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
            SELECT 'patient' AS table_name, COUNT(*) AS row_count FROM warehouse.patient
            UNION ALL SELECT 'encounter', COUNT(*) FROM warehouse.encounter
            UNION ALL SELECT 'claim', COUNT(*) FROM warehouse.claim
            UNION ALL SELECT 'claim_line', COUNT(*) FROM warehouse.claim_line
            UNION ALL SELECT 'payment', COUNT(*) FROM warehouse.payment
            UNION ALL SELECT 'denial', COUNT(*) FROM warehouse.denial
            UNION ALL SELECT 'adjustment', COUNT(*) FROM warehouse.adjustment
            ORDER BY table_name;
        """)
        for table_name, row_count in cur.fetchall():
            print(f"{table_name}: {row_count:,}")

