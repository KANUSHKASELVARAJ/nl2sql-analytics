from query_generator import generate_query


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
        result = generate_query(question)

        print("\nGENERATED NOSQL:")

        print(result)

    except Exception as e:

        print("\nERROR:")
        print(e)