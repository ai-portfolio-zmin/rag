RAG Assistant 

This repository implements a production-oriented Retrieval-Augmented Generation (RAG) service that sits on top of an external hybrid search service (BM25 + embeddings + FAISS + cross-encoder reranking).

The goal of this project is to demonstrate real-world RAG architecture, not a notebook demo:

Search infrastructure is a separate service

RAG is an API layer that consumes search results over HTTP

The system is configurable, reproducible, and deployable

High-level Architecture
Client / UI
    │
    ▼
RAG API  (this repo)
POST /answer
    │  HTTP
    ▼
Hybrid Search API (external service)
BM25 + Embeddings + FAISS + Cross-Encoder

Key idea:

This repo does not build or store indexes

All retrieval happens via an external mixed-search service

This mirrors production systems 

Features

Corpus-aware RAG (fastapi, more can be added)

Hybrid retrieval (BM25 + semantic) via external API

Cross-encoder reranking (handled by search service)

Deterministic chunk-based context with citations

Config-driven pipelines per corpus

FastAPI-based HTTP API

Gemini (Google GenAI) as LLM backend

Project Structure
api/
  api.py                # FastAPI application


src/
  config.py             # Corpus configs + prompt templates
  pipeline.py           # RAG orchestration logic
  util.py               # Context formatting helpers


  retrieval/
    client.py           # HTTP client for hybrid-search
    schema.py           # RetrievedDoc model


  data/
    fastapi_data_pipeline.py  # Offline ingestion + chunking for FastAPI docs


data/
  ...                    # Local data (not indexed here)


.env                     # Environment variables (API keys)
requirements.txt



Data Flow

Offline ingestion (example: FastAPI docs)

Markdown → cleaned text

Chunked with overlap

Written as JSONL for search indexing


Hybrid search service (external)

Builds BM25 + embedding + FAISS indices

Applies cross-encoder reranking

Exposes /retrieve endpoint


RAG pipeline (this repo)

Calls hybrid-search over HTTP

Receives ranked chunks

Builds structured context with citations

Calls LLM

Returns answer + traceable sources

API
Health Check
GET /

Response:

{"status": "ok"}
Answer a Question
POST /answer

Request body:

{
  "corpus": "fastapi",
  "query": "How do I define a request body with Pydantic models?",
  "extra_instruction": ""
}

Response:

{
  "query": "...",
  "answer": "To define a request body with Pydantic models in FastAPI, you follow these steps:
1.  **Import `BaseModel`**: First, you need to import `BaseModel` from Pydantic [5].
    ```python
    from pydantic import BaseModel
    ```
2.  **Create your data model**: Next, you declare your data model as a Python class that inherits from `BaseModel`. You use standard Python types for all the attributes within this class [5].
    For example:
    ```python
    from pydantic import BaseModel
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None
    ```
3.  **Declare it in your path operation function**: Once you have your Pydantic model, you declare it as a parameter in your *path operation* function. FastAPI will automatically recognize that function parameters declared as Pydantic models should be taken from the request body [2], [3].
    FastAPI will recognize the Pydantic model and use it to validate the request body, providing all the benefits of Pydantic [2]. You can also declare path parameters, query parameters, and a request body all at the same time, and FastAPI will correctly identify where each piece of data comes from [3].
Sources: [2], [3], [5]",
  "contexts": [
    {...}
  ]
}

The contexts field enables full traceability and citation mapping.

Configuration

Corpus-specific configuration lives in src/config.py:

base_url – hybrid-search API URL

top_k – number of retrieved chunks

rerank – whether to request reranking

model – LLM model name

domain_instruction – corpus-specific prompt guidance

Adding a new corpus requires no pipeline changes — just config.


Environment Variables

Create a .env file:

GEMINI_API_KEY=your_api_key_here


Running Locally
1. Start the hybrid-search service

Make sure the external mixed-search API is running, for example:

http://localhost:8000/retrieve


2. Run the RAG API
uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload

Then open:

http://localhost:8002/docs


Design Principles

Separation of concerns: search ≠ reasoning

Corpus-agnostic RAG: all corpus logic is config-driven

Stateless API: no index ownership in RAG

Traceability: every answer maps back to chunks

Production realism: HTTP boundaries, not imports


Future Improvements

Structured evaluation harness

Request-level tracing and metrics

Docker + docker-compose deployment

Auth & rate limiting

Streaming responses


Why this project matters

This repo demonstrates how real RAG systems are built in practice, not just in tutorials:

Dedicated retrieval infrastructure

Clean API contracts

Deterministic chunking

Observability-friendly design

It’s intentionally simple — but architecturally correct.