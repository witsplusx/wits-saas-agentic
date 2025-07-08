
#   pip install lancedb pandas langchain langchain_openai langchain-community langchain_ollama pypdf openai cohere tiktoken sentence_transformers tantivy==0.20.1

def pretty_print(docs):
    for doc in docs:
        print(doc + "\n\n")


from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load $ABNB's financial report. This may take 1-2 minutes since the PDF is large
# sec_filing_pdf = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001559720/8a9ebed0-815a-469a-87eb-1767d21d8cec.pdf"

# Create your PDF loader
loader = PyPDFLoader('datas/files/airbnb01.pdf')
# loader = UnstructuredMarkdownLoader('datas/files/平凡的世界.md')

# Load the PDF document
documents = loader.load()

# Chunk the financial report
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
docs = text_splitter.split_documents(documents)


from langchain_community.vectorstores import LanceDB
# from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
import lancedb

embedding_function = OllamaEmbeddings(model='granite-embedding:278m')

db = lancedb.connect("datas/storage/lancedb/demo_rag2")

# Load the document into LanceDB
db = LanceDB.from_documents(docs, embedding_function, connection=db, mode="overwrite")

table = db._table
table.create_fts_index("text")

# print(table.to_pandas().head())

# str_query = "孙少平都有哪些亲属？"
str_query = "What are the specific factors contributing to Airbnb's increased operational expenses in the last fiscal year?"

query = embedding_function.embed_query(str_query)
# docs = table.search(query, query_type="vector").limit(5).to_pandas()["text"].to_list()

# docs = table.search(query_type="hybrid").vector(query).text(str_query).limit(5).to_pandas()["text"].to_list()

from lancedb.rerankers import ColbertReranker
reranker = ColbertReranker()
docs = table.search(query_type="hybrid").vector(query).text(str_query).limit(5).rerank(reranker).to_pandas()["text"].to_list()


pretty_print(docs)




