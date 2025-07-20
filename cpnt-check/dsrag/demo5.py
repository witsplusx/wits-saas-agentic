from dsrag.chat.chat import create_new_chat_thread
from dsrag.database.chat_thread.sqlite_db import SQLiteChatThreadDB

# Configure chat parameters
chat_params = {
    "kb_ids": ["my_knowledge_base"],  # List of knowledge base IDs to use
    "model": "gpt-4o",                 # LLM model to use
    "temperature": 0.2,               # Response creativity (0.0-1.0)
    "system_message": "You are a helpful assistant specialized in technical documentation",
    "target_output_length": "medium"  # "short", "medium", or "long"
}

# Initialize chat thread database (SQLite in this case)
chat_thread_db = SQLiteChatThreadDB()

# Create the thread
thread_id = create_new_chat_thread(chat_params, chat_thread_db)