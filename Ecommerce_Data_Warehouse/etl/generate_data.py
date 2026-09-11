import os
import random
from datetime import date, timedelta

import pandas as pd


random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "data", "source")

os.makedirs(SOURCE_DIR, exist_ok=True)


# ============================================
# CUSTOMERS
# ============================================

first_names = [
    "Kasun", "Nimal", "Amaya", "Sahan", "Dilshan",
    "Tharushi", "Kavindi", "Sithum", "Dulakshi", "Bosily"
]

last_names = [
    "Perera", "Fernando", "Silva", "Jayasinghe",
    "Bandara", "Gunawardena", "Wijesinghe", "De Silva"
]

cities = [
    ("Colombo", "Colombo"),
    ("Kandy", "Kandy"),
    ("Galle", "Galle"),
    ("Negombo", "Gampaha"),
    ("Kurunegala", "Kurunegala"),
    ("Matara", "Matara"),
    ("Jaffna", "Jaffna"),
    ("Ratnapura", "Ratnapura")
]

customers = []

for i in range(1, 101):
    first = random.choice(first_names)
    last = random.choice(last_names)
    city, district = random.choice(cities)

    customers.append({
        "customer_id": f"C{i:03d}",
        "customer_name": f"{first} {last}",
        "gender": random.choice(["Male", "Female"]),
        "date_of_birth": date(
            random.randint(1975, 2004),
            random.randint(1, 12),
            random.randint(1, 28)
        ),
        "city": city,
        "district": district,
        "customer_type": random.choice(
            ["Individual", "Business"]
        ),
        "membership_level": random.choice(
            ["Bronze", "Silver", "Gold"]
        )
    })

customers_df = pd.DataFrame(customers)


# ============================================
# PRODUCTS
# ============================================

categories = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Monitor"],
    "Accessories": ["Mouse", "Keyboard", "Headset", "Webcam"],
    "Home": ["Lamp", "Speaker", "Fan", "Router"],
    "Office": ["Printer", "Chair", "Desk", "Calculator"]
}

brands = [
    "TechPro",
    "Nova",
    "LankaTech",
    "Vision",
    "SmartLine"
]

products = []

product_number = 1

for category, subcategories in categories.items():
    for subcategory in subcategories:
        for j in range(1, 4):
            cost = round(random.uniform(1500, 120000), 2)
            price = round(cost * random.uniform(1.15, 1.60), 2)

            products.append({
                "product_id": f"P{product_number:03d}",
                "product_name": f"{brands[j % len(brands)]} {subcategory} {j}",
                "category": category,
                "subcategory": subcategory,
                "brand": brands[j % len(brands)],
                "unit_cost": cost,
                "unit_price": price
            })

            product_number += 1

products_df = pd.DataFrame(products)


# ============================================
# LOCATIONS
# ============================================

locations = [
    ["L001", "Colombo", "Colombo", "Western", "Sri Lanka"],
    ["L002", "Kandy", "Kandy", "Central", "Sri Lanka"],
    ["L003", "Galle", "Galle", "Southern", "Sri Lanka"],
    ["L004", "Negombo", "Gampaha", "Western", "Sri Lanka"],
    ["L005", "Kurunegala", "Kurunegala", "North Western", "Sri Lanka"],
    ["L006", "Matara", "Matara", "Southern", "Sri Lanka"],
    ["L007", "Jaffna", "Jaffna", "Northern", "Sri Lanka"],
    ["L008", "Ratnapura", "Ratnapura", "Sabaragamuwa", "Sri Lanka"]
]

locations_df = pd.DataFrame(
    locations,
    columns=[
        "location_id",
        "city",
        "district",
        "province",
        "country"
    ]
)


# ============================================
# PAYMENTS
# ============================================

payments = [
    ["PM001", "Credit Card", "Card"],
    ["PM002", "Debit Card", "Card"],
    ["PM003", "Cash on Delivery", "Cash"],
    ["PM004", "Bank Transfer", "Bank"],
    ["PM005", "Digital Wallet", "Digital"]
]

payments_df = pd.DataFrame(
    payments,
    columns=[
        "payment_id",
        "payment_method",
        "payment_type"
    ]
)


# ============================================
# ORDERS
# ============================================

orders = []

start_date = date(2026, 8, 1)

for i in range(1, 701):

    order_line_id = f"OL{i:04d}"
    order_id = f"O{((i - 1) // 2) + 1:04d}"

    order_date = start_date + timedelta(
        days=random.randint(0, 30)
    )

    customer_id = random.choice(
        customers_df["customer_id"].tolist()
    )

    product_id = random.choice(
        products_df["product_id"].tolist()
    )

    location_id = random.choice(
        locations_df["location_id"].tolist()
    )

    payment_id = random.choice(
        payments_df["payment_id"].tolist()
    )

    quantity = random.randint(1, 5)

    discount_amount = round(
        random.choice([0, 0, 0, 250, 500, 750, 1000]),
        2
    )

    orders.append({
        "order_line_id": order_line_id,
        "order_id": order_id,
        "order_date": order_date,
        "customer_id": customer_id,
        "product_id": product_id,
        "location_id": location_id,
        "payment_id": payment_id,
        "quantity": quantity,
        "discount_amount": discount_amount
    })

orders_df = pd.DataFrame(orders)


# ============================================
# SAVE CSV FILES
# ============================================

customers_df.to_csv(
    os.path.join(SOURCE_DIR, "customers.csv"),
    index=False
)

products_df.to_csv(
    os.path.join(SOURCE_DIR, "products.csv"),
    index=False
)

locations_df.to_csv(
    os.path.join(SOURCE_DIR, "locations.csv"),
    index=False
)

payments_df.to_csv(
    os.path.join(SOURCE_DIR, "payments.csv"),
    index=False
)

orders_df.to_csv(
    os.path.join(SOURCE_DIR, "orders.csv"),
    index=False
)


print("========================================")
print("SOURCE DATA GENERATED SUCCESSFULLY")
print("========================================")
print(f"Customers : {len(customers_df)}")
print(f"Products  : {len(products_df)}")
print(f"Locations : {len(locations_df)}")
print(f"Payments  : {len(payments_df)}")
print(f"Order rows: {len(orders_df)}")
print(f"Output    : {SOURCE_DIR}")