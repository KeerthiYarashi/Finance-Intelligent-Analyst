# 📊 Finance RAG – Intelligent Analyst Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-blue)
![FastEmbed](https://img.shields.io/badge/FastEmbed-Local_GPU-purple)
![FlashRank](https://img.shields.io/badge/FlashRank-Re--ranker-yellow)

An enterprise-grade Retrieval-Augmented Generation (RAG) platform designed to automate the analysis of quarterly financial reports. This system ingests dense financial PDFs, converts them into high-dimensional vector embeddings, and leverages Large Language Models (LLMs) to provide mathematically accurate, source-cited answers to complex financial queries.

---

## 🏢 Business Scenario & Data Source
**Company Analyzed:** Microsoft Corporation (MSFT)
**Data Source:** [Microsoft Investor Relations](https://www.microsoft.com/en-us/investor)
**Documents Loaded:** Microsoft Q4 FY26 Press Releases and Earnings Factsheets.

This tool is built for research desks and investment advisory firms. Instead of manually parsing 60-page financial statements, analysts can query this system in plain English to instantly extract revenue numbers, margin trends, and management commentary—complete with verifiable PDF page citations and live market data integration.

---

## 🏗️ System Architecture

The application is fully decoupled, separating the backend processing from the frontend interface for maximum scalability.

1. **Document Ingestion Pipeline:** 
   - Reads PDFs using `PyPDFLoader`.
   - Chunks text using `RecursiveCharacterTextSplitter`.
2. **Vector Engine & Re-ranking:** 
   - Embeds chunks completely locally and for free using `FastEmbed` (`BAAI/bge-small-en-v1.5`) accelerated by ONNX GPU.
   - Stores vectors persistently on disk using `ChromaDB`.
   - Employs `FlashRank` to dynamically re-rank the top 20 retrieved chunks down to the 4 most relevant to avoid context pollution.
3. **Retrieval & LLM Generation:**
   - Converts user queries into vectors to perform cosine similarity searches.
   - Orchestrates the context and prompt via `LangChain`.
   - Generates answers using Google's `gemini-2.5-flash` with a strict temperature of `0.0` to prevent hallucinations.
4. **Live Market Data Engine:** Integrates `yfinance` to fetch real-time market cap and closing prices globally. Users can select from a dynamic dropdown of popular tickers (US tech, Indian NSE, and major indices).
5. **Premium FinTech User Interface:**
   - **Glassmorphism Aesthetic:** Custom CSS injected via Streamlit markdown for glowing gradients, hover animations, and a dark-mode FinTech terminal feel.
   - **Analyst Dashboard:** Real-time database metrics displayed dynamically in the sidebar.
6. **Idempotent Ingestion Engine:** Implements a strict metadata safety check to prevent duplicate vector chunking if the same PDFs are uploaded multiple times.

---

## 🛠️ Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/KeerthiYarashi/Finance-Intelligent-Analyst.git
cd Finance-Intelligent-Analyst
```

### 2. Configure the Environment
Create an isolated virtual environment and install the required dependencies:
```bash
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate

pip install -r finance-rag/requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory containing your API credentials:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application (Decoupled Services)
You must run the backend and frontend simultaneously in two separate terminals.

**Terminal 1: Start the FastAPI Backend**
```bash
cd finance-rag
python -m uvicorn api.main:app --reload
```
*The API documentation is available at `http://localhost:8000/docs`.*

**Terminal 2: Start the Streamlit Frontend**
```bash
cd finance-rag
python -m streamlit run app.py
```

---

## 📸 Application Screenshots

*(**INSTRUCTION FOR YOU**: Please take 1-2 screenshots of your working Streamlit application showing the index success message, the live market data, and an answer with sources. Replace the placeholders below with your images before submitting!)*

![App Screenshot 1](link-to-your-image.png)

---

## 📐 Critical Architectural Decisions

* **Chunk Size:** `1200` characters
* **Chunk Overlap:** `200` characters
* **Rationale:** Financial documents contain dense, tabular data. Standardizing on a larger 1200-character chunk ensures that entire financial tables, balance sheets, and their surrounding context remain perfectly intact inside a single mathematical vector. This vastly improves the LLM's ability to reason about comparative numbers.
* **Orchestration:** LangChain was utilized to future-proof the application, allowing seamless swapping of Vector Databases or LLM providers without rewriting core logic.

---

## ⚠️ Honest Note on Limitations & Learnings
While the GPT-4o model and ChromaDB pipeline work exceptionally well for narrative text and sentiment analysis, PDF financial tables inherently lose their vertical column alignment when converted to plain text via `PyPDFLoader`. This means complex grids of numbers sometimes get flattened into single lines. The system compensates via large chunk sizes, but heavily nested sub-tables still require the LLM to work harder to associate a number with its correct column header. Future iterations could explore multimodal OCR or HTML-table extraction for perfect grid alignment.

---

## 🧪 Assignment Test Cases

*(Note: The answers below were generated dynamically by the RAG engine based on the ingested Microsoft FY26 PDFs using Gemini 2.5 Flash and FlashRank).*

### 1. What was total revenue in the most recent quarter you loaded?
**Answer:** Total revenue in the most recent quarter (Three Months Ended March 31, 2026) was $82,886 million. *(Sources: PressReleaseFY26Q3.pdf Page 11, PressReleaseFY26Q2.pdf Page 11)*

### 2. Compare net profit across all the quarters you loaded. Which was highest?
**Answer:** Based on the context provided:
Net Income (GAAP) for the Three Months Ended December 31, 2024 was 24,108 million.
Net Income (GAAP) for the Three Months Ended December 31, 2025 was 38,458 million.
Comparing these two quarters, the highest net profit was $38,458 million for the three months ended December 31, 2025. *(Sources: PressReleaseFY26Q2.pdf Page 1, PressReleaseFY26Q2.pdf Page 11)*

### 3. How did revenue in the latest quarter compare with the same quarter of the previous year?
**Answer:** For the quarter ended June 30, 2026, revenue was $90.0 billion and increased 18% (up 17% in constant currency) compared to the corresponding period of the last fiscal year. *(Sources: PressReleaseFY26Q4.pdf Page 1, PressReleaseFY26Q2.pdf Page 1)*

### 4. What did management say about the demand outlook or business environment?
**Answer:** The information is not available in the uploaded documents. The context states that Microsoft will provide forward-looking guidance on its earnings conference call and webcast, but it does not detail what management said about the demand outlook or business environment. *(Sources: PressReleaseFY26Q3.pdf Page 2, PressReleaseFY26Q2.pdf Page 3)*

### 5. Which business segment or geography grew fastest, and by how much?
**Answer:** The Intelligent Cloud business segment grew fastest.
Intelligent Cloud grew by 6,805 million, from 24,092 million in 2024 to $30,897 million in 2025. This represents a growth of approximately 28.25%.
Productivity and Business Processes grew by 4,703 million, from 28,317 million in 2024 to $33,020 million in 2025. This represents a growth of approximately 16.61%.
More Personal Computing grew by 580 million, from 13,176 million in 2024 to $13,756 million in 2025. This represents a growth of approximately 4.40%.
Information regarding growth by geography is not available in the uploaded documents. *(Sources: PressReleaseFY26Q1.pdf Page 11)*

### 6. What was the operating margin in each quarter, and is the trend rising or falling?
**Answer:** The information is not available in the uploaded documents. *(Sources: PressReleaseFY26Q2.pdf Page 2, PressReleaseFY26Q1.pdf Page 2)*

### 7. Was any dividend declared? State the amount per share and the record date.
**Answer:** The information regarding the dividend amount per share and the record date is not available in the uploaded documents. The documents only state "Common stock cash dividends paid" as 6,169 million for the three months ended September 30, 2025, and 5,574 million for the three months ended September 30, 2024. *(Sources: PressReleaseFY26Q3.pdf Page 1, PressReleaseFY26Q1.pdf Page 10)*

### 8. What risks, headwinds, or challenges are mentioned in the documents?
**Answer:** The risks, headwinds, or challenges mentioned in the documents are: Security, privacy, and execution risks; Issues about the use of AI; Excessive outages, data losses; Supply or quality problems; Potential consequences of new legal requirements; Claims against them; Uncertainties relating to business with government customers; Additional tax liabilities; Claims that Microsoft has infringed intellectual property; Damage to reputation or brands; Adverse economic or market conditions; Catastrophic events or geopolitical conditions, such as the COVID-19 pandemic. *(Sources: PressReleaseFY26Q1.pdf Page 5)*

### 9. Give me a three-line summary of the latest quarter for a client email.
**Answer:** Microsoft reported strong results for the quarter ended June 30, 2026. Revenue reached 90.0 billion, an 18% increase, with GAAP net income growing 31% to 35.8 billion. Diluted earnings per share also saw a significant rise of 32% to $4.81. *(Sources: PressReleaseFY26Q4.pdf Page 1, PressReleaseFY26Q4.pdf Page 10)*

### 10. Deliberate Trap Question: "What is the CEO's personal shareholding in 2015?"
**Answer:** The information is not available in the uploaded documents. *(Sources: PressReleaseFY26Q3.pdf Page 1, PressReleaseFY26Q4.pdf Page 10)*
*(The system successfully executed an honest refusal to prevent hallucinations).*
