from query_generator import generate_query
from query_executor import execute_query


questions = [
    "Find customers from Asia",
    "Find products above 100",
    "How many customers are there?",
    "Show the most expensive products"
]


for question in questions:

    print("\n==============================")

    print("QUESTION:")
    print(question)

    try:

        # NLP → NoSQL
        query = generate_query(question)

        print("\nGENERATED QUERY:")
        print(query)

        # NoSQL → MongoDB
        result = execute_query(query)

        print("\nDATABASE RESULT:")
        print(result)

    except Exception as e:

        print("\nERROR:")
        print(e)