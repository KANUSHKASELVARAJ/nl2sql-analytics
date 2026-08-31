from mongo_db import db


# 1. Find customers from Asia
print("\n--- Customers from Asia ---")

customers = db.customers.find({
    "region": "Asia"
})

for customer in customers.limit(5):
    print(customer)


# 2. Find products with price greater than 100
print("\n--- Products above 100 ---")

products = db.products.find({
    "price": {
        "$gt": 100
    }
})

for product in products.limit(5):
    print(product)


# 3. Count customers
print("\n--- Total Customers ---")

count = db.customers.count_documents({})

print(count)


# 4. Find Electronics products
print("\n--- Electronics Products ---")

products = db.products.find({
    "category": "Electronics"
})

for product in products.limit(5):
    print(product)


# 5. Most expensive products
print("\n--- Most Expensive Products ---")

products = db.products.find().sort(
    "price",
    -1
)

for product in products.limit(5):
    print(product)