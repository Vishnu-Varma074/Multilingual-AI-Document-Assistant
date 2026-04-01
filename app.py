# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from rag import process_documents, get_llm, query_rag

load_dotenv()

st.set_page_config(page_title="DocuLens", layout="wide")
st.title("📚 DocuLens – Multilingual AI Document Assistant")
st.markdown("Upload PDFs/TXTs and ask questions in English, Hindi, Telugu, or any language.")

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("🔑 API Configuration")
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not groq_key:
        groq_key = st.text_input("Enter Groq API Key", type="password")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("API Key saved!")
    
    st.header("📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDFs or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )

    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing documents... This may take a minute."):
                try:
                    vectorstore, doc_map = process_documents(uploaded_files)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.doc_map = doc_map
                    st.session_state.processed_files = [f.name for f in uploaded_files]
                    st.success(f"✅ Successfully processed {len(uploaded_files)} document(s)!")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

# ------------------ MAIN AREA ------------------
if "vectorstore" in st.session_state:
    st.success("Documents are ready! Ask anything below.")

    # Document Selection
    doc_names = list(st.session_state.doc_map.keys())
    selected_docs = st.multiselect(
        "📄 Select specific documents (optional - leave empty for all)",
        options=doc_names,
        default=None,
        help="Leave empty to search across all uploaded documents"
    )

    # Query Input
    query = st.text_area(
        "💬 Enter your question or command",
        placeholder="Summarize the document... or Translate to Telugu... or What is mentioned about taxes?",
        height=100
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        submit = st.button("🚀 Submit Query", type="primary", use_container_width=True)

    if submit and query.strip():
        with st.spinner("Thinking..."):
            try:
                llm = get_llm()
                
                answer = query_rag(
                    vectorstore=st.session_state.vectorstore,
                    query=query,
                    llm=llm,
                    selected_docs=selected_docs if selected_docs else None
                )
                
                st.markdown("### 📝 Answer")
                st.markdown(answer)
                
                # Optional: Show sources (basic version)
                with st.expander("📚 View Retrieved Sources"):
                    # This is a simple placeholder - you can enhance it later
                    st.info("Source display coming in next improvement...")
                    
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
                st.info("Tip: Make sure your Groq API key is valid and has sufficient quota.")

else:
    st.info("👈 Please upload documents in the sidebar and click **Process Documents** to begin.")

# Footer
st.markdown("---")
st.caption("DocuLens | Powered by Groq + Llama 3.1 + LangChain | Supports English, हिंदी, తెలుగు & more")
