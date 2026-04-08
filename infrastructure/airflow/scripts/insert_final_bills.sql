INSERT INTO billing_records (customer_id, billing_month, billing_type,
    due_date, previous_reading, present_reading, consumption_kwh, tariff_rate, 
    energy_charges, vat, billed_amount, previous_balance, previous_payments, 
    previous_adjustments, net_arrears, outstanding_amount)

SELECT customer_id, billing_month, billing_type,
    due_date, previous_reading, present_reading, consumption_kwh, tariff_rate, 
    energy_charges, vat, billed_amount, previous_balance, previous_payments, 
    previous_adjustments, net_arrears, outstanding_amount
FROM stg2_billing_records

ON CONFLICT (customer_id, billing_month)
DO UPDATE SET
    consumption_kwh = EXCLUDED.consumption_kwh,
    billed_amount = EXCLUDED.billed_amount,
    outstanding_amount = EXCLUDED.outstanding_amount
;