import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain


def process_documents(files):
    """Load, split, and embed documents"""
    all_docs = []
    doc_map = {}
    temp_dir = tempfile.mkdtemp()

    for uploaded_file in files:
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        loader = PyPDFLoader(temp_path) if uploaded_file.name.endswith(".pdf") else TextLoader(temp_path)
        docs = loader.load()

        for d in docs:
            d.metadata["source"] = uploaded_file.name

        doc_map[uploaded_file.name] = docs
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    splits = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)

    return vectorstore, doc_map


def get_prompt_template():
    """Return the ChatPromptTemplate"""
    return ChatPromptTemplate.from_template("""
Answer ONLY from context.
If not found say: I don't have enough information in the provided documents.
Context:
{context}
Question:
{input}
Answer:
""")


def get_llm():
    """Return ChatGroq LLM instance"""
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0)


def create_filtered_retriever(vectorstore, selected_docs=None, k=5):
    """Return a filtered retriever if selected_docs is provided"""
    if selected_docs:
        return vectorstore.as_retriever(search_kwargs={"k": k, "filter": {"source": {"$in": selected_docs}}})
    return vectorstore.as_retriever(search_kwargs={"k": k})


def query_rag(vectorstore, query, llm, selected_docs=None):
    """Query RAG using retrieval chain"""
    retriever = create_filtered_retriever(vectorstore, selected_docs)
    chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, get_prompt_template()))
    response = chain.invoke({"input": query})
    return response["answer"]


def summarize_document(llm, docs):
    """Summarize full document content in Telugu (example)"""
    full_text = "\n".join([d.page_content for d in docs])
    return llm.invoke(f"""
Summarize this document in Telugu in 3 lines:

Content:
{full_text}
""").content