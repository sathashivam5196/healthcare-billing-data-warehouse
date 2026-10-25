
import random
from datetime import date, timedelta
from decimal import Decimal

import os
import psycopg
# Initial test batch: increase only after validation.
PATIENT_COUNT = 1000
SEED = 20261025
TODAY = date.today()
START_DATE = TODAY - timedelta(days=730)

random.seed(SEED)


def money(low, high):
    return Decimal(str(round(random.uniform(float(low), float(high)), 2)))


def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def main():
    password = getpass.getpass("PostgreSQL password: ")

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="healthcare_billing",
        user="postgres",
        password=password,
    ) as conn:
        with conn.cursor() as cur:
            # Refuse to load if any target table already contains records.
            target_tables = [
                "patient", "encounter", "claim", "claim_line",
                "payment", "denial", "adjustment",
            ]

            for table in target_tables:
                cur.execute(f"SELECT COUNT(*) FROM warehouse.{table}")
                count = cur.fetchone()[0]
                if count:
                    raise RuntimeError(
                        f"warehouse.{table} already has {count} rows. "
                        "No data was loaded."
                    )

            cur.execute(
                "SELECT provider_id FROM warehouse.provider ORDER BY provider_id"
            )
            provider_ids = [row[0] for row in cur.fetchall()]

            cur.execute(
                "SELECT payer_id FROM warehouse.payer ORDER BY payer_id"
            )
            payer_ids = [row[0] for row in cur.fetchall()]

            if not provider_ids or not payer_ids:
                raise RuntimeError("Provider and payer reference data is required.")

            patients = []
            encounters = []
            claims = []
            claim_lines = []
            payments = []
            denials = []
            adjustments = []

            encounter_id = 0
            claim_line_id = 0
            payment_id = 0
            denial_id = 0
            adjustment_id = 0

            for patient_id in range(1, PATIENT_COUNT + 1):
                patients.append((
                    patient_id,
                    f"SYN-{patient_id:08d}",
                    random_date(date(1935, 1, 1), date(2010, 12, 31)),
                    random.choice(["F", "M", "X", "U"]),
                    f"{random.randint(10000, 99999)}",
                ))

                visit_count = random.choices(
                    [1, 2, 3, 4], weights=[45, 35, 15, 5]
                )[0]

                for _ in range(visit_count):
                    encounter_id += 1
                    service_date = random_date(START_DATE, TODAY)
                    status = random.choices(
                        ["Completed", "Cancelled", "InProgress"],
                        weights=[92, 5, 3],
                    )[0]

                    encounters.append((
                        encounter_id,
                        patient_id,
                        random.choice(provider_ids),
                        service_date,
                        random.choice(["Office", "Emergency", "Ambulatory", "Other"]),
                        random.choice(["11", "22", "23", "24"]),
                        status,
                    ))

                    if status == "Cancelled":
                        continue

                    payer_id = random.choice(payer_ids)
                    submitted_date = min(
                        TODAY, service_date + timedelta(days=random.randint(0, 30))
                    )

                    # Generate lines first so claim header totals match them.
                    line_count = random.randint(1, 3)
                    line_data = []
                    total_billed = Decimal("0.00")
                    total_allowed = Decimal("0.00")

                    for line_number in range(1, line_count + 1):
                        charge = money(50, 900)
                        allowed = min(
                            charge,
                            money(charge * Decimal("0.45"), charge * Decimal("0.95")),
                        )
                        total_billed += charge
                        total_allowed += allowed
                        claim_line_id += 1

                        line_data.append((
                            claim_line_id,
                            encounter_id,
                            line_number,
                            random.choice(["99213", "99214", "93000", "80053", "A0429"]),
                            random.choice(["R05.9", "I10", "E11.9", "S09.90XA", "Z00.00"]),
                            Decimal("1.00"),
                            charge,
                            allowed,
                        ))

                    claim_lines.extend(line_data)

                    claim_status = random.choices(
                        ["Submitted", "Accepted", "Denied", "Paid",
                         "PartiallyPaid", "Rejected", "Pending"],
                        weights=[12, 10, 12, 35, 15, 6, 10],
                    )[0]

                    patient_responsibility = max(
                        Decimal("0.00"), total_billed - total_allowed
                    )

                    claims.append((
                        encounter_id, encounter_id, payer_id,
                        f"SYN-CLM-{encounter_id:010d}",
                        submitted_date, claim_status, total_billed,
                        total_allowed, patient_responsibility,
                    ))

                    if claim_status in ("Paid", "PartiallyPaid"):
                        payment_id += 1
                        amount = (
                            total_allowed
                            if claim_status == "Paid"
                            else (total_allowed / Decimal("2")).quantize(
                                Decimal("0.01")
                            )
                        )
                        payments.append((
                            payment_id, encounter_id, payer_id,
                            min(TODAY, submitted_date + timedelta(
                                days=random.randint(5, 90)
                            )),
                            random.choice(["EFT", "Check", "ERA"]),
                            max(Decimal("0.01"), amount), "Posted",
                        ))

                    if claim_status == "Denied":
                        denial_id += 1
                        denials.append((
                            denial_id, encounter_id,
                            min(TODAY, submitted_date + timedelta(
                                days=random.randint(1, 45)
                            )),
                            random.choice(["CO16", "CO97", "PR204", "CO50"]),
                            random.choice([
                                "Missing Information", "Bundled Service",
                                "Authorization", "Medical Necessity",
                            ]),
                            random.choice(["Open", "Appealed", "Resolved", "WrittenOff"]),
                        ))

                    if random.random() < 0.20:
                        adjustment_id += 1
                        adjustments.append((
                            adjustment_id, encounter_id,
                            min(TODAY, submitted_date + timedelta(
                                days=random.randint(5, 120)
                            )),
                            random.choice(["CONTRACT", "WRITE_OFF", "CORRECTION"]),
                            random.choice(["Contractual", "WriteOff", "Correction", "Other"]),
                            money(5, 250),
                        ))

            # Inserts run in a single transaction; a failure rolls everything back.
            cur.executemany("""
                INSERT INTO warehouse.patient
                (patient_id, synthetic_patient_key, birth_date, sex_at_birth, postal_code)
                VALUES (%s, %s, %s, %s, %s)
            """, patients)

            cur.executemany("""
                INSERT INTO warehouse.encounter
                (encounter_id, patient_id, provider_id, service_date,
                 encounter_type, place_of_service, encounter_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, encounters)

            cur.executemany("""
                INSERT INTO warehouse.claim
                (claim_id, encounter_id, payer_id, claim_number, submitted_date,
                 claim_status, billed_amount, allowed_amount, patient_responsibility)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, claims)

            cur.executemany("""
                INSERT INTO warehouse.claim_line
                (claim_line_id, claim_id, line_number, procedure_code, diagnosis_code,
                 units, charge_amount, allowed_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                for row in claim_lines
            ])

            if payments:
                cur.executemany("""
                    INSERT INTO warehouse.payment
                    (payment_id, claim_id, payer_id, payment_date,
                     payment_method, payment_amount, posting_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, payments)

            if denials:
                cur.executemany("""
                    INSERT INTO warehouse.denial
                    (denial_id, claim_id, denial_date, denial_code,
                     denial_category, denial_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, denials)

            if adjustments:
                cur.executemany("""
                    INSERT INTO warehouse.adjustment
                    (adjustment_id, claim_id, adjustment_date,
                     adjustment_code, adjustment_type, adjustment_amount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, adjustments)

            print("\nSynthetic data loaded successfully:")
            print(f"Patients:    {len(patients):,}")
            print(f"Encounters:  {len(encounters):,}")
            print(f"Claims:      {len(claims):,}")
            print(f"Claim lines: {len(claim_lines):,}")
            print(f"Payments:    {len(payments):,}")
            print(f"Denials:     {len(denials):,}")
            print(f"Adjustments: {len(adjustments):,}")


if __name__ == "__main__":
    main()

