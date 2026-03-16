Data Flow Architecture
Overview

The Utility Data Platform is designed to ingest, process, store, and analyze electricity distribution data across multiple operational systems. The platform integrates streaming ingestion, batch ingestion, Change Data Capture (CDC), and analytical warehousing to support operational monitoring, billing, and executive analytics.

The architecture follows a modern data platform design pattern consisting of:

Data Generation / Sources

Data Ingestion Layer

Streaming Processing Layer

Operational Storage

Change Data Capture

Analytical Warehouse

Business Intelligence & Analytics

1. Data Sources

Data originates from several operational activities within the electricity distribution business.

Meter Readings

Smart meters and manual meter reading systems generate periodic electricity consumption data.

Sources:

Smart meter telemetry streams

Manual meter reading uploads

Generated data:

meter_number

read_date

meter_reading

Destination table:

meter_readings
Customer Payments

Customers make payments through multiple channels:

POS terminals

Bank transfers

Mobile apps

Online payment gateways

Generated data:

customer_id

payment_channel

payment_amount

payment_timestamp

Destination table:

payments
Field Operations

Sales representatives perform operational activities such as:

Customer visits

Disconnections

Customer onboarding

Generated data:

Field visit records

Disconnection actions

Customer enrollment

Destination tables:

field_visits
customers
Operational Excel Uploads

Certain operational data is periodically uploaded manually through Excel sheets stored in OneDrive.

Examples:

File	Data
Feeder Energy Report	Monthly feeder consumption
Manual Meter Records	Meter readings
Transformer Mapping	Transformer → feeder updates
Sales Rep Realignment	Transformer → sales rep changes

Destination tables:

feeder_energy_consumption
meter_readings
feeder_update_records
sales_rep_update_records
2. Ingestion Layer

The ingestion layer is responsible for collecting data from external systems and publishing it to the platform.

Kafka Streaming Ingestion

Real-time operational events are published into Kafka topics.

Kafka Producers:

ingestion/kafka/producers/

Examples:

Producer	Event
meter_reading_producer.py	Meter readings
payment_producer.py	Customer payments

Kafka Topics:

Topic	Description
meter_readings	Real-time meter readings
payments	Customer payment events
field_visits	Field agent visits
disconnections	Customer disconnection events
customer_enrollment	New customer registrations

Kafka acts as the central event streaming backbone of the platform.

REST API Ingestion

Operational systems submit events through a FastAPI service.

API routes:

ingestion/api/routes/

Examples:

Endpoint	Purpose
/field_visit	Log field activity
/disconnection	Record service disconnections
/customer_enrollment	Register new customers

The API validates requests using Pydantic schemas before publishing events to Kafka.

Batch Excel Ingestion

Excel reports stored in OneDrive are ingested using batch loaders.

Location:

ingestion/onedrive/

Examples:

Loader	Target Table
feeder_energy_loader.py	feeder_energy_consumption
manual_meter_loader.py	meter_readings
transformer_mapping_loader.py	feeder_update_records
sales_rep_realignment_loader.py	sales_rep_update_records

These loaders run as scheduled workflows in Airflow.

3. Streaming Processing Layer

The Spark Streaming layer processes real-time Kafka events.

Location:

streaming_processing/spark_jobs/

Key jobs:

Job	Purpose
process_payments.py	Validate and store payments
process_field_visits.py	Process field operations
process_disconnections.py	Handle service disconnections
process_customer_enrollment.py	Register new customers
billing_engine.py	Calculate electricity bills

Processing tasks include:

Schema validation

Deduplication

Data enrichment

Aggregation

Billing calculations

Processed data is written into operational storage systems.

4. Operational Storage Layer

Operational databases store processed data for application access.

PostgreSQL

Primary relational database for structured operational data.

Tables include:

customers
transformers
feeders
service_units
districts
regions
meter_readings
billing_records
payments
field_visits

PostgreSQL acts as the system of record for operational transactions.

Cassandra

Used for high-throughput payment storage.

Location:

storage/cassandra/

Reason for use:

Handles high write volume

Scales horizontally

Optimized for time-series transactions

Example table:

payment_table
MongoDB

Stores semi-structured operational updates.

Location:

storage/mongodb/

Example use cases:

Customer update requests

Operational change logs

Example collection:

customer_update_collection
5. Change Data Capture (CDC)

To keep the analytics warehouse updated in near real time, the platform uses Debezium-based Change Data Capture.

Location:

cdc_pipeline/debezium/

Debezium monitors changes in:

customers
payments
meter_readings
billing_records

Captured changes are streamed into Kafka topics.

Kafka Connect

Kafka Connect streams CDC events into Snowflake.

Location:

cdc_pipeline/kafka_connect/

Connector:

snowflake_sink_connector.json

This enables near real-time data replication into the data warehouse.

6. Analytical Data Warehouse

The analytical warehouse is implemented in Snowflake.

Location:

warehouse/snowflake/

Data is organized into dimension and fact tables following a star schema.

Dimension tables:

dim_customer
dim_transformer
dim_feeder
dim_service_unit
dim_district
dim_region
dim_sales_rep
dim_band_tariff

Fact tables:

fact_meter_consumption
fact_payments
fact_billing
fact_field_visits

Benefits:

Fast analytical queries

Historical analysis

Business reporting

7. Transformations (dbt)

The transformation layer uses dbt to build the warehouse models.

Location:

transformations/dbt/

Structure:

staging/
intermediate/
marts/

Responsibilities:

Data cleaning

Business logic implementation

Dimensional modeling

KPI calculations

8. Workflow Orchestration

Data workflows are orchestrated using Apache Airflow.

Location:

infrastructure/airflow/dags/

Key pipelines:

DAG	Purpose
fact_payment_pipeline.py	Payment processing
fact_meter_consumption_pipeline.py	Consumption calculations
feeder_energy_ingestion.py	Feeder energy batch ingestion
manual_meter_readings_ingestion.py	Manual meter uploads
transformer_mapping_updates.py	Transformer updates
customer_update_requests_pipeline.py	Customer update processing

Airflow manages:

Scheduling

Dependency management

Failure retries

Monitoring

9. Analytics Layer

Business intelligence dashboards are built using Power BI.

Location:

analytics/powerbi/

Dashboards track key electricity distribution metrics.

Examples:

Revenue Metrics

Total revenue collected

Outstanding debt

Payment trends

Operational Metrics

Transformer load

Feeder consumption

Energy losses

Field Operations

Field visit activity

Disconnection rates

Customer service performance

10. End-to-End Data Flow Summary
Data Sources
      │
      ▼
Kafka Producers / REST APIs / Excel Uploads
      │
      ▼
Kafka Event Streaming
      │
      ▼
Spark Streaming Processing
      │
      ▼
Operational Databases
(PostgreSQL / Cassandra / MongoDB)
      │
      ▼
Debezium CDC
      │
      ▼
Kafka Connect
      │
      ▼
Snowflake Data Warehouse
      │
      ▼
dbt Transformations
      │
      ▼
Power BI Analytics