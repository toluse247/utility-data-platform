WITH 
num_direct AS (
    SELECT feeder_id, COUNT(customer_id) AS num_direct
    FROM customers
    WHERE billing_type = 'D' AND account_status = 'ACTIVE'
    GROUP BY feeder_id
),
read_consumption AS (
    SELECT feeder_id, SUM(consumption_kwh) AS read_consumption
    FROM stg1_billing_records
    WHERE billing_type = 'R'
    GROUP BY feeder_id
)
INSERT INTO stg_estimated_consumption (feeder_id, estimated_consumption)
SELECT feeder_id, estimated_consumption
FROM (
    SELECT f.feeder_id, 
           ((f.consumption_kwh - rc.read_consumption) / nd.num_direct) AS estimated_consumption
    FROM feeder_energy_consumption f
    JOIN num_direct nd ON f.feeder_id = nd.feeder_id
    JOIN read_consumption rc ON f.feeder_id = rc.feeder_id
) AS sub;