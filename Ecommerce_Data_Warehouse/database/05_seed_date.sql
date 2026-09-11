-- ============================================
-- DATE DIMENSION DATA
-- ============================================

INSERT INTO warehouse.dim_date (
    date_sk,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    week,
    day_name
)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER AS date_sk,
    d::DATE AS full_date,
    EXTRACT(DAY FROM d)::INTEGER AS day,
    EXTRACT(MONTH FROM d)::INTEGER AS month,
    TO_CHAR(d, 'FMMonth') AS month_name,
    EXTRACT(QUARTER FROM d)::INTEGER AS quarter,
    EXTRACT(YEAR FROM d)::INTEGER AS year,
    EXTRACT(WEEK FROM d)::INTEGER AS week,
    TO_CHAR(d, 'FMDay') AS day_name
FROM generate_series(
    '2026-01-01'::DATE,
    '2027-12-31'::DATE,
    '1 day'::INTERVAL
) AS d
ON CONFLICT (date_sk) DO NOTHING;