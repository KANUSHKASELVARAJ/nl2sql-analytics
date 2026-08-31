SCHEMA = """
customers:
    customer_id: integer
    name: string
    region: string
    signup_date: string

products:
    product_id: integer
    name: string
    category: string
    price: number

orders:
    order_id: integer
    customer_id: integer
    order_date: string
    status: string

order_items:
    item_id: integer
    order_id: integer
    product_id: integer
    quantity: integer
"""