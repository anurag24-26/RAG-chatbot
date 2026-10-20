import os

import streamlit as st
from dotenv import load_dotenv

from rag.chunker import build_chunks
from rag.llm import LLMError, ask
from rag.loader import DocumentError, load_file
from rag.store import VectorStore

load_dotenv()

st.set_page_config(page_title="Document Chat")
st.title("Document Chat")
st.caption("Ask questions about your PDF and TXT files. Answers come only from the documents.")

if "store" not in st.session_state:
    st.session_state.store = None
    st.session_state.messages = []
    st.session_state.summary = ""

has_key = bool(os.getenv("GROQ_API_KEY"))
if not has_key:
    st.error("GROQ_API_KEY not found. Copy .env.example to .env, add your key, and restart.")


def build_index(files, size, overlap):
    documents = {}
    for file in files:
        try:
            documents[file.name] = load_file(file)
        except DocumentError as exc:
            st.sidebar.error(str(exc))
    if not documents:
        return
    chunks = build_chunks(documents, size, overlap)
    with st.spinner("Embedding chunks. The first run downloads the embedding model."):
        st.session_state.store = VectorStore(chunks)
    st.session_state.messages = []
    st.session_state.summary = f"{len(documents)} file(s), {len(chunks)} chunks indexed"


with st.sidebar:
    st.header("Documents")
    files = st.file_uploader("Upload files", type=["pdf", "txt"], accept_multiple_files=True)
    size = st.slider("Chunk size (characters)", 300, 1500, 800, 100)
    overlap = st.slider("Chunk overlap (characters)", 0, 300, 150, 25)
    top_k = st.slider("Passages to retrieve", 1, 8, 4)
    if st.button("Process documents", disabled=not files, use_container_width=True):
        build_index(files, size, overlap)
    if st.session_state.summary:
        st.success(st.session_state.summary)


def show_sources(sources):
    with st.expander("Sources"):
        for number, hit in enumerate(sources, start=1):
            st.markdown(f"**[{number}] {hit['source']}**, page {hit['page']}, similarity {hit['score']:.2f}")
            snippet = hit["text"][:350] + ("..." if len(hit["text"]) > 350 else "")
            st.caption(snippet)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("sources"):
            show_sources(message["sources"])

if st.session_state.store is None:
    st.info("Upload a document and click Process documents to start.")
elif question := st.chat_input("Ask about your documents", disabled=not has_key):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            hits = st.session_state.store.search(question, top_k)
            with st.spinner("Thinking"):
                answer = ask(question, hits)
            st.write(answer)
            show_sources(hits)
            st.session_state.messages.append({"role": "assistant", "content": answer, "sources": hits})
        except LLMError as exc:
            st.error(str(exc))
