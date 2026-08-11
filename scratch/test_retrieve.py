import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    load_dotenv("finance-rag/.env")
    
    persist_dir = "finance-rag/chroma_db_test"
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    print("Loading persistent ChromaDB...")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    
    question = "What was the total revenue?"
    print(f"Searching for: '{question}'\n")
    
    # Retrieve top 4 chunks
    results = db.similarity_search_with_score(question, k=4)
    
    for i, (doc, score) in enumerate(results):
        print(f"--- Result {i+1} (Score: {score:.4f}) ---")
        print(f"Source: {doc.metadata.get('source')} | Page: {doc.metadata.get('page', -1) + 1}")
        print(f"Content: {doc.page_content[:200]}...\n")

if __name__ == "__main__":
    main()
