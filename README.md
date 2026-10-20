# Document Chat (RAG)

A Retrieval-Augmented Generation (RAG) chatbot built with Python and Streamlit. Upload PDF or TXT documents and ask questions about their contents. Answers are generated using the GroqCloud API and retrieved document passages, with source references displayed for transparency.

## How It Works

1. **Load:** Extract text from PDF and TXT files. PDF page numbers are preserved for source attribution.
2. **Chunk:** Split extracted text into overlapping chunks, preferring paragraph and sentence boundaries.
3. **Embed:** Convert chunks into vector embeddings using `all-MiniLM-L6-v2`, running locally on the CPU.
4. **Index:** Store vectors in a FAISS `IndexFlatIP`. Normalized vectors make inner-product search equivalent to cosine similarity.
5. **Retrieve:** Embed the user's question and retrieve the top-k most similar passages.
6. **Generate:** Send the retrieved context and a constrained prompt to the configured GroqCloud model.
7. **Cite:** Display source files, page numbers, similarity scores, and text snippets alongside answers.

## Tech Stack

- Python
- Streamlit
- GroqCloud API
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- PyPDF

## Project Structure

```text
Document-Chat-RAG/
├── app.py              # Streamlit interface
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
└── rag/
    ├── loader.py       # PDF and TXT extraction
    ├── chunker.py      # Overlapping text splitter
    ├── store.py        # Embeddings and FAISS search
    └── llm.py          # Prompt construction and Groq API call
```

## Setup (Windows PowerShell)

### 1. Clone the repository

```powershell
git clone https://github.com/anurag24-26/RAG-chatbot.git
cd RAG-chatbot
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure your API key

Create your local environment file:

```powershell
Copy-Item .env.example .env
notepad .env
```

Add your GroqCloud API key using the variable name expected by your application. For example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get an API key from [GroqCloud Console](https://console.groq.com/).

**Never commit your `.env` file or publish your API key.**

### 5. Run the chatbot

```powershell
streamlit run app.py
```

Open the local URL printed in the terminal by Streamlit.

## Configuration

- **`GROQ_API_KEY`**: API key for authenticating with GroqCloud.
- **Model name:** Use the model configured in your application and supported by your GroqCloud account.
- **Chunk size and overlap:** Adjust how documents are split.
- **Top-k retrieval:** Control how many relevant passages are retrieved.

Rebuild the document index after changing chunking settings.

## Limitations

- Scanned PDFs without an extractable text layer are not supported unless OCR is added.
- Semantic search may miss exact identifiers, codes, or rare terms.
- The FAISS index is stored in memory and resets when the application restarts.
- Answers depend on the quality of the extracted text and retrieved passages. Source citations help users verify responses, but do not guarantee correctness.

## Future Improvements

- Persistent vector storage
- Hybrid semantic and keyword search
- OCR support for scanned PDFs
- Automated evaluation of retrieval and answer quality

## Author

**Anurag Tripathi**

GitHub: [anurag24-26](https://github.com/anurag24-26)
