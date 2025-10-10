import lancedb
import pandas as pd
import numpy as np
import pyarrow as pa
import os

uri = "./data/sample-lancedb"
db = lancedb.connect(uri)

if __name__ == '__main__':
    data = [
        {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
        {"vector": [5.9, 26.5], "item": "bar", "price": 20.0},
    ]

    tbl = db.create_table("my_table", data=data)

    print(db.table_names())



