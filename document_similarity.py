import psycopg2
import chromadb
from sentence_transformers import SentenceTransformer

documents = []

#initializing chromadb client
client = chromadb.Client()

#creating and a connecting to a collection
collection = client.create_collection(name = "documents")

#Loading a pre trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
# all-MiniLM-L6-v2 is a lightweight embedding model

# connect to PostgreSQL
conn = psycopg2.connect(
    dbname = "document-similarity",
    user="postgres",
    password="Pass123",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


def add_document(doc_id, text):
    # Adding a document to chromadb
    embedding = model.encode(text) #generate embedding
    try:
        embedding_list = embedding.tolist()
        cursor.execute(
            "INSERT INTO documents (doc_id, text, embedding) VALUES (%s, %s, %s)",
            (doc_id, text, embedding_list)
        )
        conn.commit()
             
        # collection.add([doc_id], [text], [embedding])
        collection.add(documents=[text], metadatas=[{"id": doc_id}], ids=[doc_id], embeddings=[embedding])
        print(f"Document {doc_id} added successfully!")    
    except psycopg2.IntegrityError:
        conn.rollback()
        print(f"Document with ID {doc_id} already exists!")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred Devansh: {e}")    
  

def search_similar(query, collection, model, top_n):

    #Search for similar documents 
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results = top_n)
    try:
        # Search in ChromaDB
                
        print(f"Search Results for '{query}':")

        # for i in range(len(results['documents'])):
        #     for k in range(top_n):
        #         doc_id = results['ids'][k][i]
        #         text = results['documents'][k][i]
        #         print(f"Document ID: {doc_id}, Text: {text}\n")
        for i in range(top_n):
            print(results['ids'][0][i], ":", results['documents'][0][i])
    except Exception as e:
        print(f"Error occurred while searching: {e}") 

# Load documents from PostgreSQL to ChromaDB
def load_documents_from_db():
    """Load all documents from PostgreSQL into ChromaDB."""
    cursor.execute("SELECT doc_id, text, embedding FROM documents")
    rows = cursor.fetchall()
    for doc_id, text, embedding in rows:
        if not isinstance(embedding, list):
            raise ValueError(f"Invalid embedding format for doc_id {doc_id}: {embedding}")
        
        # Ensure embeddings are lists of floats
        collection.add(documents=[text], metadatas=[{"id": doc_id}], ids=[doc_id], embeddings=[embedding])

    print("All documents loaded from database into ChromaDB!")
    



if __name__ == "__main__":
    print("=== Document Search Similarity Tool ===")
    load_documents_from_db()
   
   

    while True:
        print("\nOptions: \n1. Add Document \n2. Search \n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            doc_id = input("Enter document ID: ")
            text = input("Enter document text: ")
            add_document(doc_id, text)
        elif choice =="2":
            query = input("Enter your search query: ")
            top_n = int(input("Enter the number of top results: "))
            search_similar(query, collection, model, top_n=top_n)
        elif choice == "3":
            print("Exiting...")
            break
        else:
             print("Invalid choice. Try again.")