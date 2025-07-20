import logging
import sys

# Set up a detailed formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d'
)

# Create a handler for console output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Configure the dsrag logger
logger = logging.getLogger("dsrag")
logger.setLevel(logging.DEBUG)

# Clear existing handlers and add our handler
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(console_handler)



from dsrag.llm import OllamaAPI
from dsrag.embedding import OllamaEmbedding
from dsrag.reranker import NoReranker

from dsrag.knowledge_base import KnowledgeBase

llm = OllamaAPI(model='qwen3:14b')
reranker = NoReranker()
embed = OllamaEmbedding(model='qllama/bce-embedding-base_v1:latest', dimension=2048)

kb = KnowledgeBase(kb_id="citylifeline", 
  reranker=reranker, 
  auto_context_model=llm,
  storage_directory="./datas/storage/dsrag/citylifeline",
  embedding_model=embed,
  language="zh",)

kb.add_document(
    doc_id='cityll_ahs_1q',
    file_path='./datas/dsrag/cityll_ahs_1q.pdf',
    document_title='安徽省城市生命线安全工程一期建设指南',
    auto_context_config={
        "use_generated_title": True,    # Generate title if not provided
        "get_document_summary": True,   # Generate document summary
        "llm_max_concurrent_requests": 5  # Maximum concurrent requests
    },
    semantic_sectioning_config={
        "use_semantic_sectioning": True
    },
)

kb.add_document(
    doc_id='cityll_ahs_2q',
    file_path='./datas/dsrag/cityll_ahs_2q.pdf',
    document_title='安徽省城市生命线安全工程二期建设指南',
    auto_context_config={
        "use_generated_title": True,    # Generate title if not provided
        "get_document_summary": True,   # Generate document summary
        "llm_max_concurrent_requests": 5  # Maximum concurrent requests
    },
    semantic_sectioning_config={
        "use_semantic_sectioning": True
    },
)

from dsrag.chat.chat import get_chat_thread_response
from dsrag.chat.chat_types import ChatResponseInput
from dsrag.database.chat_thread.sqlite_db import SQLiteChatThreadDB


# Initialize database and get response
chat_thread_db = SQLiteChatThreadDB()
response = get_chat_thread_response(
    thread_id='test001',
    get_response_input=ChatResponseInput(
        user_input="什么是城市生命线安全工程?"
    ),
    chat_thread_db=chat_thread_db,
    knowledge_bases=kb
)

# Access citations
citations = response["model_response"]["citations"]
for citation in citations:
    print(f"""
Source: {citation['doc_id']}
Page: {citation['page_number']}
Text: {citation['cited_text']}
Knowledge Base: {citation['kb_id']}
""")





