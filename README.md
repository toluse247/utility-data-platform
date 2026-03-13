Utility Revenue Intelligence Data Platform

An end-to-end modern data engineering platform designed to simulate how
an electricity distribution company processes operational data such as
meter readings, customer information, billing records, payments, and
field operations.

This project demonstrates how to build a production-style data pipeline
architecture using modern data engineering tools including Apache Kafka,
Apache Spark, Apache Airflow, Snowflake, and Power BI.

The platform simulates a utility company serving 1 million customers
across multiple districts, processing both real-time streaming data and
batch operational data.

------------------------------------------------------------------------

PROJECT OBJECTIVES

This repository demonstrates how to design and implement:

-   Real-time and batch data pipeline architecture
-   Streaming ingestion pipelines
-   Operational data storage with multiple database types
-   Distributed data processing
-   Cloud storage integration
-   Change Data Capture pipelines
-   Dimensional warehouse modeling
-   Business intelligence dashboards

------------------------------------------------------------------------

SYSTEM ARCHITECTURE

Data Generation Layer | v Ingestion Layer (Kafka, APIs, File Uploads) |
v Processing Layer (Spark, Databricks) | v Operational Storage Layer
(PostgreSQL, Cassandra, MongoDB, Amazon S3) | v CDC & ETL Layer
(Debezium + Airflow) | v Data Warehouse (Snowflake) | v Analytics Layer
(Power BI)

------------------------------------------------------------------------

BUSINESS DOMAIN MODEL

The system models the hierarchy of a power distribution network:

Region | District | Service Unit | Feeder | Transformer | Customer

Customer Types:

Metered Customers (Type R) Billed based on actual meter readings.

Unmetered Customers (Type D) Billed using feeder-level estimated
consumption.

Estimated Consumption Formula:

Estimated Consumption = (Total Feeder kWh – Metered Customer kWh) /
Number of Unmetered Customers

------------------------------------------------------------------------

DATA SOURCES

Streaming Data - Smart meter telemetry (hourly) - Payment transactions

API Generated Events - Field visits - Service disconnections - New
customer enrollments

Batch File Uploads (via OneDrive) - Manual meter readings - Sales
representative realignment - Transformer to feeder mapping updates -
Feeder total energy consumption per billing cycle - Customer information
update requests

------------------------------------------------------------------------

DATA STORAGE LAYER

PostgreSQL Operational relational database for customer, billing, field
operations, and payment fact tables.

Apache Cassandra High throughput storage for payment streaming events.

MongoDB Flexible schema store for customer update request workflows.

Amazon S3 Raw storage for high-frequency smart meter telemetry.

------------------------------------------------------------------------

DATA PROCESSING

Streaming Pipelines - Spark streaming processes payment events from
Cassandra into PostgreSQL - Databricks processes smart meter telemetry
from S3 into the operational meter_readings table

Batch Pipelines Managed using Apache Airflow for:

-   Excel ingestion workflows
-   Customer update workflows
-   Dimension updates
-   Fact table transformations

------------------------------------------------------------------------

DATA WAREHOUSE

Curated datasets are loaded into Snowflake.

Two strategies are used:

CDC Pipelines (for Dimension Tables) Operational dimension tables are
synchronized using change data capture.

Examples: - Customers - Transformers - Feeders - Sales Representatives

Batch ETL Pipelines (for Fact Tables)

Examples: - Payments - Meter Readings - Billing Records - Field Visits

------------------------------------------------------------------------

ANALYTICS DASHBOARDS

The warehouse powers Power BI dashboards.

Revenue Performance - Collection Efficiency by District - Collection
Efficiency by Sales Representative - Collection Efficiency by Feeder

Customer Analytics - Customer Growth - Customer Churn Rate - Average
Payment per Customer

Operations Monitoring - Disconnection Efficiency - Reconnection Fee
Recovery - Marketing Campaign Efficiency

------------------------------------------------------------------------

SYNTHETIC DATA SIMULATION

The system generates enterprise-scale simulation data.

Dataset Volumes - Customers: 1,000,000 - Transformers: 4,000 - Feeders:
100

Streaming simulations include: - Hourly smart meter telemetry - Payment
transactions - Field operations events

------------------------------------------------------------------------

PROJECT REPOSITORY STRUCTURE

utility-data-platform │ ├── architecture │ ├── system_architecture.md │
└── architecture_diagram.png │ ├── data_model │ ├──
operational_schema.sql │ └── warehouse_schema.sql │ ├── simulation │ ├──
generators │ └── kafka_producers │ ├── ingestion │ ├── kafka │ └── api │
├── processing │ ├── spark_jobs │ └── databricks_jobs │ ├── storage │
└── database_configs │ ├── cdc_pipeline │ ├── debezium │ └──
airflow_dags │ ├── warehouse │ └── snowflake_models │ ├── analytics │
└── powerbi │ ├── infrastructure │ └── docker │ ├── tests │ ├──
docker-compose.yml ├── requirements.txt └── README.md

------------------------------------------------------------------------

INFRASTRUCTURE

The platform is containerized using Docker and Docker Compose to allow
reproducible local development environments.

------------------------------------------------------------------------

RESOURCE REQUIREMENTS

Minimum recommended system resources:

RAM: 16 GB CPU: 8 cores Disk: 50 GB

------------------------------------------------------------------------

HOW TO RUN THE PLATFORM

1.  Install dependencies

-   Docker
-   Git
-   Python

2.  Clone the repository

git clone https://github.com//utility-data-platform.git cd
utility-data-platform

3.  Start infrastructure

docker-compose up -d

4.  Generate synthetic data

python simulation/generators/customer_generator.py

5.  Start event streams

python simulation/kafka_producers/payment_stream.py python
simulation/kafka_producers/meter_stream.py

6.  Trigger ETL pipelines from Airflow UI

------------------------------------------------------------------------

LEARNING OUTCOMES

This project demonstrates practical data engineering skills including:

-   Event driven architecture
-   Real-time streaming pipelines
-   CDC pipelines
-   Distributed data processing
-   Data warehouse modeling
-   Cloud data platforms

------------------------------------------------------------------------

ADDITIONAL ENTERPRISE ENGINEERING PRACTICES

1.  Architecture Decision Records (ADR)

The repository includes ADR documentation describing major architectural
decisions such as:

-   Why Cassandra was chosen for payment streaming storage
-   Why Snowflake was selected as the analytical warehouse
-   Why Kafka was selected for event streaming
-   Why CDC was used for dimension table synchronization

These records document engineering tradeoffs and are stored in:

architecture/adr/

------------------------------------------------------------------------

2.  Pipeline Observability and Monitoring

Production data platforms require monitoring and observability.

Recommended monitoring stack:

-   Pipeline health dashboards
-   Kafka lag monitoring
-   Spark job performance metrics
-   Data freshness monitoring
-   Airflow DAG success/failure alerts

Metrics to monitor:

-   Event ingestion rate
-   Pipeline latency
-   Data processing throughput
-   Failed task retries

------------------------------------------------------------------------

3.  Data Quality Validation Layer

Before loading data into the warehouse, data quality checks are applied.

Validation examples:

-   Null validation for primary keys
-   Meter reading value ranges
-   Payment amount validation
-   Duplicate record detection
-   Referential integrity checks

These tests can be implemented using data validation frameworks and
scheduled within Airflow pipelines.

------------------------------------------------------------------------

LICENSE

MIT License

------------------------------------------------------------------------

AUTHOR

Toluse Alemika

Senior Data Analyst  – BEDC Electricity Plc, 
Data Engineering & Analytics Enthusiast
