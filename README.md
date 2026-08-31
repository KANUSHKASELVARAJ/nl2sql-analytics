# NL2NoSQL — Natural Language to MongoDB Query System

## 📌 Overview

**NL2NoSQL** is an AI-powered web application that allows users to query a MongoDB database using **natural language instead of writing database queries manually**.

The system takes an English question such as:

> "Find products above 100"

and uses **Google Gemini** to convert it into a structured MongoDB query.

The generated query is then validated for safety and executed against MongoDB. The results are displayed through a simple web interface.

### Example

```text
User:
Find products above 100

        ↓

Google Gemini

        ↓

MongoDB Query:
{
    "collection": "products",
    "operation": "find",
    "filter": {
        "price": {
            "$gt": 100
        }
    }
}

        ↓

Query Validator

        ↓

MongoDB

        ↓

Actual Product Results
```

---

## 🎯 Objectives

* Allow users to interact with database data using natural language.
* Convert natural language questions into MongoDB queries using AI.
* Validate generated queries before database execution.
* Prevent unsafe database operations.
* Execute read-only queries on MongoDB.
* Display database results in a user-friendly web interface.

---

## ✨ Features

### 1. Natural Language Querying

Users can enter questions in plain English instead of writing MongoDB syntax.

Examples:

```text
Find customers from Asia

Find products above 100

How many customers are there?

Show the most expensive products

Find completed orders

Find products below 50
```

### 2. AI-Powered Query Generation

Google Gemini converts the user's natural-language question into a structured MongoDB query.

The generated structure contains:

```json
{
    "collection": "products",
    "operation": "find",
    "filter": {},
    "sort": {},
    "limit": 10,
    "explanation": "..."
}
```

### 3. Query Validation

Every AI-generated query is validated before being executed.

The system checks:

* Allowed collections
* Allowed operations
* Allowed MongoDB operators
* Sort direction
* Result limit
* Query structure

### 4. Read-Only Database Access

The application currently supports only safe read operations:

```text
find
count
```

Operations such as:

```text
delete
update
insert
drop
```

are rejected.

### 5. MongoDB Execution

Validated queries are executed directly against MongoDB using PyMongo.

### 6. Web Interface

The frontend provides:

* Natural-language search box
* Example queries
* Generated MongoDB query display
* Database result display
* Error messages
* Loading state

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      FRONTEND       │
                    │  HTML/CSS/JavaScript│
                    └──────────┬──────────┘
                               │
                               │ POST /ask
                               ↓
                    ┌─────────────────────┐
                    │     FLASK API       │
                    │      main.py        │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │    QUERY GENERATOR  │
                    │   Google Gemini AI  │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │   QUERY VALIDATOR   │
                    │ query_validator.py  │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │   QUERY EXECUTOR    │
                    │ query_executor.py   │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │      MONGODB        │
                    │    Database        │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │   RESULTS DISPLAY   │
                    │      Frontend       │
                    └─────────────────────┘
```

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS
* PyMongo

### AI

* Google Gemini API
* `google-genai` Python SDK

### Database

* MongoDB

### Environment Configuration

* Python `python-dotenv`

---

## 📂 Project Structure

```text
nl2sql/
│
├── backend/
│   │
│   ├── main.py
│   ├── mongo_db.py
│   ├── seed_data.py
│   ├── schema.py
│   ├── query_generator.py
│   ├── query_validator.py
│   ├── query_executor.py
│   │
│   ├── test_nlp.py
│   ├── test_validator.py
│   ├── test_executor.py
│   │
│   └── .env
│
└── frontend/
    │
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 🗄️ Database Schema

The project currently uses an e-commerce dataset containing four collections.

### Customers

```text
customers

customer_id
name
region
signup_date
```

### Products

```text
products

product_id
name
category
price
```

### Orders

```text
orders

order_id
customer_id
order_date
status
```

### Order Items

```text
order_items

item_id
order_id
product_id
quantity
```

---

## 📊 Sample Dataset

The project includes generated sample e-commerce data.

The seed script creates approximately:

```text
200 customers
60 products
1500 orders
Multiple order items
```

The data includes regions such as:

```text
North America
Europe
Asia
South America
Africa
```

and product categories such as:

