
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

kb = KnowledgeBase(kb_id="gscitysfy_ahsmxgc01", 
                   reranker=reranker, 
                   auto_context_model=llm,
                   storage_directory="./datas/storage/dsrag/gscitysfy_ahsmxgc01",
                   embedding_model=embed,
                   language="zh",)

file_path = "./datas/dsrag/002.pdf"
kb.add_document(doc_id='gscitysfy_ahsmxgc01', file_path=file_path)




search_queries = ["燃气专项的建设内容有哪些？"]
results = kb.query(search_queries)
# print(results)
# for segment in results:
#     print(segment['text'])
#     print('============================================================================================================')

print(results[0]['text'])

