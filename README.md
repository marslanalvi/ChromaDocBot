Chatbot Project with Flask and ChromaDB
This project implements a document-based chatbot capable of answering questions using a combination of:

Flask (as the web framework),
ChromaDB (for document storage and querying),
OpenAI (for embeddings and natural language responses),
and a custom frontend for user interaction.
Overview
The goal of this project is to build a chatbot that processes documents, generates embeddings, stores them in a database (ChromaDB), and retrieves the most relevant context to answer user queries. The project integrates backend functionality with a dynamic frontend for seamless interaction.

Project Features
1. Document Processing
Documents (e.g., text files) are loaded from a directory.
Each document is split into smaller chunks for efficient storage and querying.
Preprocessing ensures all chunks are clean and ready for embeddings.
2. Embedding Generation
Embeddings for each document chunk are generated using OpenAI's embedding model (text-embedding-3-small).
These embeddings represent the semantic meaning of each chunk.
3. Database Storage
ChromaDB is used as the vector database to store document embeddings and metadata.
Each document chunk is stored with its embedding for quick and efficient retrieval.
4. Query and Response
When the user asks a question, the system:
Converts the question into an embedding.
Queries ChromaDB for the most relevant document chunks.
Passes these chunks to OpenAI's GPT model to generate a concise response.
5. Frontend
A responsive and user-friendly chatbot interface is provided.
Users can type their questions and receive AI-powered answers dynamically.

1. Clone the Repository
git clone https://github.com/your-username/ChromaDocBot.git
cd ChromaDocBot