```text
Electronics
Clothing
Home & Garden
Sports
Books
Toys
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

```bash
cd nl2sql
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install pymongo python-dotenv
pip install google-genai
pip install flask flask-cors
```

---

## 🔐 Environment Variables

Create a `.env` file inside the `backend` directory.

```env
MONGO_URI=your_mongodb_connection_string
MONGO_DB=nl_nosql
GEMINI_API_KEY=your_gemini_api_key
```

### Important

Never upload `.env` to GitHub.

Add it to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

## ▶️ Running the Project

### Start the backend

Navigate to:

```text
backend/
```

Run:

```bash
python main.py
```

The Flask server runs at:

```text
http://127.0.0.1:5000
```

### Start the frontend

Open:

```text
frontend/index.html
```

using VS Code Live Server.

The frontend can then communicate with the Flask API.

---

## 🔌 API

### POST `/ask`

The main API endpoint accepts a natural-language question.

### Request

```json
{
    "question": "Find products above 100"
}
```

### Processing

```text
Natural Language
       ↓
Gemini
       ↓
MongoDB Query
       ↓
Validator
       ↓
MongoDB
```

### Response

The API returns:

```json
{
    "question": "Find products above 100",
    "query": {
        "collection": "products",
        "operation": "find",
        "filter": {
            "price": {
                "$gt": 100
            }
        }
    },
    "result": {
        "type": "data",
        "count": 10,
        "results": []
    }
}
```

---

## 🧪 Testing

The project contains separate tests for the major components.

### Test Natural Language → NoSQL

```bash
python test_nlp.py
```

### Test Query Validation

```bash
python test_validator.py
```

The validator should allow:

```text
find
count
```

and reject unsafe operations such as:

```text
delete
update
insert
drop
```

### Test MongoDB Execution

```bash
python test_executor.py
```

This verifies the complete:

```text
Natural Language
      ↓
Gemini
      ↓
NoSQL
      ↓
Validator
      ↓
MongoDB
      ↓
Results
```

pipeline.

---

## 💡 Example Queries

The application can handle queries such as:

```text
Find customers from Asia
```

```text
Find products above 100
```

```text
Find products below 50
```

```text
How many customers are there?
```

```text
Show the most expensive products
```

```text
Show the cheapest products
```

```text
Find completed orders
```

---

## 🔒 Security

Security is an important part of the system because an AI model is generating database queries.

The application therefore:

* Restricts accessible collections.
* Restricts database operations.
* Allows only predefined MongoDB operators.
* Validates generated queries before execution.
* Restricts result limits.
* Blocks unsupported operations.
* Uses environment variables for API credentials.

The system is currently designed around **read-only database access**.

---

## 🚧 Current Limitations

The current version focuses on basic e-commerce queries.

Complex operations such as:

* Advanced aggregation pipelines
* Multi-collection joins/lookups
* Complex analytics
* Natural-language date calculations
* Authentication and user management

can be added in future versions.

---

## 🔮 Future Enhancements

Possible improvements include:

### Advanced Natural Language Support

Support more complex questions such as:

```text
Show the top 5 products in Electronics

Which region has the most customers?

Show completed orders from Asia

What is the average product price?
```

### Query History

Store and display previous user queries.

### Dashboard

Add charts for:

* Sales
* Products
* Customers
* Orders
* Regional distribution

### Authentication

Add user login and access control.

### Advanced MongoDB Aggregation

Support:

```text
$group
$match
$sort
$limit
$lookup
$project
```

with strict validation.

### Deployment

Deploy the application using a cloud hosting platform and connect it to a cloud MongoDB database.

---

## 🎓 Project Learning Outcomes

This project demonstrates practical knowledge of:

* Natural Language Processing
* Generative AI
* Prompt Engineering
* MongoDB
* NoSQL query generation
* REST APIs
* Flask
* Python
* Frontend development
* API integration
* Query validation
* Database security
* Full-stack application development

---

## 👩‍💻 Author

**Kanushka S**

B.Tech Information Technology
Easwari Engineering College

---

## ⭐ Project Summary

**NL2NoSQL converts natural-language questions into safe MongoDB queries using Generative AI and executes them against an e-commerce database through a Flask-based REST API.**

The project demonstrates how AI can make database interaction more accessible by allowing users to communicate with structured data using ordinary language.
