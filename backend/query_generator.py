import os
import json
import re

from dotenv import load_dotenv
from google import genai

from schema import SCHEMA


# Load .env
load_dotenv()

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


SYSTEM_PROMPT = f"""
You are a Natural Language to MongoDB query generator.

Your job is to convert an English question into a SAFE MongoDB query.

DATABASE SCHEMA:

{SCHEMA}


Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "collection": "collection_name",
    "operation": "find",
    "filter": {{}},
    "sort": {{}},
    "limit": 10,
    "explanation": "short explanation"
}}


ALLOWED COLLECTIONS:

customers
products
orders
order_items


ALLOWED OPERATIONS:

find
count


ALLOWED OPERATORS:

$gt
$gte
$lt
$lte
$eq
$ne


SORT:

1 = ascending
-1 = descending


EXAMPLE 1

Question:
Find customers from Asia

Output:
{{
    "collection": "customers",
    "operation": "find",
    "filter": {{
        "region": "Asia"
    }},
    "sort": {{}},
    "limit": 10,
    "explanation": "Finds customers whose region is Asia."
}}


EXAMPLE 2

Question:
Find products above 100

Output:
{{
    "collection": "products",
    "operation": "find",
    "filter": {{
        "price": {{
            "$gt": 100
        }}
    }},
    "sort": {{}},
    "limit": 10,
    "explanation": "Finds products with price greater than 100."
}}


EXAMPLE 3

Question:
Find products below 50

Output:
{{
    "collection": "products",
    "operation": "find",
    "filter": {{
        "price": {{
            "$lt": 50
        }}
    }},
    "sort": {{}},
    "limit": 10,
    "explanation": "Finds products with price less than 50."
}}


EXAMPLE 4

Question:
How many customers are there?

Output:
{{
    "collection": "customers",
    "operation": "count",
    "filter": {{}},
    "sort": {{}},
    "limit": 0,
    "explanation": "Counts the total number of customers."
}}


EXAMPLE 5

Question:
Show the most expensive products

Output:
{{
    "collection": "products",
    "operation": "find",
    "filter": {{}},
    "sort": {{
        "price": -1
    }},
    "limit": 10,
    "explanation": "Shows products sorted by price from highest to lowest."
}}


EXAMPLE 6

Question:
Show the cheapest products

Output:
{{
    "collection": "products",
    "operation": "find",
    "filter": {{}},
    "sort": {{
        "price": 1
    }},
    "limit": 10,
    "explanation": "Shows products sorted by price from lowest to highest."
}}


EXAMPLE 7

Question:
Find completed orders

Output:
{{
    "collection": "orders",
    "operation": "find",
    "filter": {{
        "status": "completed"
    }},
    "sort": {{}},
    "limit": 10,
    "explanation": "Finds orders whose status is completed."
}}


IMPORTANT SECURITY RULES:

Never generate SQL.

Never generate delete operations.

Never generate update operations.

Never generate insert operations.

Never generate drop operations.

Never generate raw JavaScript.

Only generate the allowed collections and operations.

Return JSON only.
"""


def generate_query(question):

    """
    Convert natural language question
    into a structured MongoDB query.
    """

    prompt = SYSTEM_PROMPT + f"""

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned invalid JSON:\n" + text
        )

    return result