-- ============================================
-- E-Commerce Data Warehouse
-- Staging Tables
-- ============================================

DROP TABLE IF EXISTS staging.stg_orders;
DROP TABLE IF EXISTS staging.stg_customers;
DROP TABLE IF EXISTS staging.stg_products;
DROP TABLE IF EXISTS staging.stg_locations;
DROP TABLE IF EXISTS staging.stg_payments;

CREATE TABLE staging.stg_customers (
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    gender VARCHAR(20),
    date_of_birth DATE,
    city VARCHAR(100),
    district VARCHAR(100),
    customer_type VARCHAR(50),
    membership_level VARCHAR(50)
);

CREATE TABLE staging.stg_products (
    product_id VARCHAR(20),
    product_name VARCHAR(150),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost NUMERIC(12,2),
    unit_price NUMERIC(12,2)
);

CREATE TABLE staging.stg_locations (
    location_id VARCHAR(20),
    city VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE staging.stg_payments (
    payment_id VARCHAR(20),
    payment_method VARCHAR(50),
    payment_type VARCHAR(50)
);

CREATE TABLE staging.stg_orders (
    order_line_id VARCHAR(30),
    order_id VARCHAR(30),
    order_date DATE,
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    location_id VARCHAR(20),
    payment_id VARCHAR(20),
    quantity INTEGER,
    discount_amount NUMERIC(12,2)
);