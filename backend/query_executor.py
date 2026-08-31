from mongo_db import db
from query_validator import validate_query


def execute_query(query):

    # Validate before executing
    validate_query(query)

    collection_name = query["collection"]
    operation = query["operation"]

    query_filter = query.get("filter", {})
    sort = query.get("sort", {})
    limit = query.get("limit", 10)

    collection = db[collection_name]

    # COUNT
    if operation == "count":

        result = collection.count_documents(
            query_filter
        )

        return {
            "type": "count",
            "count": result
        }

    # FIND
    if operation == "find":

        cursor = collection.find(
            query_filter,
            {"_id": 0}
        )

        # Apply sorting
        if sort:
            sort_list = list(sort.items())
            cursor = cursor.sort(sort_list)

        # Apply limit
        if limit > 0:
            cursor = cursor.limit(limit)

        results = list(cursor)

        return {
            "type": "data",
            "count": len(results),
            "results": results
        }

    raise ValueError(
        f"Unsupported operation: {operation}"
    )