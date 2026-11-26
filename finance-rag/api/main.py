import os
import shutil
from typing import List
import yfinance as yf
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from ingest import ingest_pdfs
from rag import answer_question

load_dotenv()

app = FastAPI(title="Finance RAG API")

class AskRequest(BaseModel):
    question: str
    top_k: int = Field(default=4, ge=1, le=20)

@app.post("/ingest")
async def ingest_route(files: List[UploadFile] = File(...)):
    # Save uploaded files temporarily
    temp_dir = "data"
    os.makedirs(temp_dir, exist_ok=True)
    
    file_paths = []
    for file in files:
        filename = os.path.basename(file.filename or "")
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs are allowed")
            
        file_path = os.path.join(temp_dir, filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            await file.close()
        file_paths.append(file_path)
        
    try:
        result = ingest_pdfs(file_paths)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_route(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")
    try:
        result = answer_question(question, req.top_k)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def stats_route():
    if not os.path.exists("chroma_db"):
        raise HTTPException(status_code=404, detail="DB not initialized yet")
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
        count = db._collection.count()
        return {
            "collection_name": db._collection.name,
            "total_chunks": count,
            "embedding_model": "FastEmbed",
            "llm_model": "gemini-3.7-flash"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read DB stats: {str(e)}")

@app.get("/market/{ticker}")
def market_route(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if hist.empty:
            raise HTTPException(status_code=404, detail="No data found for ticker")
            
        latest_price = hist['Close'].iloc[-1]
        info = stock.info
        cap = info.get("marketCap", "N/A")
        
        return {
            "ticker": ticker.upper(),
            "latest_price_usd": round(latest_price, 2),
            "market_cap": cap
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data error: {str(e)}")
