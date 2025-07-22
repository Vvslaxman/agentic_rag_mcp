from utils.doc_parsers import parse_document
from utils.chunking import chunk_text

class IngestionAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def handle_message(self, message):
        if message.type == 'INGEST_REQUEST':
            files = message.payload.get('files', [])
            all_chunks = []
            all_metadatas = []
            for file_info in files:
                file_path = file_info['path']
                file_type = file_info.get('type')
                doc = parse_document(file_path, file_type)
                chunks = chunk_text(doc['text'])
                for chunk in chunks:
                    meta = {
                        'chunk_id': chunk['chunk_id'],
                        'file_path': file_path,
                        'file_type': file_type,
                        'text': chunk['text']
                    }
                    all_chunks.append(chunk['text'])
                    all_metadatas.append(meta)
            if all_chunks:
                self.vector_store.add_embeddings(all_chunks, all_metadatas)
            return {'status': 'success', 'num_chunks': len(all_chunks)}
        else:
            raise ValueError(f'Unknown message type: {message.type}') 