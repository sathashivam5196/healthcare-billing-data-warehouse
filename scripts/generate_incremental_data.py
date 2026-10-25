
import random
from datetime import date, timedelta
from decimal import Decimal

import os
import psycopg
TARGET_PATIENTS = 10_000
SEED = 20261026
TODAY = date.today()
START_DATE = TODAY - timedelta(days=730)


def money(low, high):
    return Decimal(str(round(random.uniform(float(low), float(high)), 2)))


def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def main():
    random.seed(SEED)
    password = getpass.getpass("PostgreSQL password: ")

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="healthcare_billing",
        user="postgres",
        password=password,
    ) as conn:
        with conn.cursor() as cur:
            # Check existing patient count and stop if already at target.
            cur.execute("SELECT COUNT(*) FROM warehouse.patient")
            existing_patients = cur.fetchone()[0]

            if existing_patients >= TARGET_PATIENTS:
                print(
                    f"Already have {existing_patients:,} patients. "
                    "No data was inserted."
                )
                return

            # Ensure existing data is consistent with the expected starting state.
            for table in (
                "encounter", "claim", "claim_line",
                "payment", "denial", "adjustment"
            ):
                cur.execute(f"SELECT COUNT(*) FROM warehouse.{table}")
                if cur.fetchone()[0] == 0 and existing_patients > 0:
                    raise RuntimeError(
                        f"Unexpected empty table: warehouse.{table}. "
                        "No data was inserted."
                    )

            cur.execute("SELECT provider_id FROM warehouse.provider ORDER BY provider_id")
            provider_ids = [r[0] for r in cur.fetchall()]

            cur.execute("SELECT payer_id FROM warehouse.payer ORDER BY payer_id")
            payer_ids = [r[0] for r in cur.fetchall()]

            if not provider_ids or not payer_ids:
                raise RuntimeError("Provider and payer reference data is required.")

            # Allocate new IDs after the current maximum in each table.
            def next_id(table, column):
                cur.execute(
                    f"SELECT COALESCE(MAX({column}), 0) + 1 "
                    f"FROM warehouse.{table}"
                )
                return cur.fetchone()[0]

            next_patient = next_id("patient", "patient_id")
            next_encounter = next_id("encounter", "encounter_id")
            next_claim = next_id("claim", "claim_id")
            next_line = next_id("claim_line", "claim_line_id")
            next_payment = next_id("payment", "payment_id")
            next_denial = next_id("denial", "denial_id")
            next_adjustment = next_id("adjustment", "adjustment_id")

            patient_rows = []
            encounter_rows = []
            claim_rows = []
            line_rows = []
            payment_rows = []
            denial_rows = []
            adjustment_rows = []

            patients_to_add = TARGET_PATIENTS - existing_patients

            for patient_id in range(next_patient, next_patient + patients_to_add):
                patient_rows.append((
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
                    encounter_id = next_encounter
                    next_encounter += 1

                    service_date = random_date(START_DATE, TODAY)
                    encounter_status = random.choices(
                        ["Completed", "Cancelled", "InProgress"],
                        weights=[92, 5, 3],
                    )[0]

                    encounter_rows.append((
                        encounter_id,
                        patient_id,
                        random.choice(provider_ids),
                        service_date,
                        random.choice(["Office", "Emergency", "Ambulatory", "Other"]),
                        random.choice(["11", "22", "23", "24"]),
                        encounter_status,
                    ))

                    if encounter_status == "Cancelled":
                        continue

                    payer_id = random.choice(payer_ids)
                    submitted_date = min(
                        TODAY,
                        service_date + timedelta(days=random.randint(0, 30)),
                    )
                    claim_id = next_claim
                    next_claim += 1

                    # Create detail lines first; header totals derive from those lines.
                    line_count = random.randint(1, 3)
                    billed_total = Decimal("0.00")
                    allowed_total = Decimal("0.00")

                    for line_number in range(1, line_count + 1):
                        charge = money(50, 900)
                        allowed = min(
                            charge,
                            money(
                                charge * Decimal("0.45"),
                                charge * Decimal("0.95"),
                            ),
                        )

                        line_rows.append((
                            next_line,
                            claim_id,
                            line_number,
                            random.choice(
                                ["99213", "99214", "93000", "80053", "A0429"]
                            ),
                            random.choice(
                                ["R05.9", "I10", "E11.9", "S09.90XA", "Z00.00"]
                            ),
                            Decimal("1.00"),
                            charge,
                            allowed,
                        ))
                        next_line += 1
                        billed_total += charge
                        allowed_total += allowed

                    claim_status = random.choices(
                        ["Submitted", "Accepted", "Denied", "Paid",
                         "PartiallyPaid", "Rejected", "Pending"],
                        weights=[12, 10, 12, 35, 15, 6, 10],
                    )[0]

                   
                    claims_for_encounter = (
                        claim_id, encounter_id, payer_id,
                        f"SYN-CLM-{claim_id:010d}",
                        submitted_date, claim_status, billed_total,
                        allowed_total,
                        max(Decimal("0.00"), billed_total - allowed_total),
                    )
                    claim_rows.append(claims_for_encounter)

                    if claim_status in ("Paid", "PartiallyPaid"):
                        amount = (
                            allowed_total
                            if claim_status == "Paid"
                            else (allowed_total / Decimal("2")).quantize(
                                Decimal("0.01")
                            )
                        )
                        payment_rows.append((
                            next_payment,
                            claim_id,
                            payer_id,
                            min(
                                TODAY,
                                submitted_date + timedelta(
                                    days=random.randint(5, 90)
                                ),
                            ),
                            random.choice(["EFT", "Check", "ERA"]),
                            max(Decimal("0.01"), amount),
                            "Posted",
                        ))
                        next_payment += 1

                    if claim_status == "Denied":
                        denial_rows.append((
                            next_denial,
                            claim_id,
                            min(
                                TODAY,
                                submitted_date + timedelta(
                                    days=random.randint(1, 45)
                                ),
                            ),
                            random.choice(["CO16", "CO97", "PR204", "CO50"]),
                            random.choice([
                                "Missing Information", "Bundled Service",
                                "Authorization", "Medical Necessity",
                            ]),
                            random.choice([
                                "Open", "Appealed", "Resolved", "WrittenOff"
                            ]),
                        ))
                        next_denial += 1

                    if random.random() < 0.20:
                     
                        adjustment_rows.append((
                            next_adjustment,
                            claim_id,
                            min(
                                TODAY,
                                submitted_date + timedelta(
                                    days=random.randint(5, 120)
                                ),
                            ),
                            random.choice(["CONTRACT", "WRITE_OFF", "CORRECTION"]),
                            random.choice([
                                "Contractual", "WriteOff", "Correction", "Other"
                            ]),
                            money(5, 250),
                        ))
                        next_adjustment += 1

            # Insert in dependency order; the connection commits only on success.
            cur.executemany("""
                INSERT INTO warehouse.patient
                (patient_id, synthetic_patient_key, birth_date, sex_at_birth, postal_code)
                VALUES (%s, %s, %s, %s, %s)
            """, patient_rows)

            cur.executemany("""
                INSERT INTO warehouse.encounter
                (encounter_id, patient_id, provider_id, service_date,
                 encounter_type, place_of_service, encounter_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, encounter_rows)

            cur.executemany("""
                INSERT INTO warehouse.claim
                (claim_id, encounter_id, payer_id, claim_number, submitted_date,
                 claim_status, billed_amount, allowed_amount, patient_responsibility)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, claim_rows)

            if line_rows:
                cur.executemany("""
                    INSERT INTO warehouse.claim_line
                    (claim_line_id, claim_id, line_number, procedure_code,
                     diagnosis_code, units, charge_amount, allowed_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, line_rows)

            if payment_rows:
                cur.executemany("""
                    INSERT INTO warehouse.payment
                    (payment_id, claim_id, payer_id, payment_date,
                     payment_method, payment_amount, posting_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, payment_rows)

            if denial_rows:
                cur.executemany("""
                    INSERT INTO warehouse.denial
                    (denial_id, claim_id, denial_date, denial_code,
                     denial_category, denial_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, denial_rows)

            if adjustment_rows:
                cur.executemany("""
                    INSERT INTO warehouse.adjustment
                    (adjustment_id, claim_id, adjustment_date,
                     adjustment_code, adjustment_type, adjustment_amount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, adjustment_rows)

            print("\nIncremental load committed successfully.")
            print(f"Patients added:    {len(patient_rows):,}")
            print(f"Encounters added:  {len(encounter_rows):,}")
            print(f"Claims added:      {len(claim_rows):,}")
            print(f"Claim lines added: {len(line_rows):,}")
            print(f"Payments added:    {len(payment_rows):,}")
            print(f"Denials added:     {len(denial_rows):,}")
            print(f"Adjustments added: {len(adjustment_rows):,}")
            print(f"Total patients target: {TARGET_PATIENTS:,}")


if __name__ == "__main__":
    main()

