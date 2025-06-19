
import sys
from llama_index.embeddings.modelscope.base import ModelScopeEmbedding

model = ModelScopeEmbedding(
    model_name="iic/nlp_gte_sentence-embedding_chinese-base",
    model_revision="master",
)

rsp = model.get_query_embedding("Hello, who are you?")
print(rsp)

rsp = model.get_text_embedding("Hello, who are you?")
print(rsp)

