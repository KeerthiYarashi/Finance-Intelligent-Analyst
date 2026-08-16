import os
from typing import List, Dict
from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
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
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError("ChromaDB not found. Please index documents first.")
        
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Retrieve top chunks using FlashRank reranker
    from langchain_classic.retrievers import ContextualCompressionRetriever
    from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
    
    compressor = FlashrankRerank(top_n=top_k)
    base_retriever = db.as_retriever(search_kwargs={"k": 20})
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )
    
    docs = compression_retriever.invoke(question)
    
    if not docs:
        return {
            "answer": "The information is not available in the uploaded documents.",
            "sources": []
        }
        
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)
    
    # Use Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=0)
    response = llm.invoke(prompt)
    
    # Extract sources
    sources = []
    for doc in docs:
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
            
    answer_text = response.content
    if isinstance(answer_text, list):
        answer_text = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block) 
            for block in answer_text
        )

    return {
        "answer": answer_text,
        "sources": unique_sources
    }
