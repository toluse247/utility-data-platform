# Technology Stack

## Overview

The Utility Data Platform is built using a **modern data engineering technology stack** designed to support **high-volume data ingestion, real-time processing, operational storage, analytical warehousing, and business intelligence**.

The architecture combines **streaming technologies, distributed processing frameworks, operational databases, and cloud analytics tools** to enable scalable and reliable data processing.

The technology stack follows a layered architecture consisting of:

1. Data Ingestion
2. Event Streaming
3. Processing & Transformation
4. Workflow Orchestration
5. Operational Data Storage
6. Data Warehouse
7. Analytics & Visualization
8. Infrastructure & DevOps

---

# 1. Programming Language

## Python

Python is the primary programming language used across the platform.

It is used for:

* Kafka producers
* API services
* Spark data processing
* Data simulation scripts
* Warehouse loaders
* Workflow orchestration scripts

Reasons for choosing Python:

* Large ecosystem of data engineering libraries
* Strong integration with big data tools
* Excellent support for API development
* Widely adopted in data engineering workflows

Example usage locations:

```
ingestion/kafka/producers/
streaming_processing/spark_jobs/
simulation/
warehouse/snowflake/
```

---

# 2. Data Ingestion Technologies

## Apache Kafka

Apache Kafka serves as the **event streaming backbone** of the platform.

Kafka enables real-time ingestion of operational events such as:

* Meter readings
* Customer payments
* Field visits
* Disconnection actions
* Customer enrollments

Key capabilities:

* High throughput event streaming
* Fault-tolerant message storage
* Horizontal scalability
* Real-time event processing

Kafka components used in the platform:

* Kafka Brokers
* Kafka Producers
* Kafka Topics
* Kafka Connect

Example Kafka topics:

```
meter_readings
payments
field_visits
disconnections
customer_enrollment
```

---

## FastAPI

FastAPI is used to build the platform's **REST API ingestion layer**.

The API allows external operational systems to submit structured events into the data platform.

Examples of API endpoints:

```
/field_visit
/disconnection
/customer_enrollment
```

Key benefits:

* High performance asynchronous API framework
* Built-in request validation using Pydantic
* Automatic OpenAPI documentation
* Lightweight and scalable

---

## Excel Batch Ingestion

Some operational reports are uploaded as Excel files from business teams.

These reports are ingested using **Python-based batch loaders**.

Examples:

* Feeder energy consumption reports
* Manual meter reading uploads
* Transformer mapping updates
* Sales representative realignment files

These batch loaders are orchestrated using Airflow workflows.

---

# 3. Streaming Data Processing

## Apache Spark

Apache Spark is used for **large-scale data processing and streaming transformations**.

Spark jobs process events streamed from Kafka and perform:

* Data validation
* Data enrichment
* Deduplication
* Billing calculations
* Aggregations

Example Spark jobs:

```
process_payments.py
process_field_visits.py
process_disconnections.py
process_customer_enrollment.py
billing_engine.py
```

Key advantages:

* Distributed processing
* High throughput data pipelines
* Native integration with Kafka
* Support for structured streaming

---

## Databricks

Databricks provides a **managed Spark environment** for advanced data processing and analytics.

It is used for:

* Large-scale ETL transformations
* Data exploration
* Advanced analytics workflows
* Collaborative notebook development

Benefits:

* Optimized Spark performance
* Managed cluster environment
* Integrated notebook interface
* Simplified big data operations

---

# 4. Workflow Orchestration

## Apache Airflow

Apache Airflow is used to orchestrate and schedule data pipelines.

Airflow manages:

* Batch ingestion jobs
* Data transformation pipelines
* Data warehouse loading
* Dependency management
* Pipeline monitoring and retries

Example DAGs in the platform:

```
fact_payment_pipeline.py
fact_meter_consumption_pipeline.py
feeder_energy_ingestion.py
manual_meter_readings_ingestion.py
transformer_mapping_updates.py
customer_update_requests_pipeline.py
```

Key advantages:

* Directed Acyclic Graph (DAG) pipeline design
* Flexible scheduling
* Built-in retry mechanisms
* Workflow monitoring dashboard

---

# 5. Change Data Capture (CDC)

## Debezium

Debezium is used to capture **database changes in real time** from PostgreSQL.

Debezium monitors operational tables and streams changes into Kafka topics.

Examples of captured tables:

```
customers
payments
meter_readings
billing_records
```

Benefits:

* Real-time database change streaming
* Event-driven architecture
* Near real-time warehouse updates
* Reduced batch ETL requirements

---

## Kafka Connect

