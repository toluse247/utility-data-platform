INSERT INTO stg_previous_balance (customer_id, previous_balance)
SELECT customer_id, outstanding_amount
FROM billing_records
WHERE DATE_TRUNC('month', billing_month) = (
    SELECT DATE_TRUNC('month', MAX(billing_month))
    FROM billing_records
);


INSERT INTO stg_previous_payments (customer_id, previous_payments)
SELECT customer_id, total_payment
FROM customer_monthly_payments
WHERE (year, month) IN (
    SELECT year, month
    FROM customer_monthly_payments
    ORDER BY year DESC, month DESC
    LIMIT 1
);

INSERT INTO stg_previous_adjustments (customer_id, previous_adjustments)
SELECT customer_id, SUM(previous_adjustments) AS previous_adjustments
FROM billing_records
WHERE DATE_TRUNC('month', billing_month) = (
    SELECT DATE_TRUNC('month', MAX(billing_month))
    FROM billing_records
)
GROUP BY customer_id;

INSERT INTO stg1_billing_records (
    customer_id, billing_month, billing_type,
    previous_reading, present_reading, consumption_kwh
)
SELECT 
    c.customer_id,
    DATE_TRUNC('month', CURRENT_DATE) AS billing_month,
    c.billing_type,
    prv.previous_reading,
    prs.present_reading,
    (prs.present_reading - prv.previous_reading) AS consumption_kwh
FROM customers c

JOIN stg_previous_readings prv 
    ON c.customer_id = prv.customer_id

JOIN stg_present_readings prs 
    ON c.customer_id = prs.customer_id

WHERE c.account_status = 'ACTIVE'
  AND c.billing_type = 'R'
  AND prs.present_reading IS NOT NULL
  AND prv.previous_reading IS NOT NULL
  AND prs.present_reading >= prv.previous_reading;