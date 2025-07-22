import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import tempfile
from agents.coordinator_agent import CoordinatorAgent
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from vector_store.faiss_store import FaissStore
from mcp.message import MCPMessage

def get_pipeline():
    if 'vector_store' not in st.session_state:
        st.session_state['vector_store'] = FaissStore()
    if 'ingestion_agent' not in st.session_state:
        st.session_state['ingestion_agent'] = IngestionAgent(st.session_state['vector_store'])
    if 'retrieval_agent' not in st.session_state:
        st.session_state['retrieval_agent'] = RetrievalAgent(st.session_state['vector_store'])
    if 'llm_response_agent' not in st.session_state:
        st.session_state['llm_response_agent'] = LLMResponseAgent()
    if 'coordinator_agent' not in st.session_state:
        st.session_state['coordinator_agent'] = CoordinatorAgent(
            st.session_state['ingestion_agent'],
            st.session_state['retrieval_agent'],
            st.session_state['llm_response_agent']
        )
    return st.session_state['coordinator_agent']

def save_files(files):
    file_infos = []
    for file in files:
        suffix = os.path.splitext(file.name)[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            file_infos.append({
                'path': tmp.name,
                'type': suffix
            })
    return file_infos

def main():
    st.set_page_config(page_title="Agentic RAG Chatbot (MCP)")
    st.title("Agentic RAG Chatbot (MCP)")
    st.write("Upload documents and ask questions!")

    uploaded_files = st.file_uploader(
        "Upload documents (PDF, PPTX, CSV, DOCX, TXT, MD)",
        type=["pdf", "pptx", "csv", "docx", "txt", "md"],
        accept_multiple_files=True
    )

    query = st.text_input("Ask a question about your documents:")

    if st.button("Submit"):
        if not uploaded_files or not query:
            st.warning("Please upload at least one document and enter a question.")
        else:
            file_infos = save_files(uploaded_files)
            coordinator = get_pipeline()
            user_msg = MCPMessage(
                sender='UI',
                receiver='CoordinatorAgent',
                type_='USER_QUERY',
                payload={'files': file_infos, 'query': query}
            )
            with st.spinner("Processing..."):
                result = coordinator.handle_message(user_msg)
            st.subheader("Answer:")
            st.write(result['answer'])
            st.subheader("Source Chunks:")
            if result['sources']:
                for i, chunk in enumerate(result['sources']):
                    st.markdown(f"**Chunk {i+1}** (File: `{chunk.get('file_path', 'N/A')}` | Type: `{chunk.get('file_type', 'N/A')}` | Chunk ID: `{chunk.get('chunk_id', 'N/A')}`):")
                    st.markdown(f"""
```
{chunk['text']}
```
""")
            else:
                st.info("No relevant source chunks found.")

if __name__ == "__main__":
    main() 