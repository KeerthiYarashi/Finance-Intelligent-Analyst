import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def main():
    load_dotenv("finance-rag/.env")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    text = "Microsoft reported strong growth in cloud revenue this quarter."
    print("Generating embeddings via Gemini API...")
    
    vector = embeddings.embed_query(text)
    
    print(f"Success! Vector length: {len(vector)}")
    print(f"First 5 dimensions: {vector[:5]}")

if __name__ == "__main__":
    main()
