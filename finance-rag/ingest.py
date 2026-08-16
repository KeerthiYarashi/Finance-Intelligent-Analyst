import os
import shutil
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_PATH = "chroma_db"

def ingest_pdfs(file_paths: List[str]) -> dict:
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    # Check if these files are already in ChromaDB to prevent duplicates
    existing_files = set()
    if os.path.exists(CHROMA_PATH):
        try:
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
            meta = db.get(include=['metadatas'])['metadatas']
            for m in meta:
                if m and 'source' in m:
                    existing_files.add(os.path.basename(m['source']))
                    
            # If all uploaded files already exist in the database, stop and return
            all_exist = all(os.path.basename(p) in existing_files for p in file_paths)
            if existing_files and all_exist:
                return {
                    "files": len(file_paths),
                    "chunks": len(db.get()['ids']),
                    "already_chunked": True
                }
        except Exception:
            pass

    # 1. Load PDFs and Extract Metadata
    import re
    documents = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        docs = loader.load()
        for doc in docs:
            # Example filename: PressReleaseFY26Q4.pdf
            filename = os.path.basename(doc.metadata.get("source", ""))
            match = re.search(r'FY(\d+)(Q\d)', filename)
            if match:
                doc.metadata["year"] = int("20" + match.group(1))
                doc.metadata["quarter"] = match.group(2)
            else:
                doc.metadata["year"] = 2026
                doc.metadata["quarter"] = "Q4" # Fallback
                
        documents.extend(docs)
    
    if not documents:
        raise ValueError("No text found in PDFs. Are they scanned images?")

    # 2. Split into chunks (1200 char, 200 overlap)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Embed and store in ChromaDB
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    # Store with persistent DB locally using GPU/CPU
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=CHROMA_PATH
    )
    db.persist()
    
    return {
        "files": len(file_paths),
        "chunks": len(chunks)
    }
