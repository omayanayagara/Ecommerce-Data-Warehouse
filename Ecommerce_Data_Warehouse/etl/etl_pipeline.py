import os
from datetime import date
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================
# CONFIGURATION
# ============================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "data", "source")

load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ============================================
# LOAD CSV FILES
# ============================================

print("\n================================")
print("1. EXTRACT")
print("================================")

customers = pd.read_csv(
    os.path.join(SOURCE_DIR, "customers.csv")
)

products = pd.read_csv(
    os.path.join(SOURCE_DIR, "products.csv")
)

locations = pd.read_csv(
    os.path.join(SOURCE_DIR, "locations.csv")
)

payments = pd.read_csv(
    os.path.join(SOURCE_DIR, "payments.csv")
)

orders = pd.read_csv(
    os.path.join(SOURCE_DIR, "orders.csv")
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
).dt.date

customers["date_of_birth"] = pd.to_datetime(
    customers["date_of_birth"]
).dt.date

print(f"Customers: {len(customers)}")
print(f"Products : {len(products)}")
print(f"Orders   : {len(orders)}")


# ============================================
# CLEANING
# ============================================

print("\n================================")
print("2. CLEANING / VALIDATION")
print("================================")

customers = customers.drop_duplicates(
    subset=["customer_id"]
)

products = products.drop_duplicates(
    subset=["product_id"]
)

locations = locations.drop_duplicates(
    subset=["location_id"]
)

payments = payments.drop_duplicates(
    subset=["payment_id"]
)

orders = orders.drop_duplicates(
    subset=["order_line_id"]
)

customers["customer_name"] = (
    customers["customer_name"].str.strip()
)

customers["city"] = (
    customers["city"].str.strip()
)

products["product_name"] = (
    products["product_name"].str.strip()
)

orders = orders[
    orders["quantity"] > 0
]

orders["discount_amount"] = (
    orders["discount_amount"].fillna(0)
)

orders = orders[
    orders["discount_amount"] >= 0
]

print("Validation completed.")


# ============================================
# STAGING LOAD
# ============================================

print("\n================================")
print("3. LOAD STAGING")
print("================================")

with engine.begin() as conn:

    conn.execute(
        text("TRUNCATE TABLE staging.stg_orders")
    )

    conn.execute(
        text("TRUNCATE TABLE staging.stg_customers")
    )

    conn.execute(
        text("TRUNCATE TABLE staging.stg_products")
    )

    conn.execute(
        text("TRUNCATE TABLE staging.stg_locations")
    )

    conn.execute(
        text("TRUNCATE TABLE staging.stg_payments")
    )


customers.to_sql(
    "stg_customers",
    engine,
    schema="staging",
    if_exists="append",
    index=False
)

products.to_sql(
    "stg_products",
    engine,
    schema="staging",
    if_exists="append",
    index=False
)

locations.to_sql(
    "stg_locations",
    engine,
    schema="staging",
    if_exists="append",
    index=False
)

payments.to_sql(
    "stg_payments",
    engine,
    schema="staging",
    if_exists="append",
    index=False
)

orders.to_sql(
    "stg_orders",
    engine,
    schema="staging",
    if_exists="append",
    index=False
)

print("Staging load completed.")


# ============================================
# LOAD PRODUCT DIMENSION
# ============================================

print("\n================================")
print("4. LOAD DIMENSIONS")
print("================================")

with engine.begin() as conn:

    for _, row in products.iterrows():

        conn.execute(
            text("""
                INSERT INTO warehouse.dim_product
                (
                    product_id,
                    product_name,
                    category,
                    subcategory,
                    brand,
                    unit_cost,
                    unit_price
                )
                VALUES
                (
                    :product_id,
                    :product_name,
                    :category,
                    :subcategory,
                    :brand,
                    :unit_cost,
                    :unit_price
                )
                ON CONFLICT (product_id)
                DO UPDATE SET
                    product_name = EXCLUDED.product_name,
                    category = EXCLUDED.category,
                    subcategory = EXCLUDED.subcategory,
                    brand = EXCLUDED.brand,
                    unit_cost = EXCLUDED.unit_cost,
                    unit_price = EXCLUDED.unit_price
            """),
            row.to_dict()
        )


