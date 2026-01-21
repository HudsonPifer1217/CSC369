import duckdb as dd
import pandas as pd
import time
from datetime import datetime as dt
from collections import Counter
import pyarrow.parquet as pq
import argparse

def most_placed_color(start_date: str, end_date: str, path: str = '2022_place_canvas_history.parquet'):
        color_counter = {}
        pixel_counter = {}

        try:
            start = dt.strptime(start_date, "%Y-%m-%d %H")
            end = dt.strptime(end_date, "%Y-%m-%d %H")
        except ValueError as e:
            raise ValueError("Dates must be in format 'YYYY-MM-DD HH' (example: '2022-04-04 12').") from e

        if end <= start:
            raise ValueError("End hour must be after start hour")
    
        con = dd.connect()

        t0 = time.perf_counter_ns()

        query = f"""
        WITH windowed AS (
            SELECT pixel_color AS color, coordinate AS pixel
            FROM '{path}'
            WHERE timestamp >= ? AND timestamp < ?
            ),
        top_color AS (
            SELECT color, COUNT(*) AS cS
            FROM windowed
            GROUP BY color
            ORDER BY cS DESC
            LIMIT 1
        ),
        top_coordinate AS (
            SELECT pixel, COUNT(*) AS cP
            FROM windowed
            GROUP BY pixel
            ORDER BY cP DESC
            LIMIT 1
        )
        SELECT 
            (SELECT color FROM top_color) AS most_color,
            (SELECT pixel FROM top_coordinate) AS most_pixel
        """

        row = con.execute(query, [start, end]).fetchone()

        t1 = time.perf_counter_ns()
        ms = (t1 - t0) // 1_000_000

        most_color, most_pixel = row[0], row[1]
        return most_color, most_pixel, ms

def main():
    parser = argparse.ArgumentParser(description="Find most placed color and pixel location in a given time frame.")
    parser.add_argument("start_date", type=str, help="Start date in format 'YYYY-MM-DD HH'")
    parser.add_argument("end_date", type=str, help="End date in format 'YYYY-MM-DD HH'")
    parser.add_argument("--path", type=str, default="2022_place_canvas_history.parquet", help="Path to the Parquet file")
    args = parser.parse_args()

    color, pixel, ms = most_placed_color(args.start_date, args.end_date, args.path)
    print(color)
    print(pixel)
    print(f"{ms:.3f} ms")


if __name__ == "__main__":
     main()

