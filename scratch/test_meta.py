import os
from langchain_community.document_loaders import PyPDFLoader

def main():
    pdf_path = "finance-rag/data/cdn-dynmedia-1.microsoft.com.pdf"
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    print("--- Metadata Check ---")
    # Langchain PyPDFLoader automatically adds 'source' and 'page' metadata
    for i in range(min(3, len(pages))):
        print(f"Page {i+1} Metadata: {pages[i].metadata}")

if __name__ == "__main__":
    main()
