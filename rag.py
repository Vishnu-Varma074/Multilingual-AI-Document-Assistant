import os
import tempfile
import re
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

# ------------------ LAZY EMBEDDINGS ------------------
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("Loading embedding model...")
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("Embedding model loaded.")
    return _embeddings


# ------------------ DOCUMENT PROCESSING ------------------
def process_documents(files):
    all_docs = []
    doc_map = {}

    temp_dir = tempfile.mkdtemp()

    for uploaded_file in files:
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.name.lower().endswith(".pdf"):
            loader = PyPDFLoader(temp_path)
        else:
            loader = TextLoader(temp_path, encoding="utf-8")

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = uploaded_file.name

        doc_map[uploaded_file.name] = docs
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    splits = splitter.split_documents(all_docs)

    vectorstore = FAISS.from_documents(splits, get_embeddings())  # lazy load

    return vectorstore, doc_map


# ------------------ LLM ------------------
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=1200
    )


# ------------------ PROMPT ------------------
def get_prompt_auto(query: str):
    query_lower = query.lower()

    translate_match = re.search(r'translate.*?(?:to|into)\s+([a-zA-Z]+)', query_lower)
    target_lang = None
    if translate_match:
        target_lang = translate_match.group(1).capitalize()

    if target_lang:
        if any(word in query_lower for word in ["section", "paragraph", "part", "about", "definition of", "the word", "the sentence", "following"]):
            template = f"""
The user wants to translate a **specific section, paragraph, word or sentence** from the document into **{target_lang}**.

First, identify the most relevant part(s) from the provided context that match the user's request.
Then, translate **only that specific part** clearly and naturally into {target_lang}.
Keep the original meaning and tone. Do not translate the entire document unless specifically asked.

Context:
{{context}}

User Request: {{input}}

Translation of the requested section:
"""
        else:
            template = f"""
Translate the relevant content from the document into clear and natural **{target_lang}**.

Context:
{{context}}

User Request: {{input}}

Translation:
"""
    elif "summarize" in query_lower or "summary" in query_lower:
        template = """
You are an expert summarizer. Provide a concise and clear summary.

Document:
{context}

Summary:
"""
    else:
        template = """
Answer the question based only on the provided document. Be clear, concise and accurate.

Document:
{context}

Question: {input}
Answer:
"""

    return ChatPromptTemplate.from_template(template)


# ------------------ QUERY RAG ------------------
def query_rag(vectorstore, query: str, llm, selected_docs=None):
    search_kwargs = {"k": 8}
    if selected_docs and len(selected_docs) > 0:
        search_kwargs["filter"] = {"source": {"$in": selected_docs}}

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    prompt = get_prompt_auto(query)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": query})

    return response["answer"]
