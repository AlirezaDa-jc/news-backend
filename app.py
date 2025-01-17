from flask import Flask, request, jsonify
import weaviate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

client = weaviate.connect_to_local()

@app.route('/query', methods=['POST'])
def query_weaviate():
    data = request.json.get('input', {})
    user_query = data.get('query')
    limit = int(data.get('limit', 15))

    questions = client.collections.get("News_db")
    try:
        response = questions.query.near_text(
            query=user_query,
            limit=limit
        )
        return jsonify(response.objects)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/prompt', methods=['POST'])
def prompt_weaviate():
    data = request.json.get('input', {})
    user_query = data.get('prompt')
    limit = int(data.get('limit', 15))
    try:
        # Access the collection
        collection = client.collections.get("News_db")

        # Generate response using near_text
        response = collection.generate.near_text(
            query=user_query,  # Vectorize the query automatically
            grouped_task=" Return your response as HTML and dont include tags like html . SCHEMA: html typography tags like <h1-6> <p> <span> etc \n" + user_query,
            limit=limit,
        )

        return jsonify({"response": response.generated})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
