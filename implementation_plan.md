# Finance RAG – Implementation Plan & Learning Roadmap

This document is a step-by-step, test-driven learning and implementation roadmap. It builds the system from the inside out, starting with tiny experiments and gradually layering on complexity. 

---

## PHASE 0 — UNDERSTAND THE ASSIGNMENT

### Goal
Define the exact business problem and system requirements before writing any code.

### What You Will Learn
The core "why" behind the project: why GPT-4o alone fails at this task, and why we need RAG, ChromaDB, and persistence.

### Why This Is Needed
If you don't understand the problem, you will build the wrong solution.

### What You Will Build
A mental model and a conceptual requirement-to-phase mapping.

### Files Involved
None.

### Step-by-Step Tasks
1. Define the business problem: Analysts waste hours reading PDFs to answer routine questions.
2. Define the user: An investment analyst uploading 3-4 quarterly PDFs.
3. Define the limitation: GPT-4o hallucinates on unseen/recent private data.
4. Define RAG's role: We fetch the exact text from the PDF and force GPT-4o to read it.
5. Create a mental table mapping assignment requirements to the phases below.

### Commands to Run
None.

### Expected Output
A clear understanding of the project's boundaries and goals.

### Test
Can you answer why the "trap question" is included? (Answer: to prove the system refuses to answer when data is missing).

### Common Mistakes
Jumping straight to writing Streamlit or FastAPI code.

### Debugging
Re-read the assignment prompt if any concept feels vague.

### You Should Understand
- The business problem.
- Why GPT-4o alone is insufficient.
- Why source citations and honest refusals are mandatory.

### Do Not Move Forward Until
You can explain the assignment goals in 60 seconds without looking at the prompt.

---

## PHASE 1 — UNDERSTAND RAG

### Goal
Understand the Retrieval-Augmented Generation (RAG) conceptual pipeline.

### What You Will Learn
LLM context windows, hallucination, embeddings, vectors, vector databases, semantic similarity, chunking, and grounded generation.

### Why This Is Needed
You cannot debug a RAG pipeline if you don't know how data flows through it conceptually.

### What You Will Build
A theoretical understanding of the flow.

### Files Involved
None.

### Step-by-Step Tasks
1. Understand **Retrieval**: Extracting text from a PDF, splitting it into chunks, converting chunks to numbers (embeddings), and storing them in a vector DB.
2. Understand **Similarity Search**: Converting a user's question into numbers, and finding the closest matching chunks mathematically.
3. Understand **Augmentation**: Sticking those retrieved chunks into a prompt.
4. Understand **Generation**: Sending the prompt to GPT-4o to get an answer.

### Commands to Run
None.

### Expected Output
Mastery of RAG vocabulary.

### Test
Trace this example: PDF says "Revenue increased 12%". User asks "What happened to revenue?" How does the system find that sentence?

### Common Mistakes
Thinking the vector database "reads" the text (it only compares math vectors).

### Debugging
If you forget a term, review RAG architecture diagrams.

### You Should Understand
- Embeddings (text to numbers).
- Grounding (forcing the LLM to use provided context).
- `top_k` (limiting how many chunks we retrieve).

### Do Not Move Forward Until
You can explain the difference between a traditional database search and a semantic vector search.

---

## PHASE 2 — UNDERSTAND THE FINAL ARCHITECTURE

### Goal
Map the conceptual RAG pipeline to the specific tools required by the assignment.

### What You Will Learn
How Streamlit, FastAPI, LangChain/SDK, ChromaDB, and OpenAI fit together.

### Why This Is Needed
To ensure modularity. You must know why `yfinance` is separate from `rag.py`.

### What You Will Build
A blueprint of the data flow.

### Files Involved
None.

### Step-by-Step Tasks
1. Map **Upload Flow**: Streamlit -> FastAPI `/ingest` -> `ingest.py` -> Splitter -> Embeddings -> ChromaDB.
2. Map **Question Flow**: Streamlit -> FastAPI `/ask` -> `rag.py` -> ChromaDB -> GPT-4o.
3. Map **Market Flow**: Streamlit -> FastAPI `/market` -> `yfinance`.
4. Define responsibilities to prevent putting all logic in `api/main.py`.

### Commands to Run
None.

### Expected Output
A clear mental map of the system's modularity.

### Test
Where does text splitting happen? (`ingest.py`). Where does GPT-4o get called? (`rag.py`).

### Common Mistakes
Planning to write all backend code inside FastAPI route handlers.

### Debugging
Refer back to `architecture.md`.

