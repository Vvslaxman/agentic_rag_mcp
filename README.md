# 🤖 Agentic RAG MCP Bot

A modular, agent-based **Retrieval-Augmented Generation (RAG)** chatbot that supports multi-format document question answering using a custom **Model Context Protocol (MCP)** for structured agent communication.

---

## 🚀 Overview

This project demonstrates an end-to-end AI assistant that:
- Accepts documents in diverse formats (PDF, PPTX, CSV, DOCX, TXT, MD)
- Uses semantic search over document embeddings
- Generates answers to user queries using context-aware prompting
- Implements **agent-based orchestration** (Ingestion, Retrieval, LLMResponse, Coordinator)
- Communicates between agents using an in-memory **Model Context Protocol (MCP)**

---

## ✅ Features

- 📄 Upload multiple document formats
- 🧠 SentenceTransformer embeddings (`all-MiniLM-L6-v2`)
- 🔍 FAISS vector store for semantic retrieval
- 🗂️ Modular Python agent design
- 🔁 Traceable message passing between agents using `trace_id`
- 🌐 Streamlit frontend for uploads, chat, and results

---

## 📦 Installation

```bash
git clone https://github.com/your-username/agentic_rag_mcp_bot.git
cd agentic_rag_mcp_bot
pip install -r requirements.txt

```
## 🧪 Usage
``` bash
streamlit run ui/app.py
```

Once running, you can:

- Upload documents (PDF, PPTX, CSV, DOCX, TXT, MD)

- Ask multi-turn questions

- View answers along with source context

## 🗂️ Project Structure

```agentic_rag_mcp_bot/
├── agents/              # Core agent implementations
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   ├── llm_response_agent.py
│   └── coordinator_agent.py
├── utils/               # Helpers for parsing, chunking, embedding
│   ├── parser_utils.py
│   ├── chunking.py
│   └── embedding_utils.py
├── vector_store/        # FAISS wrapper
│   └── faiss_store.py
├── mcp/                 # Model Context Protocol definitions
│   └── mcp_protocol.py
├── ui/                  # Streamlit user interface
│   └── app.py
├── static/              # Uploaded document storage
├── main.py              # Optional runner for backend-only mode
├── requirements.txt
├── README.md
└── ppt/
    └── Agentic_RAG_Chatbot_Presentation.pptx


```

## 🔁 Architecture (Agentic Flow)

1. **User uploads documents and asks a question**
2. **CoordinatorAgent** orchestrates the flow:
    - ➡️ **IngestionAgent** parses, chunks, and embeds docs into the vector store
    - ➡️ **RetrievalAgent** fetches top-k relevant chunks from FAISS
    - ➡️ **LLMResponseAgent** forms a prompt with context and generates an answer

3. Agents communicate using structured MCP messages like:

```json
{
  "type": "RETRIEVE_REQUEST",
  "sender": "CoordinatorAgent",
  "receiver": "RetrievalAgent",
  "trace_id": "abc-123",
  "payload": { "query": "What are the KPIs?" }
}

## 🧩 Tech Stack

| Layer         | Tools & Libraries                                      |
|---------------|--------------------------------------------------------|
| **UI**        | Streamlit                                              |
| **Parsing**   | PyMuPDF, python-docx, pandas, python-pptx, markdown    |
| **Embeddings**| SentenceTransformers (`all-MiniLM-L6-v2`)              |
| **Vector Store** | FAISS                                               |
| **LLM**       | OpenAI GPT / HuggingFace (mock fallback)               |
| **Messaging** | Custom MCP (JSON-based, in-memory protocol)            |

---

## ⚠️ Challenges

- Parsing noisy PPTX/CSV/table-heavy files
- Designing reusable chunking logic for multiple formats
- Balancing agent modularity vs. traceable execution
- Defining consistent MCP JSON schema for message passing

---

## 🔭 Future Scope

- Implement Redis or Kafka for asynchronous MCP message passing
- Stream LLM responses token-by-token (real-time UI updates)
- Integrate long-term memory and multi-turn dialogue support
- Add image/audio/document agents for broader multimodal input
