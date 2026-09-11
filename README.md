# E-Commerce Sales Data Warehouse with ETL and Slowly Changing Dimensions

## 1. Project Overview

This project implements an **E-Commerce Sales Data Warehouse** designed to transform raw transactional data into a structured analytical environment.

The project demonstrates the complete data warehousing lifecycle:

**Source Data → Staging → Data Cleaning → Transformation → Dimension Loading → SCD Type 2 → Fact Loading → Analytical Queries → Data Quality Validation**

The solution uses PostgreSQL as the data warehouse database and Python with Pandas for ETL processing.

---

## 2. Project Objectives

The main objectives of this project are to:

* Design a dimensional data warehouse for an e-commerce business.
* Identify suitable source data and business processes.
* Implement staging tables for raw source data.
* Clean and validate source data using Python.
* Transform transactional data into analytical measures.
* Implement dimension tables using surrogate keys.
* Implement Slowly Changing Dimension Type 2 for customer history.
* Develop a sales fact table at transaction-line level.
* Perform analytical queries using SQL.
* Validate data quality and referential integrity.
* Demonstrate how the warehouse supports business decision-making.

---

## 3. Business Domain

The selected business domain is **E-Commerce Sales**.

An e-commerce organization generates large amounts of transactional data involving:

* Customers
* Products
* Locations
* Payment methods
* Orders
* Order lines
* Sales
* Discounts
* Costs
* Profit

A data warehouse allows this information to be organized for historical analysis and business intelligence.

---

## 4. Business Process

The main business process modelled in this project is:

**E-Commerce Order and Sales Processing**

The warehouse records individual order lines.

### Fact Table Grain

The grain of the fact table is:

> **One row represents one product line within one customer order.**

This grain allows the business to analyse sales at product, customer, location, payment, and date levels.

---

## 5. Technology Stack

| Technology           | Purpose                                      |
| -------------------- | -------------------------------------------- |
| Python 3.12          | ETL and source data generation               |
| Pandas               | Data extraction, cleaning and transformation |
| NumPy                | Data generation and processing               |
| PostgreSQL 18        | Data warehouse database                      |
| pgAdmin 4            | Database management and SQL execution        |
| SQLAlchemy           | Python-to-PostgreSQL connection              |
| psycopg2             | PostgreSQL database driver                   |
| python-dotenv        | Environment variable management              |
| Git                  | Version control                              |
| GitHub               | Source code repository                       |
| diagrams.net         | Data warehouse diagrams                      |
| Microsoft Word       | Project report                               |
| Microsoft PowerPoint | Project presentation                         |

---

## 6. Source Data

The project uses CSV files as source data.

### Customers

`data/source/customers.csv`

Contains customer information including:

* Customer ID
* Customer name
* Gender
* Date of birth
* City
* District
* Customer type
* Membership level

### Products

`data/source/products.csv`

Contains:

* Product ID
* Product name
* Category
* Subcategory
* Brand
* Unit cost
* Unit price

### Locations

`data/source/locations.csv`

Contains:

* Location ID
* City
* District
* Province
* Country

### Payments

`data/source/payments.csv`

Contains:

* Payment ID
* Payment method
* Payment type

### Orders

`data/source/orders.csv`

Contains:

* Order line ID
* Order ID
* Order date
* Customer ID
* Product ID
* Location ID
* Payment ID
* Quantity
* Discount amount

---

## 7. Generated Dataset

The initial source dataset contains:

| Dataset     | Records |
| ----------- | ------: |
| Customers   |     100 |
| Products    |      48 |
| Locations   |       8 |
| Payments    |       5 |
| Order Lines |     700 |

The data generation process is implemented in:

`etl/generate_data.py`

---

## 8. Data Warehouse Architecture

The project follows a layered architecture:

```text
CSV Source Files
       ↓
Python ETL
       ↓
Staging Layer
       ↓
Cleaning & Validation
       ↓
Transformation
       ↓
Dimension Tables
       ↓
SCD Type 2 Customer History
       ↓
Fact Sales Table
       ↓
Analytical SQL
       ↓
Business Insights
```

---

## 9. Database Schemas

The PostgreSQL database is:

`ecommerce_dw`

Two main schemas are used:

### Staging Schema

Stores extracted and cleaned source data before warehouse loading.

Tables:

* `staging.stg_customers`
* `staging.stg_products`
* `staging.stg_locations`
* `staging.stg_payments`
* `staging.stg_orders`

### Warehouse Schema

