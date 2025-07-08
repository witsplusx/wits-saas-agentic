import lancedb

from lancedb.index import FTS

uri = "datas/storage/lancedb/sample01"
db = lancedb.connect(uri)

table = db.create_table(
    "my_table_fts",
    data=[
        {"vector": [3.1, 4.1], "text": "Frodo was a happy puppy"},
        {"vector": [5.9, 26.5], "text": "There are several kittens playing"},
    ],
)

# passing `use_tantivy=False` to use lance FTS index
# `use_tantivy=True` by default
table.create_fts_index("text", use_tantivy=False)
rst = table.search("puppy").limit(10).select(["text"]).to_list()
# [{'text': 'Frodo was a happy puppy', '_score': 0.6931471824645996}]
# ...

print(rst)


