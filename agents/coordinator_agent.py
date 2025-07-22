from mcp.message import MCPMessage

class CoordinatorAgent:
    def __init__(self, ingestion_agent, retrieval_agent, llm_response_agent):
        self.ingestion_agent = ingestion_agent
        self.retrieval_agent = retrieval_agent
        self.llm_response_agent = llm_response_agent
        self.last_answer = None

    def handle_message(self, message):
        if message.type == 'USER_QUERY':
            # Step 1: Ingest documents
            ingest_msg = MCPMessage(
                sender='CoordinatorAgent',
                receiver='IngestionAgent',
                type_='INGEST_REQUEST',
                payload={'files': message.payload.get('files', [])},
                trace_id=message.trace_id
            )
            ingest_result = self.ingestion_agent.handle_message(ingest_msg)
            # Step 2: Retrieve context
            retrieve_msg = MCPMessage(
                sender='CoordinatorAgent',
                receiver='RetrievalAgent',
                type_='RETRIEVE_REQUEST',
                payload={'query': message.payload['query']},
                trace_id=message.trace_id
            )
            retrieval_result = self.retrieval_agent.handle_message(retrieve_msg)
            # Step 3: LLM response
            llm_msg = MCPMessage(
                sender='CoordinatorAgent',
                receiver='LLMResponseAgent',
                type_='CONTEXT_RESPONSE',
                payload={
                    'top_chunks': retrieval_result['top_chunks'],
                    'query': message.payload['query']
                },
                trace_id=message.trace_id
            )
            answer = self.llm_response_agent.handle_message(llm_msg)
            self.last_answer = answer
            return answer
        elif message.type == 'ANSWER':
            self.last_answer = message.payload
            return message.payload
        else:
            raise ValueError(f'Unknown message type: {message.type}') 