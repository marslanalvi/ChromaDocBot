from flask import Flask, render_template, request, jsonify, send_from_directory
from environment import load_environment
from chromadb_setup import initialize_chromadb
from document_processing import load_documents_from_directory, preprocess_documents
from embedding_generation import generate_embeddings
from db_operations import upsert_documents_into_db
from query_and_response import query_documents, generate_response
from openai import OpenAI

# Load environment variables
openai_key = load_environment()

# Initialize OpenAI Client
client = OpenAI(api_key=openai_key)

# Initialize ChromaDB
collection = initialize_chromadb(openai_key)

# Load and preprocess documents
directory_path = "./data"
documents = load_documents_from_directory(directory_path)
chunked_documents = preprocess_documents(documents)

# Generate embeddings
chunked_documents = generate_embeddings(client, chunked_documents)

# Upsert documents into ChromaDB
upsert_documents_into_db(collection, chunked_documents)

# Flask application setup
app = Flask(__name__, template_folder="templates", static_folder="static")


# Route to serve the chatbot UI
@app.route("/")
def index():
    """
    Serve the main chatbot page (index.html).
    """
    return render_template("index.html")


# Route to handle user messages
@app.route("/chat", methods=["POST"])
def chat():
    """
    Process user input, query the document collection, and generate a response.
    """
    user_message = request.json.get("message")  # Extract message from frontend
    try:
        # Query the database for relevant documents
        relevant_chunks = query_documents(collection, [user_message])
        # Generate a response using the OpenAI API
        response = generate_response(client, user_message, relevant_chunks)
        return jsonify({"message": response})  # Send response back to frontend
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