Kafka Connect is used to move data between Kafka and external systems.

In this platform it is used to:

* Stream CDC events into the Snowflake data warehouse

Connector used:

```
Snowflake Sink Connector
```

---

# 6. Operational Databases

## PostgreSQL

PostgreSQL serves as the **primary relational operational database**.

It stores structured transactional data such as:

* Customer accounts
* Transformers
* Feeders
* Meter readings
* Billing records
* Field visits

Reasons for choosing PostgreSQL:

* Strong relational data integrity
* Advanced indexing capabilities
* ACID compliance
* Mature ecosystem

---

## Cassandra

Apache Cassandra is used for **high-volume transaction storage**.

It is used primarily for storing **payment events**.

Advantages:

* High write throughput
* Horizontal scalability
* Fault tolerance
* Distributed architecture

Cassandra works well for **time-series financial transaction data**.

---

## MongoDB

MongoDB is used for storing **semi-structured operational data**.

Example use cases:

* Customer update requests
* Operational logs
* Flexible change tracking

Advantages:

* Flexible schema design
* High availability
* Document-based storage

---

# 7. Data Warehouse

## Snowflake

Snowflake serves as the **central analytical data warehouse**.

It stores historical and analytical data used for reporting and business intelligence.

The warehouse contains:

### Dimension Tables

```
dim_customer
dim_transformer
dim_feeder
dim_service_unit
dim_district
dim_region
dim_sales_rep
dim_band_tariff
```

### Fact Tables

```
fact_meter_consumption
fact_payments
fact_billing
fact_field_visits
```

Advantages:

* Cloud-native architecture
* Automatic scaling
* Separation of compute and storage
* High performance analytical queries

---

# 8. Data Transformation Framework

## dbt (Data Build Tool)

dbt is used for **data modeling and transformation within the warehouse**.

dbt manages SQL transformations and organizes them into modular models.

Project structure:

```
staging/
intermediate/
marts/
```

Responsibilities:

* Data cleaning
* Business logic transformations
* Dimensional modeling
* KPI calculations

Benefits:

* Version-controlled transformations
* Modular SQL development
* Automated documentation
* Data lineage tracking

---

# 9. Data Simulation

To demonstrate the platform end-to-end, the repository includes a **data simulation layer**.

The simulation scripts generate synthetic utility data.

Examples:

### Master Data Generators

```
geography_generator.py
feeder_generator.py
transformer_generator.py
customer_generator.py
```

### Streaming Event Simulators

```
meter_reading_simulator.py
payment_simulator.py
```

### API Event Simulators

```
field_visit_simulator.py
disconnection_simulator.py
customer_enrollment_simulator.py
```

These scripts allow the platform to run **without real production data**.

---

# 10. Analytics and Visualization

## Power BI

Power BI is used for **data visualization and reporting**.

Dashboards provide insights into:

### Revenue Performance

* Revenue billed
* Revenue collected
* Outstanding debt

### Energy Operations

* Feeder energy distribution
* Transformer load
* Energy losses

### Customer Analytics

* Consumption trends
* Payment behavior
* Customer segmentation

Power BI connects directly to the **Snowflake warehouse**.

---

# 11. Infrastructure and Containerization

## Docker

Docker is used to containerize platform components.

Services containerized include:

```
Kafka
Spark
Airflow
Debezium
```

Benefits:

* Environment consistency
* Reproducible deployments
* Simplified local development

---

## Docker Compose

Docker Compose is used to orchestrate the platform's local infrastructure.

The `docker-compose.yml` file defines services such as:

* Kafka brokers
* Spark cluster
* Airflow scheduler
* Airflow webserver
* PostgreSQL
* Debezium

This allows the entire platform to run locally for development and testing.

---

# 12. CI/CD Pipeline

## GitHub Actions

GitHub Actions is used for **continuous integration and automated testing**.

Location:

```
.github/workflows/pipeline_ci.yml
```

CI pipeline tasks include:

* Running unit tests
* Validating Python code
* Checking DAG integrity
* Running Spark job tests

Benefits:

* Automated code quality checks
* Early error detection
* Improved deployment reliability

---

# Conclusion

The Utility Data Platform uses a modern and scalable technology stack that combines **event streaming, distributed data processing, operational databases, and cloud analytics infrastructure**.

This architecture supports:

* Real-time event ingestion
* Scalable data processing
* Reliable operational storage
* Near real-time warehouse updates
* Advanced business analytics

The combination of **Kafka, Spark, Airflow, Debezium, Snowflake, and Power BI** enables a robust end-to-end data engineering platform capable of handling the complex data workflows of a modern electricity distribution company.
