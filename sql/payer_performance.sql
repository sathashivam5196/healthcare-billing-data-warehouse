CREATE OR REPLACE VIEW workspace.healthcare_billing.payer_performance AS
SELECT
    p.payer_id,
    p.payer_code,
    p.payer_name,
    p.payer_type,
    COUNT(c.claim_id) AS total_claims,
    ROUND(SUM(c.billed_amount), 2) AS total_billed_amount,
    ROUND(SUM(c.allowed_amount), 2) AS total_allowed_amount,
    ROUND(SUM(c.patient_responsibility), 2) AS total_patient_responsibility,
    ROUND(
        100.0 * SUM(c.allowed_amount)
        / NULLIF(SUM(c.billed_amount), 0),
        2
    ) AS allowed_to_billed_pct
FROM workspace.healthcare_billing.payer p
LEFT JOIN workspace.healthcare_billing.claim c
    ON p.payer_id = c.payer_id
GROUP BY
    p.payer_id,
    p.payer_code,
    p.payer_name,
    p.payer_type;