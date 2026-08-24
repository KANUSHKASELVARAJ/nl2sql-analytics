"""
Stage 1: schema is hardcoded and stuffed directly into the prompt.
In Stage 3 this gets replaced with embedding-based retrieval over
per-table/column descriptions so only relevant tables are included.
"""

SCHEMA_DESCRIPTION = """
Table: customers
  - customer_id (INTEGER, primary key)
  - name (VARCHAR)
  - region (VARCHAR) -- one of: North America, Europe, Asia, South America, Africa
  - signup_date (DATE)

Table: products
  - product_id (INTEGER, primary key)
  - name (VARCHAR)
  - category (VARCHAR) -- one of: Electronics, Clothing, Home & Garden, Sports, Books, Toys
  - price (DECIMAL) -- unit price in USD

Table: orders
  - order_id (INTEGER, primary key)
  - customer_id (INTEGER, foreign key -> customers.customer_id)
  - order_date (DATE)
  - status (VARCHAR) -- one of: completed, cancelled, refunded

Table: order_items
  - item_id (INTEGER, primary key)
  - order_id (INTEGER, foreign key -> orders.order_id)
  - product_id (INTEGER, foreign key -> products.product_id)
  - quantity (INTEGER)

Notes:
  - Revenue for a line item = order_items.quantity * products.price
  - Only include orders with status = 'completed' when computing revenue,
    unless the user explicitly asks about cancelled/refunded orders.
""".strip()
