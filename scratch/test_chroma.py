import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    load_dotenv("finance-rag/.env")
    
    pdf_path = "finance-rag/data/cdn-dynmedia-1.microsoft.com.pdf"
    print("1. Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    print("2. Chunking text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = text_splitter.split_documents(pages)
    
    print("3. Generating embeddings and saving to ChromaDB...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    # Save to disk
    persist_dir = "finance-rag/chroma_db_test"
    db = Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
    db.persist()
    
    print(f"Success! Stored {len(chunks)} chunks in {persist_dir}")

if __name__ == "__main__":
    main()
