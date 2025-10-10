import lancedb

db = lancedb.connect(
  uri="db://rubik-auekyd",
  api_key="",
  region="us-east-1"
)

if __name__ == '__main__':
    data = [
        {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
        {"vector": [5.9, 26.5], "item": "bar", "price": 20.0},
    ]
    # Replace the table name with your table name.
    table_name = "my_table1"
    tbl = db.create_table(table_name, data=data)

