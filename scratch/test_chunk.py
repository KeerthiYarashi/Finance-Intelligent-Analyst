import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    pdf_path = "finance-rag/data/cdn-dynmedia-1.microsoft.com.pdf"
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    # Create the text splitter (1200 characters per chunk, 200 character overlap)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(pages)
    
    print(f"Original pages: {len(pages)}")
    print(f"Created {len(chunks)} text chunks.")
    
    print("\n--- Example Chunk 1 ---")
    print(chunks[0].page_content)
    print("Length:", len(chunks[0].page_content))

if __name__ == "__main__":
    main()
