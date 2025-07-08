
# import lancedb
# import pandas as pd
# import pyarrow as pa

# uri = "datas/storage/lancedb/sample-lancedb"
# db = lancedb.connect(uri)

import lancedb
import pandas as pd
import pyarrow as pa

uri = "datas/storage/lancedb/sample-lancedb"
db = await lancedb.connect_async(uri)

data = [
    {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
    {"vector": [5.9, 26.5], "item": "bar", "price": 20.0},
]

tbl = await db.create_table("my_table_async", data=data)

# df = pd.DataFrame(
#     [
#         {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
#         {"vector": [5.9, 26.5], "item": "bar", "price": 20.0},
#     ]
# )

# tbl = await db.create_table("table_from_df_async", df)


# Option 1: Add a list of dicts to a table
data = [
    {"vector": [1.3, 1.4], "item": "fizz", "price": 100.0},
    {"vector": [9.5, 56.2], "item": "buzz", "price": 200.0},
]
await tbl.add(data)

# Option 2: Add a pandas DataFrame to a table
df = pd.DataFrame(data)
await tbl.add(data)









