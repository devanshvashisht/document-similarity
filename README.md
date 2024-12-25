# 📄 Document Similarity Search Tool

This is a Python-based tool that helps you find similar documents based on a query. It uses **ChromaDB** for storing and querying document embeddings and **PostgreSQL** for managing document data. The tool uses a pre-trained embedding model from **Sentence-Transformers** to generate embeddings for the text documents.

## 🚀 Features

- **🔍 Search for similar documents** based on text input.
- **➕ Add new documents** to the database and ChromaDB collection.
- **📥 Load existing documents** from a PostgreSQL database into ChromaDB.
- **⚡ Fast and efficient** text embeddings using the `all-MiniLM-L6-v2` model.
- **🔄 Store document embeddings** in both PostgreSQL and ChromaDB.

## 🧰 Requirements

- Python 3.x
- Libraries:
  - `psycopg2` - PostgreSQL adapter for Python.
  - `chromadb` - A ChromaDB client for document storage and querying.
  - `sentence-transformers` - Sentence embedding models for text-to-vector conversion.

## 📦 Installation

1. **Clone the repository**:
   ```bash
   
   git clone <repository-url>
   cd <repository-name>

2. **Install the required libraries**:
   ```bash
   
   pip install psycopg2 chromadb sentence-transformers

3. **Set up PostgreSQL**:
 - Ensure your PostgreSQL server is running.
 - Create a database named document-similarity and a table documents with columns: doc_id, text, embedding.

   ```bash
   
   CREATE TABLE documents (
    doc_id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    embedding FLOAT8[]
    );

 4. **Run the tool**:
    ```bash
    
    python document_similarity.py

## 🔧 Usage

Once the tool is running, you can interact with it through the following options:

1. **Add a Document 📑**  
   Add a new document to both PostgreSQL and ChromaDB by entering its ID and text.

2. **Search for Similar Documents 🔍**  
   Enter a query, and the tool will return the most similar documents stored in ChromaDB based on the query text.

3. **Exit 🚪**  
   Exit the program.

## 💡 Functions

### `add_document(doc_id, text)`
Adds a document with the given `doc_id` and `text` to both PostgreSQL and ChromaDB. It generates an embedding for the text using the pre-trained model.

### `search_similar(query, collection, model, top_n)`
Searches for the most similar documents in the ChromaDB collection based on a given query and returns the top `n` results.

### `load_documents_from_db()`
Loads all documents from the PostgreSQL database and adds them to ChromaDB.

## 🔒 Security

Ensure that your PostgreSQL credentials (user, password, etc.) are kept secure, and do not expose them in public repositories.

## 📝 License

This tool is open-source and distributed under the MIT license. See LICENSE for more details.
