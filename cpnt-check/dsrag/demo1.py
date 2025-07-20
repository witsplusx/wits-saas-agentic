
# from dsrag.create_kb import create_kb_from_file

# file_path = "dsRAG/tests/data/levels_of_agi.pdf"
# kb_id = "levels_of_agi"
# kb = create_kb_from_file(kb_id, file_path)


from dsrag.llm import OllamaAPI
from dsrag.embedding import OllamaEmbedding
from dsrag.reranker import NoReranker

from dsrag.knowledge_base import KnowledgeBase
from dsrag.create_kb import create_kb_from_file

llm = OllamaAPI(model='qwen3:14b')
reranker = NoReranker()
embed = OllamaEmbedding(model='qllama/bce-embedding-base_v1:latest', dimension=2048)

kb = KnowledgeBase(kb_id="levels_of_agi", 
                   reranker=reranker, 
                   auto_context_model=llm,
                   storage_directory="./datas/storage/dsrag/demo1",
                   embedding_model=embed,)

file_path = "./datas/dsrag/levels_of_agi.pdf"
kb.add_document(doc_id='levels_of_agi', file_path=file_path)


search_queries = ["What are the levels of AGI?", "What is the highest level of AGI?"]
results = kb.query(search_queries)
for segment in results:
    print(segment)

