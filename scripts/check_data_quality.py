import os
import sys

import psycopg

CHECKS = [
    (
        "Claims without claim lines",
        """
        SELECT COUNT(*)
        FROM warehouse.claim c
        LEFT JOIN warehouse.claim_line cl
            ON c.claim_id = cl.claim_id
        WHERE cl.claim_id IS NULL;
        """,
    ),
    (
        "Claim billed amount mismatches",
        """
        WITH line_totals AS (
            SELECT claim_id, SUM(charge_amount) AS total_billed
            FROM warehouse.claim_line
            GROUP BY claim_id
        )
        SELECT COUNT(*)
        FROM warehouse.claim c
        LEFT JOIN line_totals lt
            ON c.claim_id = lt.claim_id
        WHERE c.billed_amount <> COALESCE(lt.total_billed, 0);
        """,
    ),
    (
        "Claim allowed amount mismatches",
        """
        WITH line_totals AS (
            SELECT claim_id, SUM(allowed_amount) AS total_allowed
            FROM warehouse.claim_line
            GROUP BY claim_id
        )
        SELECT COUNT(*)
        FROM warehouse.claim c
        LEFT JOIN line_totals lt
            ON c.claim_id = lt.claim_id
        WHERE c.allowed_amount <> COALESCE(lt.total_allowed, 0);
        """,
    ),
    (
        "Patient responsibility mismatches",
        """
        SELECT COUNT(*)
        FROM warehouse.claim
        WHERE patient_responsibility <>
              GREATEST(0, billed_amount - allowed_amount);
        """,
    ),
    (
        "Claims submitted before service",
        """
        SELECT COUNT(*)
        FROM warehouse.claim c
        JOIN warehouse.encounter e
            ON c.encounter_id = e.encounter_id
        WHERE c.submitted_date < e.service_date;
        """,
    ),
    (
        "Payment payer mismatches",
        """
        SELECT COUNT(*)
        FROM warehouse.payment p
        JOIN warehouse.claim c
            ON p.claim_id = c.claim_id
        WHERE p.payer_id <> c.payer_id;
        """,
    ),
    (
        "Payments before claim submission",
        """
        SELECT COUNT(*)
        FROM warehouse.payment p
        JOIN warehouse.claim c
            ON p.claim_id = c.claim_id
        WHERE p.payment_date < c.submitted_date;
        """,
    ),
    (
        "Denials before claim submission",
        """
        SELECT COUNT(*)
        FROM warehouse.denial d
        JOIN warehouse.claim c
            ON d.claim_id = c.claim_id
        WHERE d.denial_date < c.submitted_date;
        """,
    ),
    (
        "Adjustments before claim submission",
        """
        SELECT COUNT(*)
        FROM warehouse.adjustment a
        JOIN warehouse.claim c
            ON a.claim_id = c.claim_id
        WHERE a.adjustment_date < c.submitted_date;
        """,
    ),
    (
        "Payment and claim status mismatches",
        """
        WITH payment_summary AS (
            SELECT
                claim_id,
                COUNT(*) AS payment_rows,
                COUNT(*) FILTER (
                    WHERE posting_status = 'Posted'
                ) AS posted_rows,
                COALESCE(
                    SUM(payment_amount) FILTER (
                        WHERE posting_status = 'Posted'
                    ), 0
                ) AS posted_amount
            FROM warehouse.payment
            GROUP BY claim_id
        )
        SELECT COUNT(*)
        FROM warehouse.claim c
        LEFT JOIN payment_summary p
            ON c.claim_id = p.claim_id
        WHERE
            (
                c.claim_status = 'Paid'
                AND (
                    COALESCE(p.payment_rows, 0) <> 1
                    OR COALESCE(p.posted_rows, 0) <> 1
                    OR COALESCE(p.posted_amount, 0) <> c.allowed_amount
                )
            )
            OR
            (
                c.claim_status = 'PartiallyPaid'
                AND (
                    COALESCE(p.payment_rows, 0) <> 1
                    OR COALESCE(p.posted_rows, 0) <> 1
                    OR ABS(
                        COALESCE(p.posted_amount, 0)
                        - c.allowed_amount / 2
                    ) > 0.005
                )
            )
            OR
            (
                c.claim_status NOT IN ('Paid', 'PartiallyPaid')
                AND COALESCE(p.payment_rows, 0) <> 0
            );
        """,
    ),
    (
        "Denial and claim status mismatches",
        """
        WITH denial_summary AS (
            SELECT claim_id, COUNT(*) AS denial_rows
            FROM warehouse.denial
            GROUP BY claim_id
        )
        SELECT COUNT(*)
        FROM warehouse.claim c
        LEFT JOIN denial_summary d
            ON c.claim_id = d.claim_id
        WHERE
            (
                c.claim_status = 'Denied'
                AND COALESCE(d.denial_rows, 0) <> 1
            )
            OR
            (
                c.claim_status <> 'Denied'
                AND COALESCE(d.denial_rows, 0) <> 0
            );
        """,
    ),
]


def main() -> int:
    password = os.getenv("PGPASSWORD")

    if not password:
        print(
            "ERROR: PGPASSWORD is not set. Configure database environment variables.",
            file=sys.stderr,
        )
        return 2

    failed_checks = 0

    try:
        with (
            psycopg.connect(
                host=os.getenv("PGHOST", "localhost"),
                port=int(os.getenv("PGPORT", "5432")),
                dbname=os.getenv("PGDATABASE", "healthcare_billing"),
                user=os.getenv("PGUSER", "postgres"),
                password=password,
            ) as conn,
            conn.transaction(),
        ):
            conn.execute("SET TRANSACTION READ ONLY")

            print("\nHealthcare Billing Data Quality Results")
            print("=" * 60)

            for check_name, query in CHECKS:
                mismatch_count = conn.execute(query).fetchone()[0]

                if mismatch_count == 0:
                    status = "PASS"
                else:
                    status = "FAIL"
                    failed_checks += 1

                print(f"{status:<5} | {check_name}: {mismatch_count:,} mismatches")

        print("=" * 60)
        print(f"Total checks: {len(CHECKS)}")
        print(f"Passed: {len(CHECKS) - failed_checks}")
        print(f"Failed: {failed_checks}")

        if failed_checks:
            print("\nDATA QUALITY VALIDATION FAILED")
            return 1

        print("\nALL DATA QUALITY CHECKS PASSED")
        return 0

    except (psycopg.Error, ValueError) as exc:
        print(f"\nERROR: Data quality validation could not complete: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
