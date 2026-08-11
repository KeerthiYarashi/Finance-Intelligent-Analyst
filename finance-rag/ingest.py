import os
import shutil
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_PATH = "chroma_db"

def ingest_pdfs(file_paths: List[str]) -> dict:
    # 1. Load PDFs
    documents = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        docs = loader.load()
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
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    # Store with persistent DB
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
