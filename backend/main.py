from flask import Flask, request, jsonify
from flask_cors import CORS

from query_generator import generate_query
from query_executor import execute_query


app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "NL2NoSQL API is running"
    })


@app.route("/ask", methods=["POST"])
def ask():

    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({
                "error": "Question is required"
            }), 400

        question = data["question"].strip()

        if not question:
            return jsonify({
                "error": "Question cannot be empty"
            }), 400

        # Step 1: Natural Language → NoSQL
        query = generate_query(question)

        # Step 2: NoSQL → MongoDB
        result = execute_query(query)

        return jsonify({
            "question": question,
            "query": query,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )