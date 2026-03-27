INSERT INTO stg_previous_readings (customer_id, previous_reading)
SELECT customer_id, meter_reading AS previous_reading
FROM monthly_meter_readings
WHERE (year, month) IN (
    SELECT year, month
    FROM monthly_meter_readings
    ORDER BY year DESC, month DESC
    LIMIT 1
);