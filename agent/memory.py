from langchain.memory import ConversationBufferMemory

def get_memory():
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def save_message(role: str, content: str):
    memory.chat_memory.add_user_message(content) if role=="user" else memory.chat_memory.add_ai_message(content)

def get_history():
    return memory.load_memory_variables({})["chat_history"]
