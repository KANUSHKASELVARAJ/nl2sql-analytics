"""
Generates sample e-commerce data and loads it into MongoDB.
Run: python seed_data.py
"""

import random
from datetime import datetime, timedelta

from mongo_db import db


random.seed(42)

REGIONS = [
    "North America",
    "Europe",
    "Asia",
    "South America",
    "Africa"
]

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Garden",
    "Sports",
    "Books",
    "Toys"
]

FIRST_NAMES = [
    "Alex", "Jordan", "Sam", "Taylor",
    "Morgan", "Casey", "Riley", "Jamie",
    "Priya", "Wei", "Fatima", "Noah"
]

LAST_NAMES = [
    "Smith", "Johnson", "Lee", "Patel",
    "Garcia", "Kim", "Chen", "Nguyen",
    "Brown", "Davis"
]

PRODUCT_ADJ = [
    "Wireless", "Compact", "Premium", "Eco",
    "Smart", "Classic", "Portable", "Ultra"
]

PRODUCT_NOUN = [
    "Headphones", "Blender", "Backpack",
    "Sneakers", "Lamp", "Notebook",
    "Watch", "Speaker", "Jacket", "Bottle"
]


def gen_customers(n=200):
    customers = []

    for i in range(1, n + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

        region = random.choice(REGIONS)

        signup = (
            datetime(2023, 1, 1)
            + timedelta(days=random.randint(0, 700))
        )

        customers.append({
            "customer_id": i,
            "name": name,
            "region": region,
            "signup_date": signup.date().isoformat()
        })

    return customers


def gen_products(n=60):
    products = []

    for i in range(1, n + 1):
        name = (
            f"{random.choice(PRODUCT_ADJ)} "
            f"{random.choice(PRODUCT_NOUN)}"
        )

        category = random.choice(CATEGORIES)

        price = round(random.uniform(8, 300), 2)

        products.append({
            "product_id": i,
            "name": name,
            "category": category,
            "price": price
        })

    return products


def gen_orders_and_items(
    n_customers,
    n_products,
    n_orders=1500
):
    orders = []
    items = []

    item_id = 1

    for order_id in range(1, n_orders + 1):

        customer_id = random.randint(1, n_customers)

        order_date = (
            datetime(2023, 1, 1)
            + timedelta(days=random.randint(0, 760))
        )

        status = random.choices(
            ["completed", "cancelled", "refunded"],
            weights=[0.85, 0.08, 0.07]
        )[0]

        n_items = random.randint(1, 4)

        chosen_products = random.sample(
            range(1, n_products + 1),
            n_items
        )

        for product_id in chosen_products:

            quantity = random.randint(1, 3)

            items.append({
                "item_id": item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity
            })

            item_id += 1

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date.date().isoformat(),
            "status": status
        })

    return orders, items


def main():

    # Clear old collections
    db.customers.delete_many({})
    db.products.delete_many({})
    db.orders.delete_many({})
    db.order_items.delete_many({})

    # Generate data
    customers = gen_customers()

    products = gen_products()

    orders, items = gen_orders_and_items(
        len(customers),
        len(products)
    )

    # Insert into MongoDB
    db.customers.insert_many(customers)

    db.products.insert_many(products)

    db.orders.insert_many(orders)

    db.order_items.insert_many(items)

    print("MongoDB database seeded successfully!")

    print(f"Customers: {len(customers)}")

    print(f"Products: {len(products)}")

    print(f"Orders: {len(orders)}")

    print(f"Order items: {len(items)}")


if __name__ == "__main__":
    main()