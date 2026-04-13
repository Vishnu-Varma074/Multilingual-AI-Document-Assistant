# """
# DocuLens – FastAPI Backend
# Multilingual AI Document Assistant powered by Groq + LangChain
# """

# import os
# import uuid
# import uvicorn
# import shutil
# from typing import Optional, List
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends, Form
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# from rag import process_documents, get_llm, query_rag


# sessions: dict = {}
# UPLOAD_DIR = "tmp_uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # ---------------------------------------------------------------------------
# # Streamlit-compatible file wrapper
# # ---------------------------------------------------------------------------
# class NamedFile:
#     def __init__(self, fpath: str, fname: str):
#         self.name = fname
#         self._path = fpath

#     def getbuffer(self) -> bytes:
#         with open(self._path, "rb") as f:
#             return f.read()

#     def read(self, *args) -> bytes:
#         with open(self._path, "rb") as f:
#             return f.read(*args)

#     def close(self):
#         pass


# # ---------------------------------------------------------------------------
# # Lifespan
# # ---------------------------------------------------------------------------
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     if os.path.exists(UPLOAD_DIR):
#         shutil.rmtree(UPLOAD_DIR)


# # ---------------------------------------------------------------------------
# # App
# # ---------------------------------------------------------------------------
# app = FastAPI(
#     title="DocuLens API",
#     description="Multilingual AI Document Assistant – Groq + Llama 3.1 + LangChain",
#     version="1.0.0",
#     lifespan=lifespan,
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ---------------------------------------------------------------------------
# # Helpers / Dependencies
# # ---------------------------------------------------------------------------
# def get_groq_key(x_groq_api_key: Optional[str] = Header(default=None)) -> str:
#     key = x_groq_api_key or os.getenv("GROQ_API_KEY")
#     if not key:
#         raise HTTPException(
#             status_code=401,
#             detail="Groq API key is required. Pass it via X-Groq-Api-Key header or set GROQ_API_KEY env var.",
#         )
#     os.environ["GROQ_API_KEY"] = key
#     return key


# def get_session(session_id: str) -> dict:
#     if session_id not in sessions:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Session '{session_id}' not found. Please upload and process documents first.",
#         )
#     return sessions[session_id]


# # ---------------------------------------------------------------------------
# # Schemas
# # ---------------------------------------------------------------------------
# class QueryRequest(BaseModel):
#     session_id: str
#     query: str
#     selected_docs: Optional[List[str]] = None

# class QueryResponse(BaseModel):
#     session_id: str
#     query: str
#     answer: str

# class ProcessResponse(BaseModel):
#     session_id: str
#     processed_files: List[str]
#     available_docs: List[str]
#     message: str

# class SessionInfoResponse(BaseModel):
#     session_id: str
#     available_docs: List[str]


# # ---------------------------------------------------------------------------
# # Routes
# # ---------------------------------------------------------------------------

# @app.get("/", tags=["Health"])
# async def root():
#     return {"status": "ok", "app": "DocuLens API"}


# @app.get("/health", tags=["Health"])
# async def health():
#     return {"status": "healthy"}


# @app.post(
#     "/documents/process",
#     response_model=ProcessResponse,
#     tags=["Documents"],
#     summary="Upload and process PDF/TXT documents",
# )
# async def process_documents_endpoint(
#     files: List[UploadFile] = File(...),
#     _key: str = Depends(get_groq_key),
# ):
#     session_id = str(uuid.uuid4())
#     session_tmp = os.path.join(UPLOAD_DIR, session_id)
#     os.makedirs(session_tmp, exist_ok=True)

#     saved_paths: List[str] = []
#     file_names: List[str] = []

#     try:
#         for upload in files:
#             dest = os.path.join(session_tmp, upload.filename)
#             with open(dest, "wb") as f:
#                 content = await upload.read()
#                 f.write(content)
#             saved_paths.append(dest)
#             file_names.append(upload.filename)

#         file_objects = [NamedFile(p, n) for p, n in zip(saved_paths, file_names)]
#         vectorstore, doc_map = process_documents(file_objects)

#         sessions[session_id] = {
#             "vectorstore": vectorstore,
#             "doc_map": doc_map,
#         }

#         return ProcessResponse(
#             session_id=session_id,
#             processed_files=file_names,
#             available_docs=list(doc_map.keys()),
#             message=f"Successfully processed {len(file_names)} document(s).",
#         )

#     except HTTPException:
#         raise
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Error processing documents: {str(exc)}")


# @app.get(
#     "/sessions/{session_id}",
#     response_model=SessionInfoResponse,
#     tags=["Sessions"],
#     summary="Get info about a session",
# )
# async def get_session_info(session_id: str):
#     session = get_session(session_id)
#     return SessionInfoResponse(
#         session_id=session_id,
#         available_docs=list(session["doc_map"].keys()),
#     )


# @app.delete(
#     "/sessions/{session_id}",
#     tags=["Sessions"],
#     summary="Delete a session and free memory",
# )
# async def delete_session(session_id: str):
#     if session_id not in sessions:
#         raise HTTPException(status_code=404, detail="Session not found.")
#     del sessions[session_id]

#     session_tmp = os.path.join(UPLOAD_DIR, session_id)
#     if os.path.exists(session_tmp):
#         shutil.rmtree(session_tmp)

#     return {"message": f"Session '{session_id}' deleted successfully."}


# @app.post(
#     "/query",
#     response_model=QueryResponse,
#     tags=["Query"],
#     summary="Ask a question against uploaded documents",
# )
# async def query_endpoint(
#     body: QueryRequest,
#     _key: str = Depends(get_groq_key),
# ):
#     if not body.query.strip():
#         raise HTTPException(status_code=400, detail="Query must not be empty.")

#     session = get_session(body.session_id)

#     if body.selected_docs:
#         available = set(session["doc_map"].keys())
#         invalid = set(body.selected_docs) - available
#         if invalid:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Unknown document(s): {list(invalid)}. Available: {list(available)}",
#             )

#     try:
#         llm = get_llm()
#         answer = query_rag(
#             vectorstore=session["vectorstore"],
#             query=body.query,
#             llm=llm,
#             selected_docs=body.selected_docs or None,
#         )
#         return QueryResponse(
#             session_id=body.session_id,
#             query=body.query,
#             answer=answer,
#         )
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Error generating answer: {str(exc)}")


# # ---------------------------------------------------------------------------
# # Entry point
# # ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run("main:app", host="0.0.0.0", port=port)

import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
