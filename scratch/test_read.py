import os
from langchain_community.document_loaders import PyPDFLoader

def main():
    # Target one of the PDFs you downloaded
    pdf_path = "finance-rag/data/cdn-dynmedia-1.microsoft.com.pdf"
    
    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    print(f"Success! Loaded {len(pages)} pages.")
    
    # Print the first 200 characters of page 1 to verify it's reading text
    print("\n--- Snippet from Page 1 ---")
    print(pages[0].page_content[:200])
    print("---------------------------\n")

if __name__ == "__main__":
    main()
