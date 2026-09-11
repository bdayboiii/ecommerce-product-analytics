import psycopg2
import random
import string
import os
from datetime import datetime, timedelta, date

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------

DB_NAME = "ecommerce_analytics"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5433"

# Reproducible synthetic dataset
random.seed(42)


# -----------------------------
# CONNECT TO DATABASE
# -----------------------------

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()


# -----------------------------
# CLEAR OLD GENERATED DATA
# -----------------------------

print("Clearing old generated data...")

cur.execute("DELETE FROM orders;")
cur.execute("DELETE FROM events;")

# Keep the original 3 manually created users/products
cur.execute("DELETE FROM products WHERE product_id > 3;")
cur.execute("DELETE FROM users WHERE user_id > 3;")

conn.commit()


# -----------------------------
# GENERATE USERS
# -----------------------------

print("Generating users...")

cities = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Pune", "Kolkata", "Ahmedabad"
]

genders = ["Male", "Female", "Other"]

user_rows = []

for user_id in range(4, 1004):

    age = random.randint(18, 55)
    gender = random.choice(genders)
    city = random.choice(cities)

    # Signup dates from Jan-Jun 2026
    signup_date = date(2026, 1, 1) + timedelta(
        days=random.randint(0, 180)
    )

    user_rows.append(
        (
            user_id,
            age,
            gender,
            city,
            signup_date
        )
    )

cur.executemany(
    """
    INSERT INTO users
    (user_id, age, gender, city, signup_date)
    VALUES (%s, %s, %s, %s, %s)
    """,
    user_rows
)

conn.commit()


# -----------------------------
# GENERATE PRODUCTS
# -----------------------------

print("Generating products...")

categories = [
    "Clothing",
    "Footwear",
    "Accessories",
    "Sports",
    "Beauty"
]

brands = [
    "Nike",
    "Adidas",
    "Puma",
    "Levis",
    "H&M",
    "Zara",
    "Mango",
    "Fossil"
]

product_rows = []

for product_id in range(4, 204):

    category = random.choice(categories)
    brand = random.choice(brands)

    price = random.choice([
        random.randint(500, 1999),
        random.randint(2000, 3999),
        random.randint(4000, 10000)
    ])

    product_name = f"{brand} {category} Product {product_id}"

    product_rows.append(
        (
            product_id,
            product_name,
            category,
            brand,
            price
        )
    )

cur.executemany(
    """
    INSERT INTO products
    (product_id, product_name, category, brand, price)
    VALUES (%s, %s, %s, %s, %s)
    """,
    product_rows
)

conn.commit()


# -----------------------------
# LOAD USERS & PRODUCTS
# -----------------------------

cur.execute("""
    SELECT user_id, signup_date
    FROM users
""")

users = cur.fetchall()

cur.execute("""
    SELECT product_id, price
    FROM products
""")

products = cur.fetchall()


# -----------------------------
# GENERATE SESSIONS & EVENTS
# -----------------------------

print("Generating sessions and events...")

event_rows = []
order_rows = []

event_id = 1
order_id = 1

event_types = [
    "view",
    "add_to_cart",
    "checkout",
    "purchase"
]

