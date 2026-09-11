-- ============================================
-- E-Commerce Data Warehouse
-- Dimension Tables
-- ============================================

DROP TABLE IF EXISTS warehouse.dim_customer CASCADE;
DROP TABLE IF EXISTS warehouse.dim_product CASCADE;
DROP TABLE IF EXISTS warehouse.dim_location CASCADE;
DROP TABLE IF EXISTS warehouse.dim_payment CASCADE;
DROP TABLE IF EXISTS warehouse.dim_date CASCADE;


-- ============================================
-- DATE DIMENSION
-- ============================================

CREATE TABLE warehouse.dim_date (
    date_sk INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    year INTEGER,
    week INTEGER,
    day_name VARCHAR(20)
);


-- ============================================
-- CUSTOMER DIMENSION
-- SCD TYPE 2
-- ============================================

CREATE TABLE warehouse.dim_customer (
    customer_sk BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100),
    gender VARCHAR(20),
    date_of_birth DATE,
    city VARCHAR(100),
    district VARCHAR(100),
    customer_type VARCHAR(50),
    membership_level VARCHAR(50),

    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);


-- ============================================
-- PRODUCT DIMENSION
-- ============================================

CREATE TABLE warehouse.dim_product (
    product_sk BIGSERIAL PRIMARY KEY,
    product_id VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(150),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost NUMERIC(12,2),
    unit_price NUMERIC(12,2)
);


-- ============================================
-- LOCATION DIMENSION
-- ============================================

CREATE TABLE warehouse.dim_location (
    location_sk BIGSERIAL PRIMARY KEY,
    location_id VARCHAR(20) UNIQUE NOT NULL,
    city VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100),
    country VARCHAR(100)
);


-- ============================================
-- PAYMENT DIMENSION
-- ============================================

CREATE TABLE warehouse.dim_payment (
    payment_sk BIGSERIAL PRIMARY KEY,
    payment_id VARCHAR(20) UNIQUE NOT NULL,
    payment_method VARCHAR(50),
    payment_type VARCHAR(50)
);