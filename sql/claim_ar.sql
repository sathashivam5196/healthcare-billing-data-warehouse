CREATE OR REPLACE VIEW workspace.healthcare_billing.claim_ar AS
SELECT
    c.claim_id,
    c.claim_number,
    c.encounter_id,
    e.patient_id,
    e.provider_id,
    e.service_date,
    e.encounter_status,
    c.payer_id,
    p.payer_name,
    c.submitted_date,
    c.claim_status,
    c.billed_amount,
    c.allowed_amount,
    c.patient_responsibility,
    ROUND(
        c.billed_amount - COALESCE(c.allowed_amount, 0),
        2
    ) AS billed_less_allowed
FROM workspace.healthcare_billing.claim c
LEFT JOIN workspace.healthcare_billing.encounter e
    ON c.encounter_id = e.encounter_id
LEFT JOIN workspace.healthcare_billing.payer p
    ON c.payer_id = p.payer_id;