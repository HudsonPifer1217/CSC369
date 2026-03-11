# combineData_duckdb_safe.py
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "Data"
OUTPUT_CSV = BASE_DIR / "master_flights.csv"

def main():
    pattern = str(INPUT_DIR / "*.csv")
    con = duckdb.connect(database=":memory:")

    con.execute(f"""
        CREATE TABLE all_flights AS
        SELECT *
        FROM read_csv_auto('{pattern}',
                           union_by_name=true,
                           header=true,
                           sample_size=-1);
    """)

    print("Rows:", con.execute("SELECT COUNT(*) FROM all_flights").fetchone()[0])
    
    con.execute(f"COPY all_flights TO '{str(OUTPUT_CSV)}' (HEADER, DELIMITER ',');")
    print("Wrote:", OUTPUT_CSV.resolve())

if __name__ == "__main__":
    main()
