# E-Commerce Sales Data Warehouse with ETL and SCD Type 2

## Project Overview

This project implements an E-Commerce Sales Data Warehouse using PostgreSQL, Python, Pandas and SQL.

## Business Process

Online Sales Transactions

## Technology Stack

- PostgreSQL
- Python
- Pandas
- SQLAlchemy
- psycopg2
- SQL
- Git
- GitHub

## Architecture

Source CSV files → Staging → Cleaning & Validation → Transformation → Dimensions → SCD Type 2 → Fact Table → Analytical SQL

## Data Warehouse Model

The warehouse uses a star schema consisting of:

- Fact_Sales
- Dim_Date
- Dim_Customer
- Dim_Product
- Dim_Location
- Dim_Payment

## Slowly Changing Dimension

The Customer Dimension implements Slowly Changing Dimension Type 2 to preserve historical changes to customer attributes.

## Team

- Omaya Nayagara - CIT-24-01-0373 — Project Lead / Technical Lead
- Bosilu Pupulewela - CIT-24-01-0471 — Design & Presentation
- Dulakshi Hashinika CIT-24-01-0241 — Data, Analytics & Documentation 