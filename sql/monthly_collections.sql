CREATE OR REPLACE VIEW workspace.healthcare_billing.monthly_collections AS
SELECT
    YEAR(payment_date) AS collection_year,
    MONTH(payment_date) AS collection_month,
    DATE_FORMAT(payment_date, 'yyyy-MM') AS collection_period,
    COUNT(*) AS payment_count,
    ROUND(SUM(payment_amount), 2) AS total_collections,
    ROUND(AVG(payment_amount), 2) AS average_payment_amount
FROM workspace.healthcare_billing.payment
WHERE posting_status = 'Posted'
GROUP BY
    YEAR(payment_date),
    MONTH(payment_date),
    DATE_FORMAT(payment_date, 'yyyy-MM');