import os
import shutil
from typing import List
import yfinance as yf
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from ingest import ingest_pdfs
from rag import answer_question

load_dotenv()

app = FastAPI(title="Finance RAG API")

class AskRequest(BaseModel):
    question: str
    top_k: int = 4

@app.post("/ingest")
async def ingest_route(files: List[UploadFile] = File(...)):
    # Save uploaded files temporarily
    temp_dir = "data"
    os.makedirs(temp_dir, exist_ok=True)
    
    file_paths = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs are allowed")
            
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)
        
    try:
        result = ingest_pdfs(file_paths)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_route(req: AskRequest):
    try:
        result = answer_question(req.question, req.top_k)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def stats_route():
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
        count = db._collection.count()
        return {
            "collection_name": db._collection.name,
            "total_chunks": count,
            "embedding_model": "gemini-embedding-2",
            "llm_model": "gemini-2.5-flash"
        }
    except Exception as e:
        return {"error": "DB not initialized yet"}

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data error: {str(e)}")