# ============================================
# LOCATION DIMENSION
# ============================================

    for _, row in locations.iterrows():

        conn.execute(
            text("""
                INSERT INTO warehouse.dim_location
                (
                    location_id,
                    city,
                    district,
                    province,
                    country
                )
                VALUES
                (
                    :location_id,
                    :city,
                    :district,
                    :province,
                    :country
                )
                ON CONFLICT (location_id)
                DO UPDATE SET
                    city = EXCLUDED.city,
                    district = EXCLUDED.district,
                    province = EXCLUDED.province,
                    country = EXCLUDED.country
            """),
            row.to_dict()
        )


# ============================================
# PAYMENT DIMENSION
# ============================================

    for _, row in payments.iterrows():

        conn.execute(
            text("""
                INSERT INTO warehouse.dim_payment
                (
                    payment_id,
                    payment_method,
                    payment_type
                )
                VALUES
                (
                    :payment_id,
                    :payment_method,
                    :payment_type
                )
                ON CONFLICT (payment_id)
                DO UPDATE SET
                    payment_method = EXCLUDED.payment_method,
                    payment_type = EXCLUDED.payment_type
            """),
            row.to_dict()
        )


# ============================================
# CUSTOMER SCD TYPE 2
# ============================================

print("\n================================")
print("5. SCD TYPE 2")
print("================================")

RUN_DATE = date(2026, 8, 1)

new_count = 0
changed_count = 0
unchanged_count = 0

customer_columns = [
    "customer_name",
    "gender",
    "date_of_birth",
    "city",
    "district",
    "customer_type",
    "membership_level"
]

with engine.begin() as conn:

    for _, row in customers.iterrows():

        existing = conn.execute(
            text("""
                SELECT *
                FROM warehouse.dim_customer
                WHERE customer_id = :customer_id
                AND is_current = TRUE
            """),
            {
                "customer_id": row["customer_id"]
            }
        ).mappings().first()

        if existing is None:

            conn.execute(
                text("""
                    INSERT INTO warehouse.dim_customer
                    (
                        customer_id,
                        customer_name,
                        gender,
                        date_of_birth,
                        city,
                        district,
                        customer_type,
                        membership_level,
                        effective_start_date,
                        effective_end_date,
                        is_current
                    )
                    VALUES
                    (
                        :customer_id,
                        :customer_name,
                        :gender,
                        :date_of_birth,
                        :city,
                        :district,
                        :customer_type,
                        :membership_level,
                        :start_date,
                        '9999-12-31',
                        TRUE
                    )
                """),
                {
                    **row.to_dict(),
                    "start_date": RUN_DATE
                }
            )

            new_count += 1

        else:

            changed = any(
                str(existing[col]) != str(row[col])
                for col in customer_columns
            )

            if changed:

                conn.execute(
                    text("""
                        UPDATE warehouse.dim_customer
                        SET
                            effective_end_date = :end_date,
                            is_current = FALSE
                        WHERE customer_sk = :customer_sk
                    """),
                    {
                        "end_date": RUN_DATE,
                        "customer_sk": existing["customer_sk"]
                    }
                )

                conn.execute(
                    text("""
                        INSERT INTO warehouse.dim_customer
                        (
                            customer_id,
                            customer_name,
                            gender,
                            date_of_birth,
                            city,
                            district,
                            customer_type,
                            membership_level,
                            effective_start_date,
                            effective_end_date,
                            is_current
                        )
                        VALUES
                        (
                            :customer_id,
                            :customer_name,
                            :gender,
                            :date_of_birth,
                            :city,
                            :district,
                            :customer_type,
                            :membership_level,
                            :start_date,
                            '9999-12-31',
                            TRUE
                        )
                    """),
                    {
                        **row.to_dict(),
                        "start_date": RUN_DATE
                    }
                )

                changed_count += 1

            else:
                unchanged_count += 1


