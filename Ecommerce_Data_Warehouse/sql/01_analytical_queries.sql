-- ============================================
-- E-COMMERCE DATA WAREHOUSE
-- ANALYTICAL SQL QUERIES
-- ============================================


-- ============================================
-- QUERY 1: MONTHLY SALES
-- ============================================

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.sales_amount) AS gross_sales,
    SUM(f.discount_amount) AS discounts,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_date d
    ON f.date_sk = d.date_sk
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- ============================================
-- QUERY 2: TOP 10 PRODUCTS
-- ============================================

SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_product p
    ON f.product_sk = p.product_sk
GROUP BY
    p.product_name,
    p.category
ORDER BY net_sales DESC
LIMIT 10;


-- ============================================
-- QUERY 3: TOP 10 CUSTOMERS
-- ============================================

SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_customer c
    ON f.customer_sk = c.customer_sk
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY net_sales DESC
LIMIT 10;


-- ============================================
-- QUERY 4: PROFIT BY CATEGORY
-- ============================================

SELECT
    p.category,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.cost_amount) AS total_cost,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_product p
    ON f.product_sk = p.product_sk
GROUP BY p.category
ORDER BY profit DESC;


-- ============================================
-- QUERY 5: SALES BY CITY
-- ============================================

SELECT
    l.city,
    l.district,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_location l
    ON f.location_sk = l.location_sk
GROUP BY
    l.city,
    l.district
ORDER BY net_sales DESC;


-- ============================================
-- QUERY 6: PAYMENT METHOD PERFORMANCE
-- ============================================

SELECT
    p.payment_method,
    COUNT(*) AS transaction_lines,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_payment p
    ON f.payment_sk = p.payment_sk
GROUP BY p.payment_method
ORDER BY net_sales DESC;


-- ============================================
-- QUERY 7: PROFIT MARGIN BY CATEGORY
-- ============================================

SELECT
    p.category,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit,
    ROUND(
        100.0 * SUM(f.profit_amount)
        / NULLIF(
            SUM(f.sales_amount - f.discount_amount),
            0
        ),
        2
    ) AS profit_margin_percentage
FROM warehouse.fact_sales f
JOIN warehouse.dim_product p
    ON f.product_sk = p.product_sk
GROUP BY p.category
ORDER BY profit_margin_percentage DESC;


-- ============================================
-- QUERY 8: MONTHLY PROFIT
-- ============================================

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.profit_amount) AS total_profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_date d
    ON f.date_sk = d.date_sk
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- ============================================
-- QUERY 9: MEMBERSHIP PERFORMANCE
-- ============================================

SELECT
    c.membership_level,
    COUNT(DISTINCT c.customer_id) AS customers,
    SUM(f.sales_amount - f.discount_amount) AS net_sales,
    SUM(f.profit_amount) AS profit
FROM warehouse.fact_sales f
JOIN warehouse.dim_customer c
    ON f.customer_sk = c.customer_sk
GROUP BY c.membership_level
ORDER BY net_sales DESC;


-- ============================================
-- QUERY 10: AVERAGE ORDER VALUE
-- ============================================

SELECT
    ROUND(
        SUM(f.sales_amount - f.discount_amount)
        / NULLIF(COUNT(DISTINCT f.order_id), 0),
        2
    ) AS average_order_value
FROM warehouse.fact_sales f;