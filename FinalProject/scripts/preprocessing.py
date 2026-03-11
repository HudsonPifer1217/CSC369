import duckdb as db
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

PATH = "master_flights.parquet"

con = db.connect()

head = con.execute(f"""
    SELECT *
    FROM read_parquet('{PATH}',
                       union_by_name=true,
                       header=true)
    LIMIT 10""")

row_count = con.execute(f"""
    SELECT COUNT(*)
    FROM read_parquet('{PATH}',
                       union_by_name=true,
                       header=true)
    """).fetchone()[0]

head2 = con.sql(f"""
    SELECT *
    FROM read_parquet('{PATH}', union_by_name=true, header=true)
    LIMIT 10
""")


"""
col_names = head2.df().columns
col_df = pd.DataFrame({"column_name": col_names})
pd.set_option('display.max_rows', None)
print(col_df)"""
print(f"Rows: {row_count}")


