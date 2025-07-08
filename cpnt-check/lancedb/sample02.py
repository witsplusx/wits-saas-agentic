
# import lancedb
# import pandas as pd
# import pyarrow as pa

# uri = "datas/storage/lancedb/sample-lancedb"
# db = lancedb.connect(uri)

import lancedb
import pandas as pd
import pyarrow as pa

uri = "datas/storage/lancedb/sample01"
db = lancedb.connect(uri)

data = [
    {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
    {"vector": [5.9, 26.5], "item": "bar", "price": 20.0},
]

table = db.create_table("pd_table", data=data)

import duckdb

arrow_table = table.to_lance()

result = duckdb.query("SELECT * FROM arrow_table")

print(result.fetchall())

