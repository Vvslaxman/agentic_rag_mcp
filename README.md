# Agentic RAG MCP Bot

## Overview
A Retrieval-Augmented Generation (RAG) chatbot with agent-based architecture and Model Context Protocol (MCP) for multi-format document QA.

## Features
- Multi-format document upload (PDF, PPTX, CSV, DOCX, TXT/MD)
- Modular agentic design (Ingestion, Retrieval, LLM Response, Coordinator)
- MCP-based agent communication
- Embeddings + FAISS vector store
- Streamlit UI

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run ui/app.py
```

## Project Structure
- `agents/`: Agent classes
- `mcp/`: MCP message protocol
- `vector_store/`: Embedding and vector DB
- `utils/`: Document parsing and chunking
- `ui/`: Streamlit app

## Architecture
See `architecture_pptx_content.txt` for slides content. 