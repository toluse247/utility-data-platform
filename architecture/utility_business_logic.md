# Utility Business Logic

## Overview

This document describes the **core business logic of the electricity distribution system** implemented in the Utility Data Platform. The logic reflects how electricity distribution companies operate, including **energy delivery, billing, revenue collection, customer management, and field operations**.

The platform models the operational structure of a typical electricity distribution company and implements the rules required to calculate **electricity consumption, billing amounts, arrears, tariff application, and payment reconciliation**.

---

# 1. Electricity Distribution Hierarchy

Electricity flows through a hierarchical distribution structure before reaching customers.

```
Region
   └── District
        └── Service Unit
             └── Feeder
                  └── Transformer
                       └── Customer
```

### Regions

A region represents a large geographic area of operation.

Example:

* Edo Region
* Delta Region

Table:

```
regions
```

---

### Districts

Each region contains multiple districts responsible for local operations.

Table:

```
districts
```

---

### Service Units

Service units manage day-to-day technical and commercial activities such as:

* Metering
* Fault management
* Customer service
* Billing operations

Table:

```
service_units
```

---

### Feeders

A feeder is a **high-voltage distribution line** supplying electricity to multiple transformers.

Characteristics:

* Each feeder belongs to a service unit.
* Each feeder has a **tariff band classification**.
* Energy delivered through feeders is monitored monthly.

Table:

```
feeders
```

---

### Transformers

Transformers step down electricity voltage before distribution to customers.

Each transformer:

* Belongs to a feeder
* Is managed by a sales representative
* Serves multiple customers

Table:

```
transformers
```

---

### Customers

Customers represent the final electricity consumers.

Each customer:

* Is connected to a transformer
* Has a meter number
* Has a billing account
* Generates meter readings
* Makes electricity payments

Table:

```
customers
```

Customer types may include:

| Code | Description |
| ---- | ----------- |
| R    | Residential |
| C    | Commercial  |
| I    | Industrial  |

---

# 2. Tariff and Band System

Electricity pricing is determined using a **band tariff system**.

Table:

```
band_tariff
```

Each band defines:

* Energy tariff rate (cost per kWh)
* VAT rate
* Feeder classification

Example:

| Band | Tariff Rate | VAT      |
| ---- | ----------- | -------- |
| A    | High        | Standard |
| B    | Medium      | Standard |
| C    | Low         | Standard |

Feeder tariff band determines **customer billing rates**.

---

# 3. Meter Reading Logic

Electricity consumption is measured using **customer meter readings**.

Table:

```
meter_readings
```

Each reading contains:

* Meter number
* Customer ID
* Reading date
* Meter value

---

### Consumption Calculation

Customer consumption is calculated using the formula:

```
Consumption (kWh) =
Present Reading − Previous Reading
```

Example:

| Previous Reading | Present Reading | Consumption |
| ---------------- | --------------- | ----------- |
| 12500            | 12740           | 240 kWh     |

---

### Handling Missing Readings

If meter readings are unavailable:

The system may use:

1. Estimated consumption
2. Historical average consumption
3. Feeder allocation estimates

---

# 4. Billing Calculation Logic

Billing records are generated monthly.

Table:

```
billing_records
```

Each bill contains:

* Meter consumption
* Tariff rate
* VAT
* Previous arrears
* Payments received

---

## Step 1: Energy Charge Calculation

```
Energy Charge =
Consumption × Tariff Rate
```

Example:

```
Consumption = 240 kWh
Tariff = ₦60 / kWh

Energy Charge = 240 × 60
Energy Charge = ₦14,400
```

---

## Step 2: VAT Calculation

```
VAT = Energy Charge × VAT Rate
```

Example:

```
VAT Rate = 7.5%

VAT = 14,400 × 0.075
VAT = ₦1,080
```

---

## Step 3: Total Billed Amount

```
Billed Amount =
Energy Charge + VAT
```

Example:

```
Billed Amount = 14,400 + 1,080
Billed Amount = ₦15,480
```

---

# 5. Arrears and Outstanding Balance Logic

