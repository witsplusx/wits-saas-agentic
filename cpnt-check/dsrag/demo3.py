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

# Advanced query with filtering and parameters
results = kb.query(
    search_queries=[
        "什么是城市生命线安全工程？"
    ],
    # metadata_filter={
    #     "field": "doc_id",
    #     "operator": "equals",
    #     "value": "user_manual"
    # },
    # rse_params="precise", 
    rse_params={
        "max_length": 2,                # Max segments length (in number of chunks)
        "overall_max_length": 20,       # Total length limit across all segments (in number of chunks)
        "minimum_value": 0.5,           # Minimum relevance score
        "irrelevant_chunk_penalty": 0.2 # Penalty for irrelevant chunks in a segment - higher penalty leads to shorter segments
    } ,
    return_mode="text"     # Return text content
)

# Process results
for segment in results:
    print(f"""
      Document: {segment['doc_id']}
      Pages: {segment['segment_page_start']} - {segment['segment_page_end']}
      Content: {segment['content']}
      Relevance: {segment['score']}
    """)






