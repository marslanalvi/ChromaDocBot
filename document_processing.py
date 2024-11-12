import os

def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(
                os.path.join(directory_path, filename), "r", encoding="utf-8"
            ) as file:
                documents.append({"id": filename, "text": file.read()})
    return documents

def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

def preprocess_documents(documents, chunk_size=1000, chunk_overlap=20):
    chunked_documents = []
    for doc in documents:
        chunks = split_text(doc["text"], chunk_size, chunk_overlap)
        print("==== Splitting docs into chunks ====")
        for i, chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}", "text": chunk})
    return chunked_documents
