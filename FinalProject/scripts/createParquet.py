import duckdb as db
import time

con = db.connect()

PATH = "master_flights.csv"

start = time.time()

con.execute(f"""
    COPY (
        SELECT *
        FROM read_csv_auto('{PATH}', union_by_name=true, header=true)
    )
    TO 'master_flights.parquet'
    (FORMAT PARQUET);
""")

end = time.time()

print(f"Conversion completed in {end - start:.2f} seconds")
