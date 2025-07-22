class LLMResponseAgent:
    def __init__(self, llm=None):
        self.llm = llm  # Placeholder for LLM API

    def handle_message(self, message):
        if message.type == 'CONTEXT_RESPONSE':
            context = '\n'.join([chunk['text'] for chunk in message.payload['top_chunks']])
            query = message.payload['query']
            # TODO: Replace with real LLM call
            answer = f"[MOCK ANSWER] Q: {query}\nA: ...based on context..."
            return {'answer': answer, 'sources': message.payload['top_chunks']}
        else:
            raise ValueError(f'Unknown message type: {message.type}') 