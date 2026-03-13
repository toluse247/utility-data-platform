# Utility Data Platform Architecture

## Overview

This project implements an end-to-end data engineering platform for a power utility company to ingest, process, and analyze operational and financial data including customer information, billing records, payment transactions, smart meter telemetry, and field operations.

The system supports both batch and streaming data pipelines and follows a modern lakehouse architecture.

## Architecture Layers

The platform is composed of five primary layers:

1. Data Ingestion
2. Data Storage
3. Data Processing
4. Data Warehousing
5. Data Analytics

---

## Data Ingestion Layer

The ingestion layer collects data from multiple operational sources.

Sources include:

- Web Application APIs
- OneDrive batch files
- Kafka streaming events
- Operational databases

Technologies:

- Apache Kafka
- Apache Airflow
- Flask API

Data Types:

- Customer enrollment
- Billing records
- Smart meter readings
- POS and online payments
- Field visitation logs
- Disconnection records

---

## Data Storage Layer

The platform uses a polyglot persistence architecture.

Databases:

PostgreSQL
Used for relational operational data such as customer information, billing records, and field operations.

Cassandra
Used for high-volume streaming data such as payment transactions.

MongoDB
Used for semi-structured data including customer update requests.

Amazon S3
Used as a data lake for raw and processed datasets including smart meter telemetry and image uploads.

---

## Data Processing Layer

Batch and streaming processing is implemented using distributed data processing engines.

Technologies:

Apache Spark
Databricks

Processing Tasks:

- Data cleaning
- Schema normalization
- Payment aggregation
- Meter reading filtering
- Customer update processing
- Billing aggregation

---

## Data Warehouse Layer

Curated datasets are loaded into the Snowflake data warehouse.

The warehouse follows a star schema optimized for analytical queries.

Fact Tables:

fact_payments
fact_billing
fact_meter_readings
fact_disconnections

Dimension Tables:

dim_customer
dim_sales_rep
dim_transformer
dim_feeder
dim_date

---

## Analytics Layer

Business dashboards are built using Power BI connected directly to the Snowflake warehouse.

Analytics include:

- Collection efficiency
- Revenue runrate
- Customer churn
- Sales representative performance
- Disconnection and reconnection metrics
- Energy consumption analytics