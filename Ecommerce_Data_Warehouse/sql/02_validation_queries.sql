-- ============================================
-- E-COMMERCE DATA WAREHOUSE
-- DATA QUALITY VALIDATION
-- ============================================


-- ============================================
-- TEST 1: NULL FOREIGN KEYS
-- Expected: 0 rows
-- ============================================

SELECT *
FROM warehouse.fact_sales
WHERE date_sk IS NULL
   OR customer_sk IS NULL
   OR product_sk IS NULL
   OR location_sk IS NULL
   OR payment_sk IS NULL;


-- ============================================
-- TEST 2: INVALID QUANTITY
-- Expected: 0 rows
-- ============================================

SELECT *
FROM warehouse.fact_sales
WHERE quantity <= 0;


-- ============================================
-- TEST 3: NEGATIVE SALES
-- Expected: 0 rows
-- ============================================

SELECT *
FROM warehouse.fact_sales
WHERE sales_amount < 0;


-- ============================================
-- TEST 4: DUPLICATE CURRENT CUSTOMERS
-- Expected: 0 rows
-- ============================================

SELECT
    customer_id,
    COUNT(*) AS current_versions
FROM warehouse.dim_customer
WHERE is_current = TRUE
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- ============================================
-- TEST 5: HISTORICAL SCD RECORDS
-- Expected: C001 should have more than one version
-- ============================================

SELECT
    customer_id,
    COUNT(*) AS versions
FROM warehouse.dim_customer
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- ============================================
-- TEST 6: FACT ROW COUNT
-- ============================================

SELECT COUNT(*) AS fact_row_count
FROM warehouse.fact_sales;


-- ============================================
-- TEST 7: ORPHAN PRODUCT RECORDS
-- Expected: 0 rows
-- ============================================

SELECT f.*
FROM warehouse.fact_sales f
LEFT JOIN warehouse.dim_product p
    ON f.product_sk = p.product_sk
WHERE p.product_sk IS NULL;


-- ============================================
-- TEST 8: ORPHAN CUSTOMER RECORDS
-- Expected: 0 rows
-- ============================================

SELECT f.*
FROM warehouse.fact_sales f
LEFT JOIN warehouse.dim_customer c
    ON f.customer_sk = c.customer_sk
WHERE c.customer_sk IS NULL;