import os
import streamlit as st
from dotenv import load_dotenv
from rag import process_documents, get_llm, query_rag, summarize_document

# ------------------- CONFIG -------------------
st.set_page_config(page_title="DocuLens", layout="wide")
st.title("DocuLens – Multilingual AI Document Assistant")

# ------------------- SIDEBAR -------------------
with st.sidebar:
    load_dotenv(override=True)
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        groq_key = st.text_input("Enter Groq API Key", type="password")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key

    uploaded_files = st.file_uploader(
        "Upload PDFs or TXT",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

# ------------------- PROCESS DOCUMENTS -------------------
if uploaded_files:
    if st.button("Process Documents"):
        vectorstore, doc_map = process_documents(uploaded_files)
        st.session_state.vectorstore = vectorstore
        st.session_state.doc_map = doc_map
        st.success("Documents processed successfully!")

# ------------------- DOC SELECTION -------------------
selected_docs = None
if "doc_map" in st.session_state:
    doc_names = list(st.session_state.doc_map.keys())
    selected_docs = st.multiselect("📄 Select Documents (leave empty for ALL)", doc_names)

# ------------------- QUERY -------------------
if "vectorstore" in st.session_state and os.getenv("GROQ_API_KEY"):
    query = st.text_input("Ask something")

    if st.button("Submit") and query:
        llm = get_llm()

        # Multi-document summary
        if "summarize" in query.lower():
            st.markdown("### 📝 Summaries")
            docs_to_use = selected_docs if selected_docs else st.session_state.doc_map.keys()
            for doc_name in docs_to_use:
                docs = st.session_state.doc_map[doc_name]
                summary = summarize_document(llm, docs)
                st.markdown(f"### 📄 {doc_name}")
                st.markdown(summary)

        else:
            answer = query_rag(st.session_state.vectorstore, query, llm, selected_docs)
            st.write(answer)
else:
    st.info("Upload documents and set API key.")
