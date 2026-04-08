
WITH base AS (
    
    SELECT c.customer_id AS customer_id, 
    DATE_TRUNC('month', CURRENT_DATE) AS billing_month, 
    c.billing_type AS billing_type,
    DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '14 days' AS due_date, 
    prv.previous_reading AS previous_reading, 
    prs.present_reading AS present_reading,

    CASE 
        WHEN c.account_status = 'SUSPENDED' THEN 0
        WHEN c.account_status = 'ACTIVE' AND c.billing_type = 'R'
        AND prs.present_reading IS NOT NULL AND prv.previous_reading IS NOT NULL 
        AND prs.present_reading >= prv.previous_reading
        THEN prs.present_reading - prv.previous_reading 
        ELSE COALESCE(est.estimated_consumption, 0)
    END AS consumption_kwh,
    
    bt.tariff_rate AS tariff_rate,
    bt.vat_rate AS vat_rate,
    COALESCE(prev_b.previous_balance, 0) AS previous_balance,
    COALESCE(prev_p.previous_payments, 0) AS previous_payments,
    COALESCE(prev_a.previous_adjustments, 0) AS previous_adjustments

    FROM customers c

    LEFT JOIN stg_previous_readings prv 
        ON c.customer_id = prv.customer_id

    LEFT JOIN stg_present_readings prs 
        ON c.customer_id = prs.customer_id

    LEFT JOIN stg_estimated_consumption est 
        ON c.feeder_id = est.feeder_id

    LEFT JOIN transformers t 
        ON c.transformer_id = t.transformer_id

    LEFT JOIN feeders f 
        ON t.feeder_id = f.feeder_id

    LEFT JOIN band_tariff bt 
        ON f.band_id = bt.band_id

    LEFT JOIN stg_previous_balance prev_b 
        ON c.customer_id = prev_b.customer_id

    LEFT JOIN stg_previous_payments prev_p 
        ON c.customer_id = prev_p.customer_id

    LEFT JOIN stg_previous_adjustments prev_a 
        ON c.customer_id = prev_a.customer_id
)

INSERT INTO stg2_billing_records (customer_id, billing_month, billing_type,
    due_date, previous_reading, present_reading, consumption_kwh, tariff_rate, 
    energy_charges, vat, billed_amount, previous_balance, previous_payments, 
    previous_adjustments, net_arrears, outstanding_amount)

SELECT customer_id, 
    billing_month, 
    billing_type,
    due_date, 
    previous_reading, 
    present_reading,
    consumption_kwh,
    tariff_rate,

    ROUND(consumption_kwh * tariff_rate, 2) AS energy_charges,
    ROUND(consumption_kwh * tariff_rate * vat_rate, 2) AS vat, 
    ROUND(consumption_kwh * tariff_rate * (1 + vat_rate), 2) AS billed_amount, 

    previous_balance,
    previous_payments,
    previous_adjustments,
    (previous_balance - previous_payments) AS net_arrears,

    ROUND(
    (previous_balance - previous_payments) +
    ROUND(consumption_kwh * tariff_rate * (1 + vat_rate), 2) -
    previous_adjustments, 2) AS outstanding_amount

FROM base

ON CONFLICT (customer_id, billing_month)
DO UPDATE SET
    consumption_kwh = EXCLUDED.consumption_kwh,
    billed_amount = EXCLUDED.billed_amount,
    outstanding_amount = EXCLUDED.outstanding_amount
;