DROP TABLE IF EXISTS stg_previous_readings;
CREATE TABLE stg_previous_readings (
    customer_id INT,
    previous_reading DOUBLE PRECISION
    );

DROP TABLE IF EXISTS stg_present_readings;
CREATE TABLE stg_present_readings (
    customer_id INT,
    year INT,
    month INT,
    meter_reading NUMERIC(10, 2),
    );


DROP TABLE IF EXISTS stg_estimated_consumption;
CREATE TABLE stg_estimated_consumption (
    feeder_id INT,
    estimated_consumption DOUBLE PRECISION
    );

DROP TABLE IF EXISTS stg_previous_balance;
CREATE TABLE stg_previous_balance (
    customer_id INT,
    previous_balance DOUBLE PRECISION
    );


DROP TABLE IF EXISTS stg_previous_payments;
CREATE TABLE stg_previous_payments (
    customer_id INT,
    previous_payments DOUBLE PRECISION
    );


DROP TABLE IF EXISTS stg_previous_adjustments;
CREATE TABLE stg_previous_adjustments (
    customer_id INT,
    previous_adjustments DOUBLE PRECISION
    );

DROP TABLE IF EXISTS stg1_billing_records;
CREATE TABLE stg1_billing_records (
    customer_id INT,
    billing_month DATE,
    billing_type VARCHAR(1),
    previous_reading FLOAT,
    present_reading FLOAT,
    consumption_kwh NUMERIC(10, 2),
);

DROP TABLE IF EXISTS stg2_billing_records;
CREATE TABLE stg2_billing_records (
    bill_id SERIAL PRIMARY KEY,
    customer_id INT,
    billing_month DATE,
    billing_type VARCHAR(1),
    due_date DATE,
    previous_reading FLOAT,
    present_reading FLOAT,
    consumption_kwh NUMERIC(10, 2),
    tariff_rate NUMERIC(10, 2),
    energy_charges NUMERIC(10, 2),
    vat NUMERIC(10, 2),
    billed_amount NUMERIC(10, 2),
    previous_balance NUMERIC(10, 2),
    previous_payments NUMERIC(10, 2),
    previous_adjustments NUMERIC(10, 2),
    net_arrears NUMERIC(10, 2),
    outstanding_amount NUMERIC(10, 2),

);