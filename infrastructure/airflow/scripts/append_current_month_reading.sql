INSERT INTO monthly_meter_readings (customer_id, year, month, meter_reading)
SELECT customer_id, year, month, meter_reading
FROM stg_present_readings;