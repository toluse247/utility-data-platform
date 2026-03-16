# Utility Data Platform – System Design

## 1. Overview

The **Utility Data Platform** is a modern data engineering architecture designed to ingest, process, store, and analyze operational and customer data from an electricity distribution utility.

The platform integrates **real-time streaming**, **batch ingestion**, **change-data-capture**, and **analytical warehousing** to support operational analytics, billing, monitoring, and executive reporting.

The system simulates the data environment of a power distribution company where millions of customers generate operational events such as:

* Smart meter readings
* Customer payments
* Field service visits
* Customer enrollment and disconnections
* Feeder energy consumption reports
* Operational updates to transformers and feeders

The architecture is designed for **scalability, fault tolerance, and near real-time analytics**.

---

# 2. High-Level Architecture

The platform consists of the following layers:

1. Data Sources
2. Data Ingestion
3. Streaming Processing
4. Storage Systems
5. Data Warehouse
6. Transformation Layer
7. Analytics and Visualization

```
Operational Systems
        │
        ▼
Ingestion Layer
(API / Kafka / Batch / CDC)
        │
        ▼
Streaming Processing
(Spark / Databricks)
        │
        ▼
Storage Layer
(PostgreSQL / Cassandra / MongoDB / S3)
        │
        ▼
Data Warehouse
(Snowflake)
        │
        ▼
Transformation Layer
(dbt)
        │
        ▼
Analytics Layer
(Power BI)
```

---

# 3. Data Sources

The system ingests data from several simulated operational sources:

### Smart Meter Devices

Smart meters periodically send electricity consumption readings.

**Events generated:**

* Meter readings
* Consumption updates

### Payment Channels

Customers pay electricity bills through multiple payment channels such as:

* Mobile banking
* POS terminals
* Online payment gateways

### Field Operations

Field engineers perform operational activities including:

* Meter inspections
* Customer disconnections
* Maintenance visits

### Operational Updates

Administrative updates occur such as:

* Transformer reassignments
* Sales representative changes
* Feeder realignments
* Tariff updates

### Batch Reports

Operational reports such as feeder energy consumption may be delivered as:

* Excel spreadsheets
* Uploaded files

---

# 4. Data Ingestion Layer

The ingestion layer captures data from multiple interfaces.

## 4.1 Streaming Ingestion (Kafka)

Real-time operational events are published into **Kafka topics**.

Example topics:

* `meter_readings`
* `payments`
* `customer_enrollment`
* `disconnections`
* `field_visits`

Kafka producers simulate event streams using the simulation module.

Kafka provides:

* High throughput ingestion
* Fault tolerance
* Horizontal scalability

---

## 4.2 API Ingestion

A REST API accepts operational updates from field applications.

Example endpoints:

* `/field_visit`
* `/disconnection`
* `/customer_enrollment`

The API validates incoming payloads using schema validation before publishing events to Kafka.

---

## 4.3 Batch File Ingestion

Certain operational datasets arrive as batch files.

Examples:

* Feeder energy reports
* Manual meter readings
* Transformer mapping updates

Batch ingestion is handled using scheduled ingestion pipelines orchestrated by Airflow.

---

## 4.4 Change Data Capture (CDC)

Operational database changes are captured using **Debezium**.

CDC captures updates such as:

* Customer information changes
* Transformer assignments
* Tariff modifications

These changes are streamed to Kafka using Kafka Connect and then synchronized into the data warehouse.

---

# 5. Streaming Processing Layer

Real-time processing is implemented using Apache Spark.

Spark Streaming jobs consume Kafka topics and perform transformations such as:

* Payment aggregation
* Meter consumption calculations
* Customer event processing
* Billing calculations

The **billing engine** calculates energy charges using:

```
Energy Charge = Consumption_kWh × Tariff Rate
VAT = Energy Charge × VAT Rate
Billed Amount = Energy Charge + VAT
```

Processed data is written into operational storage systems and the analytical warehouse.

---

# 6. Storage Layer

The platform uses **polyglot persistence**, selecting databases optimized for different workloads.

## PostgreSQL (Operational Database)

Stores structured operational data such as:

* Customers
* Transformers
* Feeders
* Billing records
* Meter readings

PostgreSQL acts as the core operational database.

---

## Cassandra (High-Volume Event Storage)

Cassandra stores high-throughput transactional datasets such as:

* Customer payments

Cassandra is optimized for high write throughput and horizontal scalability.

---

## MongoDB (Semi-Structured Data)

MongoDB stores operational update records such as:

* Customer update requests
* Administrative updates

This allows flexible storage for evolving data structures.

---

## Object Storage (S3)

Object storage stores:

* Raw batch files
* Archived ingestion data
* Intermediate data lake datasets

---

# 7. Data Warehouse Layer

The analytical warehouse is implemented using Snowflake.

Snowflake stores:

* Historical analytics datasets
* Dimension tables
* Fact tables

The warehouse supports analytical workloads such as:

* revenue analytics
* consumption analysis
* operational performance monitoring

---

# 8. Transformation Layer

Data transformations are implemented using dbt.

dbt organizes data into a layered architecture:

### Staging Layer

Standardizes raw data from ingestion sources.

### Intermediate Layer

Applies business logic and joins operational datasets.

### Mart Layer

Produces analytical models used by dashboards and reporting tools.

Example marts:

* `fact_payments`
* `fact_meter_consumption`
* `dim_customer`
* `dim_transformer`
* `dim_region`

---

# 9. Orchestration

Data pipelines are orchestrated using Apache Airflow.

Airflow manages:

* Batch ingestion pipelines
* Data warehouse loading
* Transformation jobs
* Data validation tasks

Example pipelines include:

* payment processing pipeline
* meter consumption pipeline
* transformer update pipelines

---

# 10. Analytics and Reporting

Analytical dashboards are developed using Power BI.

Key dashboards include:

* revenue analytics
* customer payment performance
* feeder energy monitoring
* regional consumption analysis
* operational efficiency dashboards

These dashboards query curated datasets in the Snowflake warehouse.

---

# 11. Monitoring and Observability

The system includes monitoring components that track:

* pipeline execution status
* ingestion throughput
* data processing latency
* error rates

Logging and pipeline metrics are configured within the monitoring infrastructure.

---

# 12. Testing Strategy

The platform includes automated tests for key components:

* Kafka producer validation
* Spark job correctness
* API endpoint testing
* Airflow DAG validation

Automated tests are executed in the CI pipeline during every repository update.

---

# 13. CI/CD Pipeline

Continuous integration is implemented using GitHub Actions.

The CI pipeline performs:

* code validation
* unit testing
* DAG validation
* dependency checks

This ensures platform stability and prevents faulty deployments.

---

# 14. Scalability Considerations

The platform is designed to scale horizontally through:

* distributed Kafka clusters
* scalable Spark processing
* Snowflake elastic warehouses
* Cassandra distributed storage

This enables the system to handle millions of events per day.

---

# 15. Security Considerations

The architecture supports several security best practices:

* API input validation
* access control for storage systems
* encrypted communication between services
* controlled access to the analytics warehouse

---

# 16. Conclusion

The Utility Data Platform demonstrates a complete end-to-end modern data engineering architecture combining:

* real-time streaming pipelines
* batch ingestion workflows
* change-data-capture pipelines
* distributed processing
* scalable storage systems
* analytical data warehousing

The platform provides a foundation for building real-time operational intelligence systems in the energy and utilities sector.
