import os
from typing import List, Dict
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

CHROMA_PATH = "chroma_db"

PROMPT_TEMPLATE = """
Answer only from the context provided below. If the context does not contain the answer, reply that the information is not available in the uploaded documents. Do not guess or invent information.

Context:
{context}

Question:
{question}
"""

def answer_question(question: str, top_k: int = 4) -> dict:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError("ChromaDB not found. Please index documents first.")
        
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Retrieve top chunks
    results = db.similarity_search_with_score(question, k=top_k)
    
    if not results:
        return {
            "answer": "The information is not available in the uploaded documents.",
            "sources": []
        }
        
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)
    
    # Use Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    response = llm.invoke(prompt)
    
    # Extract sources
    sources = []
    for doc, _ in results:
        source_name = os.path.basename(doc.metadata.get("source", "unknown"))
        page = doc.metadata.get("page", -1)
        sources.append({"file": source_name, "page": page + 1}) # PyPDFLoader pages are 0-indexed
        
    # Deduplicate sources
    unique_sources = []
    seen = set()
    for s in sources:
        key = f"{s['file']}_{s['page']}"
        if key not in seen:
            unique_sources.append(s)
            seen.add(key)
            
    return {
        "answer": response.content,
        "sources": unique_sources
    }