Contains the dimensional model.

Tables:

* `warehouse.dim_customer`
* `warehouse.dim_product`
* `warehouse.dim_location`
* `warehouse.dim_payment`
* `warehouse.dim_date`
* `warehouse.fact_sales`

---

## 10. Dimensional Model

The warehouse follows a **star schema**.

### Dimension Tables

* Customer Dimension
* Product Dimension
* Location Dimension
* Payment Dimension
* Date Dimension

### Fact Table

* Sales Fact

The fact table contains foreign keys to the dimensions and quantitative business measures.

---

## 11. Slowly Changing Dimension Type 2

Customer information is implemented using **Slowly Changing Dimension Type 2**.

The customer dimension stores:

* Effective start date
* Effective end date
* Current status

When a tracked customer attribute changes, the existing record is closed and a new version is created.

For example:

```text
C001
│
├── Historical Version
│   City: Colombo
│   Start: 2026-08-01
│   End: 2026-08-31
│   Current: FALSE
│
└── Current Version
    City: Kandy
    Start: 2026-09-01
    End: 9999-12-31
    Current: TRUE
```

This preserves historical customer information.

---

## 12. ETL Process

The ETL pipeline performs:

### Extract

Reads CSV source files using Pandas.

### Transform

Performs:

* Duplicate removal
* String cleaning
* Date conversion
* Quantity validation
* Discount validation
* Product and order transformations
* Sales calculation
* Cost calculation
* Profit calculation

### Load

Loads the transformed data into:

* Staging tables
* Dimension tables
* Customer SCD Type 2
* Sales fact table

The main ETL program is:

`etl/etl_pipeline.py`

---

## 13. Sales Calculations

The warehouse calculates the following measures:

### Gross Sales

```text
Gross Sales = Quantity × Unit Price
```

### Net Sales

```text
Net Sales = Gross Sales − Discount
```

### Cost

```text
Cost = Quantity × Unit Cost
```

### Profit

```text
Profit = Gross Sales − Discount − Cost
```

---

## 14. Analytical Queries

The project provides analytical SQL queries for:

1. Monthly sales
2. Top products
3. Top customers
4. Profit by category
5. Sales by city
6. Payment method performance
7. Profit margin by category
8. Monthly profit
9. Membership performance
10. Average order value

The queries are stored in:

`sql/01_analytical_queries.sql`

---

## 15. Data Quality Testing

Validation queries are stored in:

`sql/02_validation_queries.sql`

The project validates:

* Null foreign keys
* Invalid quantities
* Negative sales
* Duplicate current customer versions
* Historical SCD records
* Fact table row count
* Orphan product records
* Orphan customer records

---

## 16. Reproducibility

The project can be reproduced by:

1. Creating the PostgreSQL database.
2. Creating the staging and warehouse schemas.
3. Installing Python dependencies.
4. Generating source data.
5. Running the ETL pipeline.
6. Executing analytical SQL queries.
7. Executing validation queries.

---

## 17. Environment Configuration

Database credentials are stored in a local `.env` file.

Example:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_dw
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
```

The `.env` file is intentionally excluded from GitHub for security.

---

## 18. Project Team

### Omaya Nayagara

Project Leader / Data Warehouse & ETL Lead

Responsibilities:

* Data warehouse architecture
* Database implementation
* ETL pipeline
* SCD Type 2
* Fact and dimension implementation
* SQL analytics
* Integration
* Final submission

### Bosilu Pupulewela

Design & Presentation Lead

Responsibilities:

* Data warehouse diagrams
* Presentation design
* Visual documentation
* Report formatting

### Dulakshi Hashinika

Data, Analytics & Documentation Lead

Responsibilities:

* Dataset support
* Analytical queries
* Data validation
* Documentation
* Testing support

---

## 19. Repository Structure

```text
data/          Source and Run 2 datasets
database/      Database creation SQL
diagrams/      Architecture and dimensional diagrams
etl/           Python ETL programs
sql/           Analytical and validation SQL
screenshots/   Project evidence
presentation/  Presentation files
reports/       Final report
```

---

## 20. Conclusion

This project demonstrates how an e-commerce organization can transform operational transaction data into a structured data warehouse suitable for historical analysis and business intelligence.

The implementation demonstrates dimensional modelling, ETL, surrogate keys, Slowly Changing Dimension Type 2, fact table design, analytical SQL and data quality validation.

The resulting warehouse provides a foundation for analysing sales, products, customers, locations, payment methods and profitability.