# Generate 10,000 sessions
for session_number in range(10000):

    user_id, signup_date = random.choice(users)
    product_id, price = random.choice(products)

    # --------------------------------
    # SESSION TIMESTAMP
    # --------------------------------

    # Ensure session happens AFTER signup
    session_base = datetime.combine(
        max(signup_date, date(2026, 6, 1)),
        datetime.min.time()
    )

    session_start = (
        session_base
        + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
    )

    session_id = (
        f"session_{session_number + 1}_"
        + "".join(
            random.choices(
                string.ascii_lowercase + string.digits,
                k=6
            )
        )
    )

    # --------------------------------
    # USER TYPE
    # --------------------------------

    days_since_signup = (
        session_start.date() - signup_date
    ).days

    is_new_user = days_since_signup <= 30

    # --------------------------------
    # PRICE SEGMENT
    # --------------------------------

    is_high_price = price >= 4000

    # --------------------------------
    # EXPERIMENT ASSIGNMENT
    # --------------------------------

    experiment_group = None

    if is_new_user and is_high_price:

        experiment_group = random.choice(
            ["control", "treatment"]
        )

    # --------------------------------
    # VIEW EVENT
    # --------------------------------

    event_rows.append(
        (
            event_id,
            user_id,
            product_id,
            session_id,
            "view",
            session_start,
            experiment_group
        )
    )

    event_id += 1

    # --------------------------------
    # BASE ADD-TO-CART PROBABILITY
    # --------------------------------

    add_probability = 0.75

    # New users have lower confidence
    if is_new_user:
        add_probability -= 0.30

    # Higher-priced products have lower conversion
    if is_high_price:
        add_probability -= 0.05

    # --------------------------------
    # TREATMENT EFFECT
    # --------------------------------

    if experiment_group == "treatment":

        # Synthetic assumption:
        # treatment increases ATC probability
        # by 20% relative
        add_probability *= 1.20

    # --------------------------------
    # ADD TO CART
    # --------------------------------

    if random.random() < add_probability:

        cart_time = session_start + timedelta(
            seconds=random.randint(10, 120)
        )

        event_rows.append(
            (
                event_id,
                user_id,
                product_id,
                session_id,
                "add_to_cart",
                cart_time,
                experiment_group
            )
        )

        event_id += 1

        # --------------------------------
        # CHECKOUT PROBABILITY
        # --------------------------------

        checkout_probability = 0.85

        if is_new_user:
            checkout_probability -= 0.10

        if random.random() < checkout_probability:

            checkout_time = cart_time + timedelta(
                seconds=random.randint(30, 180)
            )

            event_rows.append(
                (
                    event_id,
                    user_id,
                    product_id,
                    session_id,
                    "checkout",
                    checkout_time,
                    experiment_group
                )
            )

            event_id += 1

            # --------------------------------
            # PURCHASE PROBABILITY
            # --------------------------------

            purchase_probability = 0.85

            if is_new_user:
                purchase_probability -= 0.15

            if is_high_price:
                purchase_probability -= 0.10

            if random.random() < purchase_probability:

                purchase_time = checkout_time + timedelta(
                    seconds=random.randint(30, 180)
                )

                event_rows.append(
                    (
                        event_id,
                        user_id,
                        product_id,
                        session_id,
                        "purchase",
                        purchase_time,
                        experiment_group
                    )
                )

                event_id += 1

                # --------------------------------
                # CREATE ORDER
                # --------------------------------

                quantity = 1
                amount = price * quantity

                order_rows.append(
                    (
                        order_id,
                        user_id,
                        product_id,
                        purchase_time.date(),
                        quantity,
                        amount
                    )
                )

                order_id += 1


# -----------------------------
# INSERT EVENTS
# -----------------------------

print("Inserting events...")

cur.executemany(
    """
    INSERT INTO events
    (
        event_id,
        user_id,
        product_id,
        session_id,
        event_type,
        event_timestamp,
        experiment_group
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    event_rows
)


# -----------------------------
# INSERT ORDERS
# -----------------------------

print("Inserting orders...")

cur.executemany(
    """
    INSERT INTO orders
    (
        order_id,
        user_id,
        product_id,
        order_date,
        quantity,
        amount
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    order_rows
)

conn.commit()


# -----------------------------
# SUMMARY
# -----------------------------

print("\nData generation complete!")

print(f"Users generated: {len(user_rows)}")
print(f"Products generated: {len(product_rows)}")
print(f"Sessions generated: 10,000")
print(f"Events generated: {len(event_rows)}")
print(f"Orders generated: {len(order_rows)}")


# -----------------------------
# CLOSE CONNECTION
# -----------------------------

cur.close()
conn.close()