### You Should Understand
- The strict separation between Document RAG and Market Data.

### Do Not Move Forward Until
You can draw the architecture diagram on a whiteboard.

---

## PHASE 3 — CREATE DEVELOPMENT ENVIRONMENT

### Goal
Initialize the project structure and install dependencies.

### What You Will Learn
Python virtual environments and dependency management for RAG.

### Why This Is Needed
A clean environment prevents dependency conflicts (e.g., LangChain version issues).

### What You Will Build
The `finance-rag/` directory and virtual environment.

### Files Involved
- `requirements.txt`
- `.gitignore`

### Step-by-Step Tasks
1. Create folder `finance-rag/`.
2. Create virtual environment `python -m venv venv`.
3. Activate virtual environment.
4. Create empty files: `app.py`, `ingest.py`, `rag.py`, `api/main.py`.
5. Create `requirements.txt` with: `fastapi`, `uvicorn`, `streamlit`, `langchain`, `langchain-openai`, `chromadb`, `pypdf`, `python-dotenv`, `yfinance`.
6. Run `pip install -r requirements.txt`.
7. Create `.gitignore` ignoring `venv/`, `.env`, `chroma_db/`, `__pycache__/`.

### Commands to Run
```bash
mkdir finance-rag
cd finance-rag
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Expected Output
A working Python environment with all libraries installed.

### Test
Run `python -c "import fastapi, chromadb, langchain; print('Success!')"`

### Common Mistakes
Forgetting to activate the virtual environment before installing.

### Debugging
If an import fails, ensure the environment is activated and the package is in `requirements.txt`.

### You Should Understand
- Project directory structure.
- What each dependency is used for.

### Do Not Move Forward Until
The test command prints "Success!".

---

## PHASE 4 — API KEY SECURITY

### Goal
Securely load the OpenAI API key.

### What You Will Learn
Environment variables and `.env` files.

### Why This Is Needed
Committing an API key to GitHub will result in it being immediately revoked.

### What You Will Build
`.env` and `.env.example`.

### Files Involved
- `.env`
- `.env.example`
- `.gitignore`
- `scratch/test_env.py`

### Step-by-Step Tasks
1. Verify `.env` is explicitly written in `.gitignore`.
2. Create `.env` and add `OPENAI_API_KEY=sk-...`
3. Create `.env.example` and add `OPENAI_API_KEY=your_key_here`.
4. Write a script to load and print the key using `dotenv`.

### Commands to Run
```bash
python scratch/test_env.py
```

### Expected Output
The script securely loads and prints a masked version of your API key.

### Test
Ensure `git status` does NOT list `.env` as an untracked file.

### Common Mistakes
Accidentally naming the file `env` instead of `.env`.

### Debugging
If the key loads as `None`, check that `load_dotenv()` is called before `os.getenv()`.

### You Should Understand
- Why we never hardcode keys.

### Do Not Move Forward Until
`.env` is hidden from git and successfully loaded in Python.

---

## PHASE 5 — SELECT COMPANY

### Goal
Download valid financial PDFs for testing.

### What You Will Learn
Data selection constraints for RAG.

### Why This Is Needed
If you pick a scanned PDF, the entire pipeline fails because no text can be extracted.

### What You Will Build
A populated `data/` folder.

### Files Involved
- `data/*.pdf`

### Step-by-Step Tasks
1. Choose a company (e.g., Infosys, Microsoft).
2. Download 3-4 consecutive quarterly press releases or fact sheets.
3. Save them to the `data/` folder.
4. **CRITICAL:** Open each PDF, click and drag your mouse. Ensure the text highlights blue (is selectable).

### Commands to Run
None.

### Expected Output
3-4 valid, text-selectable PDFs in your `data/` folder.

### Test
Manually copy a sentence from the PDF and paste it into notepad.

### Common Mistakes
Downloading full audited annual statements instead of quarterly press releases.

### Debugging
If it copies as an image or empty space, discard the file. Find a non-scanned version.

### You Should Understand
- Why OCR is forbidden in this assignment.

### Do Not Move Forward Until
You have 3-4 selectable PDFs saved locally.

---

## PHASE 6 — MINI EXPERIMENT: READ ONE PDF

### Goal
Extract raw text from a PDF programmatically.

### What You Will Learn
How PDF text extraction works and why tables lose alignment.

### Why This Is Needed
To verify `pypdf` can read your specific files before building complex logic.

### What You Will Build
A temporary script `test_pdf.py`.

### Files Involved
- `scratch/test_pdf.py`

### Step-by-Step Tasks
1. Use `PyPDFLoader` (LangChain) or `pypdf` to load one PDF from `data/`.
2. Iterate through the first 2 pages.
3. Print the raw text to the console.

### Commands to Run
```bash
python scratch/test_pdf.py
```

### Expected Output
Blocks of text printing to the terminal.

### Test
Compare the terminal output to the actual PDF content.

### Common Mistakes
Assuming text will look perfectly formatted in the console.

### Debugging
If text is missing, the PDF might have complex encodings. Try a different company's PDF.

### You Should Understand
- Extracted text is messy, and tables lose visual structure.

### Do Not Move Forward Until
You can successfully print readable text from your PDF.

---

## PHASE 7 — PAGE METADATA

### Goal
Ensure every extracted page retains its source filename and page number.

### What You Will Learn
Metadata handling in documents.

### Why This Is Needed
The final assignment requires citing the exact file and page number. If lost here, it can't be recovered later.

### What You Will Build
Update `test_pdf.py` to extract metadata.

### Files Involved
- `scratch/test_pdf.py`

### Step-by-Step Tasks
1. Modify the script to inspect the `metadata` dictionary of the loaded document objects.
2. Print `doc.metadata['source']` and `doc.metadata['page']` alongside the text.

### Commands to Run
```bash
python scratch/test_pdf.py
```

### Expected Output
Console output showing: `[Page 1 of Q3.pdf]: "Revenue was..."`

### Test
Verify the printed page number matches the physical PDF page number (note: 0-indexed vs 1-indexed).

### Common Mistakes
Forgetting that PDF page indices often start at 0.

### Debugging
If metadata is empty, check the specific loader's documentation (e.g., `PyPDFLoader` includes this automatically).

### You Should Understand
- Why metadata travels alongside text through the entire RAG pipeline.

### Do Not Move Forward Until
You can print the exact filename and page number for a block of text.

---

## PHASE 8 — CHUNKING

### Goal
Split large documents into smaller, overlapping chunks.

### What You Will Learn
Context limits, retrieval precision, and why overlap is crucial.

### Why This Is Needed
You cannot send a 60-page PDF to the LLM. 1200-character chunks balance precision and context.

### What You Will Build
A chunking script using `RecursiveCharacterTextSplitter`.

### Files Involved
- `scratch/test_chunk.py`

### Step-by-Step Tasks
1. Load a PDF.
2. Initialize `RecursiveCharacterTextSplitter` with `chunk_size=1200` and `chunk_overlap=200`. (1200 helps keep financial tables together).
3. Split the loaded documents.
4. Print the total number of chunks and the first chunk's text and metadata.

### Commands to Run
```bash
python scratch/test_chunk.py
```

### Expected Output
`Generated 145 chunks. Chunk 1 length: 1150 chars. Metadata: {'source': '...', 'page': 0}`

### Test
Verify the metadata (filename and page) successfully copied over to the child chunks.

### Common Mistakes
Setting overlap to 0, which cuts sentences and financial figures in half.

### Debugging
If chunks are too small, ensure `chunk_size` is based on characters, not tokens.

### You Should Understand
- Why `chunk_overlap=200` prevents data loss at chunk boundaries.

### Do Not Move Forward Until
You can reliably split a PDF into chunks that retain their page metadata.

---

## PHASE 9 — EMBEDDINGS

### Goal
Convert text chunks into numerical vectors.

### What You Will Learn
Semantic meaning, query embeddings, and the OpenAI API.

### Why This Is Needed
To search by meaning (e.g., "profit") instead of exact keyword match.

### What You Will Build
A script that generates a vector using `text-embedding-3-small`.

### Files Involved
- `scratch/test_embed.py`

### Step-by-Step Tasks
1. Initialize OpenAI Embeddings (`text-embedding-3-small`).
2. Pass a single string "Net profit increased" to the embedder.
3. Print the length of the resulting vector list.

### Commands to Run
```bash
python scratch/test_embed.py
```

### Expected Output
A list of floats, usually of length 1536.

### Test
Verify the API key works and the request doesn't throw a billing/auth error.

### Common Mistakes
Using an expensive model like `text-embedding-ada-002` when `text-embedding-3-small` is specified and cheaper.

### Debugging
If you get an Auth error, check your `.env` loading.

### You Should Understand
- Text goes in, a list of 1536 numbers comes out.

### Do Not Move Forward Until
You can successfully generate a vector from the OpenAI API.

---

## PHASE 10 — CHROMADB

### Goal
Store vectors in a local, persistent database.

### What You Will Learn
Vector databases, collections, and persistence on disk.

### Why This Is Needed
To save embeddings so you don't have to re-pay OpenAI to embed the PDFs every time you restart the app.

### What You Will Build
A script that saves chunks to ChromaDB.

### Files Involved
- `scratch/test_chroma.py`
- `chroma_db/`

### Step-by-Step Tasks
1. Initialize a Chroma client pointing to a local directory `./chroma_db`.
2. Load, chunk, and embed a single PDF.
3. Store the chunks in a Chroma collection.
4. Verify the `chroma_db/` folder is created on your hard drive.

### Commands to Run
```bash
python scratch/test_chroma.py
```

### Expected Output
No errors, and a new `chroma_db` folder appears in your workspace.

### Test
Check your filesystem to ensure `chroma_db` has SQLite/binary files inside it.

### Common Mistakes
Using an in-memory Chroma client that wipes data on restart.

### Debugging
If the folder isn't created, check the `persist_directory` argument in Chroma.

### You Should Understand
- How `ChromaDB` links the vector, the text, and the metadata together.

### Do Not Move Forward Until
The `chroma_db/` directory successfully populates on your disk.

---

## PHASE 11 — RETRIEVAL EXPERIMENT

### Goal
Perform a semantic search against your database.

### What You Will Learn
Similarity search and the importance of `top_k`.

### Why This Is Needed
To verify that the database can actually find the right chunks before throwing an LLM into the mix.

### What You Will Build
A script that queries ChromaDB.

### Files Involved
- `scratch/test_retrieve.py`

### Step-by-Step Tasks
1. Connect to the existing `./chroma_db` (do NOT ingest data again).
2. Ask a question: "What was the revenue?"
3. Retrieve `top_k=4` chunks.
4. Print the text and metadata of those 4 chunks.

### Commands to Run
```bash
python scratch/test_retrieve.py
```

### Expected Output
4 printed text blocks that talk about revenue, along with their page numbers.

### Test
Does the retrieved text actually contain the answer to the question?

### Common Mistakes
Re-indexing the documents every time you run a query, wasting money.

### Debugging
If results are irrelevant, try changing the question wording.

### You Should Understand
- If the answer isn't in these 4 chunks, GPT-4o cannot answer the question.

### Do Not Move Forward Until
You can reliably retrieve relevant text and page numbers for a test question.

---

## PHASE 12 — BUILD ingest.py

### Goal
Productionize the ingestion pipeline into a reusable module.

### What You Will Learn
Modular programming for RAG.

### Why This Is Needed
FastAPI and Streamlit should not contain raw PDF parsing code.

### What You Will Build
`ingest.py`

### Files Involved
- `ingest.py`

### Step-by-Step Tasks
1. Create a function `ingest_documents(file_paths)`.
2. Move the loading, chunking (1200/200), and Chroma storage logic here.
3. Have it return a dictionary: `{"files": len(file_paths), "chunks": total_chunks}`.

### Commands to Run
None (this is a module).

### Expected Output
Clean, reusable Python functions.

### Test
Write a quick `if __name__ == "__main__":` block to run it locally on `data/`.

### Common Mistakes
Hardcoding file paths instead of accepting them as arguments.

### Debugging
Ensure paths resolve correctly whether called from root or inside an `api/` folder.

### You Should Understand
- This script is invoked when the user clicks "Index" in Streamlit.

### Do Not Move Forward Until
`ingest.py` cleanly processes a list of files and returns the correct stats.

---

## PHASE 13 — BUILD rag.py RETRIEVAL

### Goal
Productionize the retrieval logic.

### What You Will Learn
Isolating search logic.

### Why This Is Needed
Separation of concerns.

### What You Will Build
`rag.py`

### Files Involved
- `rag.py`

### Step-by-Step Tasks
1. Create a function `answer_query(question, top_k=4)`.
2. Connect to ChromaDB.
3. Perform the similarity search.
4. (For now) Just return the retrieved chunks and their metadata as a list.

### Commands to Run
None.

### Expected Output
Reusable search function.

### Test
Call `answer_query("profit")` locally and print results.

### Common Mistakes
Forgetting to initialize the embeddings model inside the retrieval script.

### Debugging
Ensure it points to the exact same `persist_directory` as `ingest.py`.

### You Should Understand
- This is the first half of the RAG action.

### Do Not Move Forward Until
`rag.py` successfully retrieves documents from the persisted DB.

---

## PHASE 14 — ADD GPT-4o

### Goal
Generate an answer from the retrieved context.

### What You Will Learn
Prompt grounding, context injection, and system prompts.

### Why This Is Needed
To turn raw chunks into a fluent, human-readable answer.

### What You Will Build
Update `rag.py` to call GPT-4o.

### Files Involved
- `rag.py`

### Step-by-Step Tasks
1. Initialize OpenAI LLM (`gpt-4o`) with `temperature=0`.
2. Create a prompt template injecting `{context}` and `{question}`.
3. ADD THE MANDATORY RULE: "Answer only from the context provided below. If the context does not contain the answer, reply that the information is not available..."
4. Combine chunks into a single string.
5. Send to GPT-4o.

### Commands to Run
Run `rag.py` locally.

### Expected Output
A natural language answer derived only from the text.

### Test
Ask for the revenue. The answer should be correct.

### Common Mistakes
Using a high temperature, causing the model to hallucinate or slightly alter numbers.

### Debugging
Print the exact prompt being sent to the LLM to ensure `{context}` is populated.

### You Should Understand
- How prompt grounding restricts the LLM's vast knowledge base.

### Do Not Move Forward Until
GPT-4o successfully answers a question based on your PDF context.

---

## PHASE 15 — SOURCE CITATIONS

### Goal
Return the filename and page numbers alongside the answer.

### What You Will Learn
Data formatting.

### Why This Is Needed
The assignment mandates source citations for analyst verification.

### What You Will Build
Modify `rag.py` to return a structured dictionary.

### Files Involved
- `rag.py`

### Step-by-Step Tasks
1. After generating the answer, loop through the retrieved chunks.
2. Extract `source` and `page` metadata.
3. Deduplicate sources (if 2 chunks came from Page 7, only list Page 7 once).
4. Return `{"answer": text, "sources": [{"file": "X", "page": Y}]}`.

### Commands to Run
Run `rag.py` locally.

### Expected Output
A dictionary containing the answer string and a list of source objects.

### Test
Check the returned page number against the physical PDF.

### Common Mistakes
Returning raw metadata dictionaries that look ugly in the UI.

### Debugging
If page numbers are off by 1, remember `PyPDFLoader` is 0-indexed. Add +1 if desired.

### You Should Understand
- How metadata flows from extraction to the final output.

### Do Not Move Forward Until
The output contains the answer AND clean source citations.

---

## PHASE 16 — HONEST REFUSAL

### Goal
Implement and test the trap question logic.

### What You Will Learn
Hallucination prevention testing.

### Why This Is Needed
Worth 10 marks. The system must not invent financial figures.

### What You Will Build
A test run of the trap question.

### Files Involved
- `rag.py`

### Step-by-Step Tasks
1. Pass the question: "What is the CEO's personal shareholding in 2015?"
2. Observe the answer.
3. If it answers the question by guessing, strengthen your system prompt.

### Commands to Run
None.

### Expected Output
"The information is not available in the uploaded documents."

### Test
Try another fake question: "Does the company own a base on Mars?"

### Common Mistakes
Forgetting the strict grounding instructions in the system prompt.

### Debugging
If it guesses, set `temperature=0` and make the system prompt extremely aggressive ("DO NOT GUESS").

### You Should Understand
- Why "I don't know" is a successful outcome in RAG.

### Do Not Move Forward Until
The trap question is reliably refused.

---

## PHASE 17 — COMPLETE RAG CORE

### Goal
Verify the independent RAG pipeline works flawlessly before adding APIs or UIs.

### What You Will Learn
System integration testing.

### Why This Is Needed
If you build FastAPI now and it breaks, you won't know if the API broke or the RAG broke.

### What You Will Build
A complete terminal test.

### Files Involved
- `ingest.py`, `rag.py`

### Step-by-Step Tasks
1. Delete `chroma_db/`.
2. Run `ingest_documents()`.
3. Run `answer_query()` with a real question.
4. Run `answer_query()` with the trap question.

### Commands to Run
Terminal python script.

### Expected Output
Flawless ingestion, answering, citations, and refusal.

### Test
Complete the milestone checklist.

### Common Mistakes
Moving to FastAPI before this works perfectly.

### Debugging
Fix any issues directly in `ingest.py` or `rag.py`.

### You Should Understand
- The core logic is complete. Everything else is just wrapping.

### Do Not Move Forward Until
You are 100% confident in the RAG pipeline.

---

## PHASE 18 — FASTAPI

### Goal
Wrap the core logic in a REST API.

### What You Will Learn
FastAPI routes, Pydantic models, and HTTP flows.

### Why This Is Needed
To fulfill the optional (but implemented) bonus requirement.

### What You Will Build
`api/main.py` with 3 endpoints.

### Files Involved
- `api/main.py`

### Step-by-Step Tasks
1. Create FastAPI app.
2. Build `POST /ingest` (accepts files, saves them to temp, calls `ingest.py`).
3. Build `POST /ask` (accepts JSON `{"question": "...", "top_k": 4}`, calls `rag.py`).
4. Build `GET /stats` (returns DB stats).
5. Run uvicorn.

### Commands to Run
```bash
uvicorn api.main:app --reload
```

### Expected Output
Server starts on localhost:8000.

### Test
Visit `http://localhost:8000/docs` and test all 3 endpoints using Swagger.

### Common Mistakes
Duplicating ChromaDB logic in `main.py` instead of importing from `rag.py`.

### Debugging
If `/ingest` fails, check how you are handling `UploadFile` objects in FastAPI.

### You Should Understand
- How HTTP POST payloads translate to Python function arguments.

### Do Not Move Forward Until
Swagger UI successfully returns an answer and sources via `/ask`.

---

## PHASE 19 — STREAMLIT

### Goal
Build the analyst UI.

### What You Will Learn
Streamlit state, file uploaders, and HTTP requests (`requests` library).

### Why This Is Needed
Analysts need a friendly interface, not a Swagger page.

### What You Will Build
`app.py`

### Files Involved
- `app.py`

### Step-by-Step Tasks
1. Build file uploader and an "Index" button. On click, POST to FastAPI `/ingest`.
2. Build chat input or text box. On submit, POST to FastAPI `/ask`.
3. Display the returned answer.
4. Loop through returned sources and display them as small captions.

### Commands to Run
```bash
streamlit run app.py
```

### Expected Output
A clean web UI.

### Test
Upload a file in the UI, index it, ask a question, see the answer and sources.

### Common Mistakes
Doing the RAG processing directly in `app.py` instead of making an HTTP request to FastAPI.

### Debugging
If the UI hangs, ensure Uvicorn is running in a separate terminal window.

### You Should Understand
- Separation of frontend and backend.

### Do Not Move Forward Until
The UI successfully controls the backend.

---

## PHASE 20 — PERSISTENCE

### Goal
Prove that ChromaDB saves data between sessions.

### What You Will Learn
Database persistence verification.

### Why This Is Needed
Mandatory grading criteria.

### What You Will Build
A restart test.

### Files Involved
- Entire App

### Step-by-Step Tasks
1. Ensure app is running and data is indexed.
2. Ask a question to verify it works.
3. KILL the FastAPI server (Ctrl+C).
4. Restart the FastAPI server.
5. Do NOT click Index in Streamlit.
6. Ask a new question.

### Commands to Run
Restart Uvicorn.

### Expected Output
The system answers correctly without needing re-indexing.

### Test
Verify the answer is accurate.

### Common Mistakes
Forgetting that restarting Streamlit doesn't wipe ChromaDB, but restarting FastAPI might if ChromaDB is set to in-memory.

### Debugging
If it fails (says "no chunks found"), check ChromaDB's `persist_directory` configuration.

### You Should Understand
- Disk storage vs RAM storage.

### Do Not Move Forward Until
The system survives a restart.

---

## PHASE 21 — YFINANCE

### Goal
Add the optional market data feature separately from RAG.

### What You Will Learn
External API integration.

### Why This Is Needed
Bonus assignment requirement.

### What You Will Build
A new FastAPI endpoint and a Streamlit sidebar/section.

### Files Involved
- `api/main.py`
- `app.py`

### Step-by-Step Tasks
1. Add `GET /market/{ticker}` to `api/main.py`. Use `yfinance` to fetch the current price and market cap.
2. Add a sidebar in Streamlit allowing the user to enter a ticker (e.g., "AAPL").
3. Call the endpoint and display the data.

### Commands to Run
None.

### Expected Output
Real-time stock price visible in the UI.

### Test
Enter "MSFT" and verify the price is current.

### Common Mistakes
Trying to pipe `yfinance` data into the LLM prompt. Keep it separate as a distinct UI feature.

### Debugging
If `yfinance` times out, catch the exception and return a friendly error message.

### You Should Understand
- How to augment an app with external APIs without breaking the RAG core.

### Do Not Move Forward Until
Market data is visible in the UI.

---

## PHASE 22 — COMPLETE APPLICATION

### Goal
Final end-to-end testing of all paths.

### What You Will Learn
System validation.

### Why This Is Needed
To ensure nothing broke during the final integrations.

### What You Will Build
Confidence in the app.

### Files Involved
- All files.

### Step-by-Step Tasks
1. Test Document RAG.
2. Test Market Data.
3. Test stats endpoint.

### Commands to Run
None.

### Expected Output
100% functional app.

### Test
Perform the actions exactly as a user would.

### Common Mistakes
Assuming it works without doing a fresh run.

### Debugging
Clear `chroma_db/` and start from absolute scratch.

### You Should Understand
- The full architecture data flow.

### Do Not Move Forward Until
The app runs flawlessly from a blank slate.

---

## PHASE 23 — ASSIGNMENT QUESTIONS

### Goal
Generate the exact answers for the README submission.

### What You Will Learn
Prompt evaluation.

### Why This Is Needed
Mandatory grading criteria.

### What You Will Build
The answers for your README.

### Files Involved
- Streamlit UI

### Step-by-Step Tasks
1. Take the 10 questions from the assignment.
2. Adapt the wording to your chosen company.
3. Ask each question through Streamlit.
4. Record the answer, filename, and page number.
5. Manually open the PDF and verify at least 3 financial figures.

### Commands to Run
None.

### Expected Output
10 recorded answers.

### Test
Manual PDF verification.

### Common Mistakes
Not adapting the wording of the question to the company.

### Debugging
If an answer is wrong, proceed to Phase 24.

### You Should Understand
- The LLM is only as good as the retrieved chunks.

### Do Not Move Forward Until
All 10 answers are recorded.

---

## PHASE 24 — DEBUGGING RAG

### Goal
Fix any incorrect answers systematically.

### What You Will Learn
The RAG debugging hierarchy.

### Why This Is Needed
Answers are rarely perfect on the first try.

### What You Will Build
Debugging skills.

### Files Involved
- Console / logs.

### Step-by-Step Tasks
1. If an answer is wrong, print the retrieved chunks for that question.
2. Does the text contain the answer? 
3. YES -> The LLM failed. Adjust the prompt.
4. NO -> Retrieval failed. Adjust chunk size, `top_k`, or question wording.

### Commands to Run
None.

### Expected Output
Corrected answers.

### Test
Re-ask the failed question.

### Common Mistakes
Blaming GPT-4o before checking the retrieved chunks.

### Debugging
Focus heavily on `top_k`.

### You Should Understand
- Why debugging RAG is a search problem, not just an AI problem.

### Do Not Move Forward Until
The 10 answers look solid.

---

## PHASE 25 — ERROR HANDLING

### Goal
Ensure the app doesn't crash on bad inputs.

### What You Will Learn
Resilience.

### Why This Is Needed
Graders will test edge cases.

### What You Will Build
Try/except blocks where necessary.

### Files Involved
- `app.py`, `api/main.py`

### Step-by-Step Tasks
1. Upload an image (not a PDF). Handle error gracefully.
2. Ask a question before indexing. Handle error gracefully.
3. Enter an invalid ticker. Handle error gracefully.

### Commands to Run
None.

### Expected Output
UI warnings instead of red crash screens.

### Test
Try to break the app purposefully.

### Common Mistakes
Letting FastAPI 500 errors bleed to the frontend without a friendly message.

### Debugging
Check Uvicorn logs for the exact exception stack trace.

### You Should Understand
- Defensive programming.

### Do Not Move Forward Until
The app survives bad inputs.

---

## PHASE 26 — README

### Goal
Create the mandatory submission documentation.

### What You Will Learn
Professional technical writing.

### Why This Is Needed
Grading relies heavily on the README.

### What You Will Build
`README.md`

### Files Involved
- `README.md`

### Step-by-Step Tasks
Create the file and include:
1. Company chosen + PDF links.
2. Setup and run instructions.
3. Chunk size (1200) and overlap (200) with justification.
4. Screenshots of working app.
5. The 10 test questions and your app's answers.
6. An honest note on what did not work well (limitations).

### Commands to Run
None.

### Expected Output
A polished, complete README.

### Test
Read it as a stranger. Can you run the app using only these instructions?

### Common Mistakes
Forgetting the "honest note on limitations".

### Debugging
Ensure screenshot links resolve correctly in Markdown.

### You Should Understand
- Documentation is as important as code.

### Do Not Move Forward Until
All 6 mandatory README items are present.

---

## PHASE 27 — GITHUB

### Goal
Submit the code cleanly.

### What You Will Learn
Repository hygiene.

### Why This Is Needed
If you commit your API key, you fail security.

### What You Will Build
A public GitHub repo.

### Files Involved
- `.gitignore`

### Step-by-Step Tasks
1. Verify `.env` and `chroma_db/` are in `.gitignore`.
2. `git init`
3. `git add .`
4. `git commit -m "Initial commit"`
5. Push to public GitHub repo.

### Commands to Run
```bash
git status
```

### Expected Output
`.env` DOES NOT appear in the status list.

### Test
Check the GitHub web UI to ensure no secrets are visible.

### Common Mistakes
Committing `venv/` or `.env`.

### Debugging
If committed accidentally, revoke the key immediately and rewrite git history or delete the repo and start over.

### You Should Understand
- Security hygiene.

### Do Not Move Forward Until
The code is live and secure on GitHub.

---

## PHASE 28 — 3-MINUTE DEMO

### Goal
Record the mandatory video.

### What You Will Learn
Technical presentation.

### Why This Is Needed
Mandatory grading criteria.

### What You Will Build
A 3-minute video (MP4/YouTube).

### Files Involved
- Screen recording software.

### Step-by-Step Tasks
Record following this script:
0:00 - Explain architecture/problem.
0:20 - Show PDF upload and index confirmation.
1:00 - Ask 3 questions, point out sources/page numbers.
2:20 - Ask the trap question, show the honest refusal.
2:40 - Briefly show FastAPI Swagger.
2:55 - Conclude.

### Commands to Run
None.

### Expected Output
A crisp, under-3-minute video.

### Test
Time the video. Ensure the refusal works on camera.

### Common Mistakes
Rambling over 3 minutes.

### Debugging
Do a practice run before hitting record.

### You Should Understand
- How to demo software effectively.

### Do Not Move Forward Until
The video is uploaded/linked.

---

## PHASE 29 — FINAL SUBMISSION CHECKLIST

### Goal
Final verify before submission.

### What You Will Learn
QA review.

### Why This Is Needed
To ensure max marks.

### What You Will Build
Confidence.

### Files Involved
- None.

### Step-by-Step Tasks
Review this checklist:
- [ ] 3–4 quarterly PDFs in `data/`
- [ ] Company selected + official PDF links in README
- [ ] Chunking works (1200 size, 200 overlap)
- [ ] ChromaDB persists after restart
- [ ] GPT-4o answers with sources and page numbers
- [ ] Trap question refused correctly
- [ ] FastAPI backend working
- [ ] Streamlit/Gradio working
- [ ] .env is in .gitignore
- [ ] 10 questions answered and recorded
- [ ] README complete (screenshots + limitations)
- [ ] 3-minute demo video recorded and linked
- [ ] Repository link ready

### Commands to Run
None.

### Expected Output
A ready-to-submit project.

### Test
Click your own GitHub link in incognito mode to ensure it's public.

### Common Mistakes
Leaving the repo on private.

### Debugging
None.

### You Should Understand
- You have built a complete, production-style RAG application.

### Do Not Move Forward Until
Everything is checked off.

---

## FINAL LEARNING OUTCOME

**What I will know after completing this project:**
By following this plan, you will have moved from a RAG beginner to someone who can confidently explain and build:
1. Document Ingestion (pypdf, Recursive Splitter)
2. Metadata Preservation (tracking page numbers)
3. Embedding Generation (OpenAI text-embedding-3-small)
4. Vector Database Management (ChromaDB persistence)
5. Semantic Retrieval Search (top_k logic)
6. Prompt Grounding & Hallucination Prevention (GPT-4o temperature 0)
7. Source Attribution (citing file and page)
8. API Architecture (FastAPI endpoints)
9. Frontend Integration (Streamlit requests)
10. RAG Debugging (inspecting chunks before blaming the LLM)

### Explain the project in 60 seconds (Pitch)
*"I built a Retrieval-Augmented Generation (RAG) system to solve the problem of LLMs hallucinating on private financial data. Analysts upload quarterly PDF reports, which the system chunks, vectorizes using OpenAI embeddings, and stores in a persistent ChromaDB database. When an analyst asks a question via the Streamlit frontend, the FastAPI backend performs a semantic search to retrieve the 4 most relevant text chunks. It then injects those chunks into a strict prompt for GPT-4o, forcing the model to answer only using the provided text. The final output provides the accurate answer alongside the exact source filename and page number for immediate verification. It successfully refuses to answer questions if the data isn't in the PDFs."*
