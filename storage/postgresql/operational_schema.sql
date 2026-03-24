CREATE TABLE regions (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50)
);

CREATE TABLE districts (
    district_id INT PRIMARY KEY,
    district_name VARCHAR(50),
    region_id INT NOT NULL,

    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE service_units (
    service_unit_id INT PRIMARY KEY,
    service_unit_name VARCHAR(50),
    district_id INT NOT NULL,

    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

CREATE TABLE band_tariff (
    band_id INT PRIMARY KEY,
    band_name VARCHAR(1) NOT NULL,
    tariff_rate NUMERIC(10, 2) NOT NULL,
    vat_rate NUMERIC(10, 2) NOT NULL
);

CREATE TABLE feeders (
    feeder_id INT PRIMARY KEY,
    feeder_name VARCHAR(50) NOT NULL,
    band_id INT NOT NULL,
    service_unit_id INT NOT NULL,

    FOREIGN KEY (band_id) REFERENCES band_tariff(band_id),
    FOREIGN KEY (service_unit_id) REFERENCES service_units(service_unit_id)
);

CREATE TABLE sales_reps (
    sales_rep_id INT PRIMARY KEY,
    sales_rep_name VARCHAR(50),
    sales_rep_phone VARCHAR(15)
);

CREATE TABLE transformers (
    transformer_id INT PRIMARY KEY,
    transformer_name VARCHAR(50),
    sales_rep_id INT NOT NULL,
    feeder_id INT NOT NULL,

    FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id),
    FOREIGN KEY (sales_rep_id) REFERENCES sales_reps(sales_rep_id)
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    meter_number VARCHAR(50) UNIQUE,
    customer_name VARCHAR(100),
    address TEXT,
    customer_phone VARCHAR(30),
    customer_type VARCHAR(20),
    billing_type VARCHAR(1),
    transformer_id INT NOT NULL,
    account_status VARCHAR(20),
    latitude FLOAT,
    longitude FLOAT,
    email VARCHAR(50),
    created_at TIMESTAMP,

    FOREIGN KEY (transformer_id) REFERENCES transformers(transformer_id)
);

CREATE TABLE feeder_energy_consumption (
    feeder_cons_id INT PRIMARY KEY,
    feeder_id INT NOT NULL,
    feeder_name VARCHAR(50),
    consumption_month DATE,
    consumption_kwh NUMERIC(10, 2),

    FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id)
);



CREATE TABLE billing_records (
    bill_id SERIAL PRIMARY KEY,
    customer_id INT,
    billing_month DATE,
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

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE meter_readings (
    meter_reading_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    meter_number VARCHAR(50),
    read_date DATE,
    meter_reading FLOAT,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE customer_monthly_payments (
    customer_id INT,
    year INT,
    month INT,
    total_payment NUMERIC(10, 2),

    PRIMARY KEY (customer_id, year, month),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    
);


CREATE TABLE field_visits (
    visit_id SERIAL PRIMARY KEY,
    sales_rep_id INT NOT NULL,
    customer_id INT NOT NULL,
    visit_date DATE,
    visit_type VARCHAR(50),
    notes TEXT,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (sales_rep_id) REFERENCES sales_reps(sales_rep_id)
);


CREATE TABLE feeder_update_records (
    feeder_update_id SERIAL PRIMARY KEY,
    transformer_id INT NOT NULL,
    transformer_name VARCHAR(50),
    new_feeder_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE,

    FOREIGN KEY (transformer_id) REFERENCES transformers(transformer_id),
    FOREIGN KEY (new_feeder_id) REFERENCES feeders(feeder_id)
);


CREATE TABLE sales_rep_update_records (
    sales_rep_update_id SERIAL PRIMARY KEY,
    transformer_id INT NOT NULL,
    transformer_name VARCHAR(50),
    new_sales_rep_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE,

    FOREIGN KEY (transformer_id) REFERENCES transformers(transformer_id),
    FOREIGN KEY (new_sales_rep_id) REFERENCES sales_reps(sales_rep_id)
);


CREATE TABLE band_update_records (
    band_update_id SERIAL PRIMARY KEY,
    feeder_id INT NOT NULL,
    feeder_name VARCHAR(50),
    new_band_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE,

    FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id),
    FOREIGN KEY (new_band_id) REFERENCES band_tariff(band_id)
);


CREATE TABLE tariff_rate_update_records (
    tariff_rate_update_id SERIAL PRIMARY KEY,
    band_id INT NOT NULL,
    band_name VARCHAR(50),
    new_tariff_rate NUMERIC(10, 2) NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE,

    FOREIGN KEY (band_id) REFERENCES band_tariff(band_id)
);

CREATE TABLE vat_rate_update_records (
    vat_rate_update_id SERIAL PRIMARY KEY,
    band_id INT NOT NULL,
    band_name VARCHAR(50),
    new_vat_rate NUMERIC(10, 2) NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE,

    FOREIGN KEY (band_id) REFERENCES band_tariff(band_id)
);


CREATE INDEX idx_customer_id ON billing_records(customer_id);
CREATE INDEX idx_meter_customer ON meter_readings(customer_id);
CREATE INDEX idx_payment_customer ON payments(customer_id);