"""
Generates a small sample e-commerce dataset and loads it into a DuckDB file.
Run this once before starting the API: `python seed_data.py`
"""
import duckdb
import random
from datetime import datetime, timedelta

DB_PATH = "analytics.duckdb"

random.seed(42)

REGIONS = ["North America", "Europe", "Asia", "South America", "Africa"]
CATEGORIES = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
FIRST_NAMES = ["Alex", "Jordan", "Sam", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Priya", "Wei", "Fatima", "Noah"]
LAST_NAMES = ["Smith", "Johnson", "Lee", "Patel", "Garcia", "Kim", "Chen", "Nguyen", "Brown", "Davis"]
PRODUCT_ADJ = ["Wireless", "Compact", "Premium", "Eco", "Smart", "Classic", "Portable", "Ultra"]
PRODUCT_NOUN = ["Headphones", "Blender", "Backpack", "Sneakers", "Lamp", "Notebook", "Watch", "Speaker", "Jacket", "Bottle"]


def gen_customers(n=200):
    rows = []
    for i in range(1, n + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        region = random.choice(REGIONS)
        signup = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
        rows.append((i, name, region, signup.date().isoformat()))
    return rows


def gen_products(n=60):
    rows = []
    for i in range(1, n + 1):
        name = f"{random.choice(PRODUCT_ADJ)} {random.choice(PRODUCT_NOUN)}"
        category = random.choice(CATEGORIES)
        price = round(random.uniform(8, 300), 2)
        rows.append((i, name, category, price))
    return rows


def gen_orders_and_items(n_customers, n_products, n_orders=1500):
    orders = []
    items = []
    item_id = 1
    for order_id in range(1, n_orders + 1):
        customer_id = random.randint(1, n_customers)
        order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 760))
        status = random.choices(
            ["completed", "cancelled", "refunded"], weights=[0.85, 0.08, 0.07]
        )[0]
        n_items = random.randint(1, 4)
        order_total = 0.0
        chosen_products = random.sample(range(1, n_products + 1), n_items)
        for product_id in chosen_products:
            qty = random.randint(1, 3)
            items.append((item_id, order_id, product_id, qty))
            item_id += 1
        orders.append((order_id, customer_id, order_date.date().isoformat(), status))
    return orders, items


def main():
    con = duckdb.connect(DB_PATH)

    con.execute("DROP TABLE IF EXISTS order_items")
    con.execute("DROP TABLE IF EXISTS orders")
    con.execute("DROP TABLE IF EXISTS products")
    con.execute("DROP TABLE IF EXISTS customers")

    con.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR,
            region VARCHAR,
            signup_date DATE
        )
    """)
    con.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR,
            category VARCHAR,
            price DECIMAL(10,2)
        )
    """)
    con.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            status VARCHAR
        )
    """)
    con.execute("""
        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER
        )
    """)

    customers = gen_customers()
    products = gen_products()
    orders, items = gen_orders_and_items(len(customers), len(products))

    con.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)
    con.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
    con.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    con.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", items)

    print(f"Seeded {len(customers)} customers, {len(products)} products, "
          f"{len(orders)} orders, {len(items)} order_items into {DB_PATH}")
    con.close()


if __name__ == "__main__":
    main()
