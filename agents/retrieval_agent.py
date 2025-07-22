class RetrievalAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def handle_message(self, message):
        if message.type == 'RETRIEVE_REQUEST':
            query = message.payload['query']
            top_chunks = self.vector_store.query(query, top_k=5)
            return {'top_chunks': top_chunks}
        else:
            raise ValueError(f'Unknown message type: {message.type}') 