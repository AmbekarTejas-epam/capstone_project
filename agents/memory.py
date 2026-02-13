from langchain.memory import ConversationBufferMemory


class AgentMemory:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def get(self):
        return self.memory
