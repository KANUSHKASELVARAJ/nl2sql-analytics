ALLOWED_COLLECTIONS = {
    "customers",
    "products",
    "orders",
    "order_items"
}

ALLOWED_OPERATIONS = {
    "find",
    "count"
}

ALLOWED_OPERATORS = {
    "$gt",
    "$gte",
    "$lt",
    "$lte",
    "$eq",
    "$ne"
}


def validate_query(query):

    # Check collection
    collection = query.get("collection")

    if collection not in ALLOWED_COLLECTIONS:
        raise ValueError(
            f"Invalid collection: {collection}"
        )

    # Check operation
    operation = query.get("operation")

    if operation not in ALLOWED_OPERATIONS:
        raise ValueError(
            f"Invalid operation: {operation}"
        )

    # Check filter
    query_filter = query.get("filter", {})

    if not isinstance(query_filter, dict):
        raise ValueError("Filter must be a dictionary")

    # Check MongoDB operators
    check_operators(query_filter)

    # Check sort
    sort = query.get("sort", {})

    if not isinstance(sort, dict):
        raise ValueError("Sort must be a dictionary")

    for field, direction in sort.items():

        if direction not in [1, -1]:
            raise ValueError(
                "Sort direction must be 1 or -1"
            )

    # Check limit
    limit = query.get("limit", 10)

    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer")

    if limit < 0 or limit > 100:
        raise ValueError(
            "Limit must be between 0 and 100"
        )

    return True


def check_operators(value):

    if isinstance(value, dict):

        for key, val in value.items():

            if key.startswith("$"):

                if key not in ALLOWED_OPERATORS:
                    raise ValueError(
                        f"Operator not allowed: {key}"
                    )

            check_operators(val)

    elif isinstance(value, list):

        for item in value:
            check_operators(item)