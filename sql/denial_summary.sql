CREATE OR REPLACE VIEW workspace.healthcare_billing.denial_summary AS
SELECT
    YEAR(denial_date) AS denial_year,
    MONTH(denial_date) AS denial_month,
    DATE_FORMAT(denial_date, 'yyyy-MM') AS denial_period,
    denial_category,
    denial_code,
    denial_status,
    COUNT(*) AS denial_count
FROM workspace.healthcare_billing.denial
GROUP BY
    YEAR(denial_date),
    MONTH(denial_date),
    DATE_FORMAT(denial_date, 'yyyy-MM'),
    denial_category,
    denial_code,
    denial_status;