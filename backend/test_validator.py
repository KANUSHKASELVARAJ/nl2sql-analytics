from query_validator import validate_query


# Valid query
query1 = {
    "collection": "products",
    "operation": "find",
    "filter": {
        "price": {
            "$gt": 100
        }
    },
    "sort": {},
    "limit": 10
}


# Invalid query
query2 = {
    "collection": "products",
    "operation": "delete",
    "filter": {},
    "sort": {},
    "limit": 10
}


print("Testing valid query...")

try:
    validate_query(query1)
    print("VALID QUERY PASSED")
except Exception as e:
    print("ERROR:", e)


print("\nTesting invalid query...")

try:
    validate_query(query2)
    print("ERROR: Invalid query was accepted")
except Exception as e:
    print("INVALID QUERY BLOCKED")
    print(e)