import streamlit as st
import requests
import os

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Finance RAG Analyst", layout="wide")

st.title("Finance RAG – Quarterly Financial Reports")

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
                st.json(res.json())
        except Exception:
            st.error("API offline")

# Main columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("2. Document Question Answering (RAG)")
    st.info("Ask questions about the uploaded financial PDFs.")
    question = st.text_input("Enter your question:")
    
    if st.button("Ask Document"):
        if not question:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    res = requests.post(f"{API_URL}/ask", json={"question": question, "top_k": 4})
                    if res.status_code == 200:
                        data = res.json()
                        st.markdown(f"**Answer:** {data['answer']}")
                        
                        if data['sources']:
                            st.write("---")
                            st.markdown("**Sources Used:**")
                            for s in data['sources']:
                                st.caption(f"- File: `{s['file']}`, Page: {s['page']}")
                    else:
                        st.error(f"Error: {res.json()['detail']}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {str(e)}")

with col2:
    st.header("3. Market Data")
    st.info("Get live stock market data via yfinance.")
    ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL, MSFT):")
    
    if st.button("Get Market Data"):
        if not ticker:
            st.warning("Please enter a ticker.")
        else:
            with st.spinner("Fetching..."):
                try:
                    res = requests.get(f"{API_URL}/market/{ticker}")
                    if res.status_code == 200:
                        data = res.json()
                        st.metric(label=f"{data['ticker']} Latest Price", value=f"${data['latest_price_usd']}")
                        st.write(f"**Market Cap:** {data['market_cap']}")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {str(e)}")
