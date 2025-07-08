import os
import openai
from lancedb.embeddings import get_registry


# db = lancedb.connect("/tmp/db")

# func = get_registry().get("openai").create(name="text-embedding-ada-002")
# model = get_registry().get("sentence-transformers").create(name="BAAI/bge-small-en-v1.5", device="cpu")
# model = get_registry().get("huggingface").create(name='facebook/bart-base')
# func = get_registry().get("ollama").create(name="nomic-embed-text")
# func = get_registry().get("openai").create(name="text-embedding-ada-002")

with open("datas/files/lease.txt", "r") as file:
    text_data = file.read()


# chunk

import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize
import re


def recursive_text_splitter(text, max_chunk_length=1000, overlap=100):
    """
    Helper function for chunking text recursively
    """
    # Initialize result
    result = []

    current_chunk_count = 0
    separator = ["\n", " "]
    _splits = re.split(f"({separator})", text)
    splits = [_splits[i] + _splits[i + 1] for i in range(1, len(_splits), 2)]

    for i in range(len(splits)):
        if current_chunk_count != 0:
            chunk = "".join(
                splits[
                    current_chunk_count
                    - overlap : current_chunk_count
                    + max_chunk_length
                ]
            )
        else:
            chunk = "".join(splits[0:max_chunk_length])

        if len(chunk) > 0:
            result.append("".join(chunk))
        current_chunk_count += max_chunk_length

    return result


chunks = recursive_text_splitter(text_data, max_chunk_length=100, overlap=10)
print("Number of Chunks: ", len(chunks))

# vector store
# Insert text chunks with their embeddings

import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector


embeddings = (
    get_registry().get("sentence-transformers").create(name="BAAI/bge-small-en-v1.5")
)


class Documents(LanceModel):
    vector: Vector(embeddings.ndims()) = embeddings.VectorField()
    text: str = embeddings.SourceField()


def prepare_data(chunks, embeddings):
    """
    Helper function to prepare data to insert in LanceDB
    """
    data = []
    for chunk, embed in zip(chunks, embeddings):
        temp = {}
        temp["text"] = chunk
        temp["vector"] = embed
        data.append(temp)
    return data


def lanceDBConnection(chunks):
    """
    LanceDB insertion
    """

    db = lancedb.connect("datas/storage/lancedb/demo_rag1")
    # data = prepare_data(chunks, embeddings)
    table = db.create_table("documents", schema=Documents, mode="overwrite")

    data = [{"text": s} for s in chunks]
    # ingest data in table
    table.add(data)
    return table


# create and add table in table
table = lanceDBConnection(chunks)

# Create a fts index before the hybrid search
table.create_fts_index("text", replace=True)

# Retriever
question = "What is issue date of lease?"

# FTS Search
# fts_result = table.search(question, query_type="fts").limit(5).to_list()
# print(fts_result)

# Retriever
# question = "What is issue date of lease?"

# # Vector Search
vs_result = table.search(question, query_type="vector").limit(10).to_list()
# print(vs_result)
vs_context = [r["text"] for r in vs_result]
# # print(vs_context)





# from lancedb.rerankers import LinearCombinationReranker

# reranker = LinearCombinationReranker(
#     weight=0.7
# )  # Weight = 0 Means pure Text Search (BM-25) and 1 means pure Sementic (Vector) Search
# question = "What is issue date of lease?"
# hs_result = (
#     table.search(
#         question,
#         query_type="hybrid",
#     )
#     .rerank(reranker=reranker)
#     .limit(5)
#     .to_list()
# )

# hs_context = [r["text"] for r in hs_result]
# print(hs_context)




# Context Prompt

base_prompt = """You are an AI assistant. Your task is to understand the user question, and provide an answer using the provided contexts. Every answer you generate should have citations in this pattern  "Answer [position].", for example: "Earth is round [1][2].," if it's relevant.

Your answers are correct, high-quality, and written by an domain expert. If the provided context does not contain the answer, simply state, "The provided context does not have the answer."

User question: {}

Contexts:
{}
"""


question = "What is issue date of lease?"
# Your prompt
prompt = f"{base_prompt.format(question, vs_context)}"
print(prompt)

from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(
    model='qwen3:8b', 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    think=False,
)
print(response['message']['content'])
# or access fields directly from the response object
# print(response.message.content)














