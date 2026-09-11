-- ============================================
-- FACT SALES TABLE
-- ============================================

DROP TABLE IF EXISTS warehouse.fact_sales;

CREATE TABLE warehouse.fact_sales (
    sales_sk BIGSERIAL PRIMARY KEY,

    order_line_id VARCHAR(30) UNIQUE NOT NULL,
    order_id VARCHAR(30) NOT NULL,

    date_sk INTEGER NOT NULL,
    customer_sk BIGINT NOT NULL,
    product_sk BIGINT NOT NULL,
    location_sk BIGINT NOT NULL,
    payment_sk BIGINT NOT NULL,

    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,

    sales_amount NUMERIC(14,2) NOT NULL,
    cost_amount NUMERIC(14,2) NOT NULL,
    profit_amount NUMERIC(14,2) NOT NULL,

    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_sk)
        REFERENCES warehouse.dim_date(date_sk),

    CONSTRAINT fk_fact_customer
        FOREIGN KEY (customer_sk)
        REFERENCES warehouse.dim_customer(customer_sk),

    CONSTRAINT fk_fact_product
        FOREIGN KEY (product_sk)
        REFERENCES warehouse.dim_product(product_sk),

    CONSTRAINT fk_fact_location
        FOREIGN KEY (location_sk)
        REFERENCES warehouse.dim_location(location_sk),

    CONSTRAINT fk_fact_payment
        FOREIGN KEY (payment_sk)
        REFERENCES warehouse.dim_payment(payment_sk)
);