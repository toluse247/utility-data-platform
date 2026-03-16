CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    meter_number VARCHAR(50) UNIQUE,
    customer_name VARCHAR(100),
    address TEXT,
    customer_phone VARCHAR(15),
    customer_type VARCHAR(1),
    transformer_id INT,
    account_status VARCHAR(20),
    latitude FLOAT,
    longitude FLOAT,
    email VARCHAR(50),
    created_at TIMESTAMP,

    FOREIGN KEY (transformer_id) REFERENCES transformers(transformer_id)
);


CREATE TABLE transformers (
    transformer_id INT PRIMARY KEY,
    transformer_name VARCHAR(50),
    sales_rep_id INT,
    feeder_id INT NOT NULL,

    FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id),
    FOREIGN KEY (sales_rep_id) REFERENCES sales_reps(sales_rep_id)
);


CREATE TABLE feeders (
    feeder_id INT PRIMARY KEY,
    feeder_name VARCHAR(50) NOT NULL,
    band_id INT NOT NULL,
    service_unit_id INT NOT NULL,

    FOREIGN KEY (band_id) REFERENCES band_tariff(band_id),
    FOREIGN KEY (service_unit_id) REFERENCES service_units(service_unit_id)
);


CREATE TABLE service_units (
    service_unit_id INT PRIMARY KEY,
    service_unit_name VARCHAR(50),
    district_id INT NOT NULL,

    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);


CREATE TABLE districts (
    district_id INT PRIMARY KEY,
    district_name VARCHAR(50),
    region_id INT NOT NULL,

    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);


CREATE TABLE regions (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50)
);


CREATE TABLE band_tariff (
    band_id INT PRIMARY KEY,
    band_name VARCHAR(1) NOT NULL,
    tariff_rate FLOAT NOT NULL,
    vat_rate FLOAT NOT NULL
);

CREATE TABLE sales_reps (
    sales_rep_id INT PRIMARY KEY,
    sales_rep_name VARCHAR(50),
    sales_rep_phone VARCHAR(15)
);


CREATE TABLE feeder_energy_consumption (
    feeder_cons_id INT PRIMARY KEY,
    feeder_id INT NOT NULL,
    feeder_name VARCHAR(50),
    consumption_month DATE,
    consumption_kwh FLOAT,

    FOREIGN KEY (feeder_id) REFERENCES feeders(feeder_id)
);



CREATE TABLE billing_records (
    bill_id SERIAL PRIMARY KEY,
    customer_id INT,
    billing_month DATE,
    due_date DATE,
    previous_reading FLOAT,
    present_reading FLOAT,
    consumption_kwh FLOAT,
    tariff_rate FLOAT,
    energy_charges FLOAT,
    vat FLOAT,
    billed_amount FLOAT,
    previous_balance FLOAT,
    previous_payments FLOAT,
    previous_adjustments FLOAT,
    net_arrears FLOAT,
    outstanding_amount FLOAT,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE meter_readings (
    meter_reading_id SERIAL PRIMARY KEY,
    customer_id INT,
    meter_number VARCHAR(50),
    read_date DATE,
    meter_reading FLOAT,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    customer_id INT,
    payment_channel VARCHAR(50),
    payment_amount FLOAT,
    payment_timestamp TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE field_visits (
    visit_id SERIAL PRIMARY KEY,
    sales_rep_id INT,
    customer_id INT,
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
    request_date DATE
);


CREATE TABLE sales_rep_update_records (
    sales_rep_update_id SERIAL PRIMARY KEY,
    transformer_id INT NOT NULL,
    transformer_name VARCHAR(50),
    new_sales_rep_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE
);


CREATE TABLE band_update_records (
    band_update_id SERIAL PRIMARY KEY,
    feeder_id INT NOT NULL,
    feeder_name VARCHAR(50),
    new_band_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE
);


CREATE TABLE tariff_rate_update_records (
    tariff_rate_update_id SERIAL PRIMARY KEY,
    band_id INT NOT NULL,
    band_name VARCHAR(50),
    new_tariff_rate_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE
);

CREATE TABLE vat_rate_update_records (
    vat_rate_update_id SERIAL PRIMARY KEY,
    band_id INT NOT NULL,
    band_name VARCHAR(50),
    new_vat_rate_id INT NOT NULL,
    initiator_name VARCHAR(50),
    request_date DATE
);


