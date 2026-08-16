import streamlit as st
import requests
import os

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Finance RAG Analyst", layout="wide", page_icon="📊")

# --- PREMIUM CSS INJECTION ---
st.markdown("""
<style>
    /* Global Font & Background Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Button Hover Effects */
    div[data-testid="stButton"] button {
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3);
        border-color: #00f2fe;
        color: #00f2fe !important;
    }
    
    /* Primary Button specific */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        border: none;
        color: white !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        box-shadow: 0 5px 20px rgba(0, 242, 254, 0.6);
    }
    
    /* Input Boxes */
    div[data-baseweb="input"] {
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #00f2fe !important;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.2) !important;
    }
    
    /* Info Box Styling */
    div[data-testid="stInfo"] {
        background-color: rgba(79, 172, 254, 0.1);
        border-left: 4px solid #4facfe;
        border-radius: 0 8px 8px 0;
    }
    div[data-testid="stInfo"] * {
        color: #ffffff !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("Finance RAG – Intelligent Analyst Engine")

# Sidebar for Ingestion
with st.sidebar:
    st.header("1. Document Ingestion")
    uploaded_files = st.file_uploader("Upload Quarterly PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("Index Documents"):
        if not uploaded_files:
            st.error("Please upload at least one PDF.")
        else:
            with st.spinner("Indexing..."):
                # Send files to FastAPI
                files_payload = []
                for f in uploaded_files:
                    files_payload.append(("files", (f.name, f.getvalue(), "application/pdf")))
                
                try:
                    res = requests.post(f"{API_URL}/ingest", files=files_payload)
                    if res.status_code == 200:
                        data = res.json()
                        if data.get("already_chunked"):
                            st.info(f"✅ These {data['files']} documents are already indexed and chunked in the database!")
                        else:
                            st.success(f"Successfully processed {data['files']} files and stored {data['chunks']} chunks.")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {str(e)}. Make sure FastAPI is running.")
                    
    st.divider()
    st.header("Database Stats")
    if st.button("Refresh Stats"):
        try:
            res = requests.get(f"{API_URL}/stats")
            if res.status_code == 200:
                stats = res.json()
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"**📦 Total Chunks:** `{stats['total_chunks']}`")
                st.markdown(f"**📁 Collection:** `{stats['collection_name']}`")
                st.markdown(f"**🧠 LLM:** `{stats['llm_model']}`")
                st.markdown(f"**🔍 Embed:** `{stats['embedding_model']}`")
        except Exception:
            st.error("API offline")

st.header("2. Document Question Answering & Market Data")
st.info("Ask questions about the uploaded financial PDFs, and optionally pull live stock prices.")

if "q_input" not in st.session_state:
    st.session_state["q_input"] = ""
if "t_input" not in st.session_state:
    st.session_state["t_input"] = ""

def clear_text():
    st.session_state["q_input"] = ""
    st.session_state["t_input"] = ""

colA, colB = st.columns([3, 1])
with colA:
    question = st.text_input("Enter your question:", key="q_input")
with colB:
    ticker_options = ["", "MSFT", "AAPL", "NVDA", "TSLA", "GOOGL", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "^GSPC"]
    ticker = st.selectbox("Market Data Ticker:", options=ticker_options, key="t_input", help="Select a stock ticker to pull live Yahoo Finance data alongside your answer.")
    
col1, col2, _ = st.columns([2, 2, 6])
with col1:
    ask_btn = st.button("Ask Document", type="primary", use_container_width=True)
with col2:
    st.button("Clear Fields", on_click=clear_text, use_container_width=True)
    
st.write("---")

if ask_btn:
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing documents & fetching market data..."):
            try:
                # Fetch RAG Answer
                res_rag = requests.post(f"{API_URL}/ask", json={"question": question, "top_k": 4})
                
                # Fetch Market Data if requested
                market_text = ""
                if ticker:
                    try:
                        res_mkt = requests.get(f"{API_URL}/market/{ticker}")
                        if res_mkt.status_code == 200:
                            mkt = res_mkt.json()
                            cap_display = f"{mkt['market_cap']:,}" if isinstance(mkt['market_cap'], (int, float)) else mkt['market_cap']
                            market_text = f"📈 **Live {mkt['ticker']} Market Data:** Price: \${mkt['latest_price_usd']} USD | Market Cap: \${cap_display} USD *(Source: Yahoo Finance)*"
                        else:
                            market_text = f"⚠️ Could not fetch market data for {ticker}."
                    except Exception:
                        pass # Ignore market errors so RAG answer still shows
                
                if res_rag.status_code == 200:
                    data = res_rag.json()
                    
                    # Display Market Data alongside the answer
                    if market_text:
                        st.success(market_text)
                        
                    st.markdown("### 🤖 Analyst Answer")
                    st.info(data['answer'])
                    
                    if data.get('sources'):
                        st.markdown("**📚 Sources Used:**")
                        for s in data['sources']:
                            st.markdown(f"📄 File: `{s['file']}` (Page {s['page']})")
                else:
                    st.error(f"Error: {res_rag.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")