print(f"New customers      : {new_count}")
print(f"Changed customers  : {changed_count}")
print(f"Unchanged customers: {unchanged_count}")


# ============================================
# FACT TABLE
# ============================================

print("\n================================")
print("6. LOAD FACT TABLE")
print("================================")

orders = orders.merge(
    products[
        [
            "product_id",
            "unit_cost",
            "unit_price"
        ]
    ],
    on="product_id",
    how="left"
)

orders["sales_amount"] = (
    orders["quantity"] *
    orders["unit_price"]
)

orders["cost_amount"] = (
    orders["quantity"] *
    orders["unit_cost"]
)

orders["profit_amount"] = (
    orders["sales_amount"]
    - orders["discount_amount"]
    - orders["cost_amount"]
)

fact_count = 0

with engine.begin() as conn:

    for _, row in orders.iterrows():

        exists = conn.execute(
            text("""
                SELECT 1
                FROM warehouse.fact_sales
                WHERE order_line_id = :order_line_id
            """),
            {
                "order_line_id": row["order_line_id"]
            }
        ).first()

        if exists:
            continue

        customer_sk = conn.execute(
            text("""
                SELECT customer_sk
                FROM warehouse.dim_customer
                WHERE customer_id = :customer_id
                AND effective_start_date <= :order_date
                AND effective_end_date >= :order_date
                ORDER BY effective_start_date DESC
                LIMIT 1
            """),
            {
                "customer_id": row["customer_id"],
                "order_date": row["order_date"]
            }
        ).scalar()

        product_sk = conn.execute(
            text("""
                SELECT product_sk
                FROM warehouse.dim_product
                WHERE product_id = :product_id
            """),
            {
                "product_id": row["product_id"]
            }
        ).scalar()

        location_sk = conn.execute(
            text("""
                SELECT location_sk
                FROM warehouse.dim_location
                WHERE location_id = :location_id
            """),
            {
                "location_id": row["location_id"]
            }
        ).scalar()

        payment_sk = conn.execute(
            text("""
                SELECT payment_sk
                FROM warehouse.dim_payment
                WHERE payment_id = :payment_id
            """),
            {
                "payment_id": row["payment_id"]
            }
        ).scalar()

        date_sk = int(
            pd.to_datetime(row["order_date"]).strftime("%Y%m%d")
        )

        conn.execute(
            text("""
                INSERT INTO warehouse.fact_sales
                (
                    order_line_id,
                    order_id,
                    date_sk,
                    customer_sk,
                    product_sk,
                    location_sk,
                    payment_sk,
                    quantity,
                    unit_price,
                    discount_amount,
                    sales_amount,
                    cost_amount,
                    profit_amount
                )
                VALUES
                (
                    :order_line_id,
                    :order_id,
                    :date_sk,
                    :customer_sk,
                    :product_sk,
                    :location_sk,
                    :payment_sk,
                    :quantity,
                    :unit_price,
                    :discount_amount,
                    :sales_amount,
                    :cost_amount,
                    :profit_amount
                )
            """),
            {
                "order_line_id": row["order_line_id"],
                "order_id": row["order_id"],
                "date_sk": date_sk,
                "customer_sk": customer_sk,
                "product_sk": product_sk,
                "location_sk": location_sk,
                "payment_sk": payment_sk,
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
                "discount_amount": float(row["discount_amount"]),
                "sales_amount": float(row["sales_amount"]),
                "cost_amount": float(row["cost_amount"]),
                "profit_amount": float(row["profit_amount"])
            }
        )

        fact_count += 1


print(f"New fact rows: {fact_count}")

print("\n================================")
print("ETL PIPELINE COMPLETED")
print("================================")