Customers may have outstanding balances from previous months.

The system calculates arrears using the following fields:

* Previous balance
* Previous payments
* Previous adjustments

---

### Net Arrears Calculation

```
Net Arrears =
Previous Balance − Previous Payments − Previous Adjustments
```

Example:

```
Previous Balance = ₦20,000
Payments = ₦8,000
Adjustments = ₦2,000

Net Arrears = 20,000 − 8,000 − 2,000
Net Arrears = ₦10,000
```

---

### Final Outstanding Amount

```
Outstanding Amount =
Billed Amount + Net Arrears
```

Example:

```
Billed Amount = ₦15,480
Net Arrears = ₦10,000

Outstanding Amount = ₦25,480
```

---

# 6. Payment Processing Logic

Customers make payments through multiple channels.

Table:

```
payments
```

Supported payment channels include:

* POS
* Bank transfer
* Mobile payment
* Online payment gateway

Each payment contains:

* Customer ID
* Payment amount
* Payment channel
* Timestamp

---

### Payment Reconciliation

Payments are applied to the customer's outstanding balance.

Payment allocation follows the rule:

```
Payments are applied to the oldest outstanding bill first.
```

This ensures correct debt reconciliation.

---

# 7. Feeder Energy Monitoring

Electricity delivered through feeders is tracked monthly.

Table:

```
feeder_energy_consumption
```

Fields include:

* Feeder ID
* Feeder name
* Consumption month
* Total feeder energy

---

### Energy Loss Calculation

Distribution companies monitor **technical and commercial losses**.

```
Energy Loss =
Feeder Energy − Total Customer Consumption
```

Example:

```
Feeder Energy = 100,000 kWh
Customer Consumption = 85,000 kWh

Loss = 15,000 kWh
Loss Percentage = 15%
```

Losses may be caused by:

* Technical losses
* Energy theft
* Meter bypass
* Billing inefficiencies

---

# 8. Field Operations Logic

Sales representatives perform operational activities.

Table:

```
field_visits
```

Visit types include:

* Meter inspection
* Debt recovery visit
* Customer complaint investigation
* Disconnection enforcement

Field operations support:

* Revenue protection
* Customer service
* Network monitoring

---

# 9. Operational Update Processes

Operational changes occur frequently within the network structure.

The platform tracks these updates using dedicated audit tables.

---

### Transformer Feeder Updates

Table:

```
feeder_update_records
```

Tracks cases where a transformer is moved to a new feeder.

---

### Sales Representative Realignment

Table:

```
sales_rep_update_records
```

Tracks reassignment of transformers to different sales representatives.

---

### Tariff Band Updates

Table:

```
band_update_records
```

Tracks feeder band classification changes.

---

### Tariff Rate Updates

Table:

```
tariff_rate_update_records
```

Tracks changes to electricity pricing.

---

### VAT Rate Updates

Table:

```
vat_rate_update_records
```

Tracks VAT policy changes.

---

# 10. Billing Engine Workflow

The billing engine performs the following steps each billing cycle:

```
1. Retrieve customer meter readings
2. Calculate energy consumption
3. Retrieve applicable tariff rate
4. Compute energy charge
5. Calculate VAT
6. Add previous arrears
7. Apply payments received
8. Generate billing record
9. Update outstanding balance
```

This process is implemented in the Spark job:

```
billing_engine.py
```

---

# 11. Key Business KPIs

The platform enables tracking of key utility performance metrics.

### Revenue Metrics

* Total billed revenue
* Total payments collected
* Outstanding receivables

---

### Operational Metrics

* Feeder energy delivered
* Customer consumption
* Energy loss percentage

---

### Commercial Metrics

* Collection efficiency
* Average revenue per customer
* Debt recovery rate

---

# Conclusion

The Utility Data Platform models the operational structure and financial processes of an electricity distribution company. By combining **real-time streaming, batch ingestion, operational databases, and analytical warehousing**, the system enables:

* Accurate billing
* Efficient revenue tracking
* Energy loss monitoring
* Operational transparency
* Data-driven decision making.
