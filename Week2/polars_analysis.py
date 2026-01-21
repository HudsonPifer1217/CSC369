import polars as pl
import time
from datetime import datetime as dt
from collections import Counter
import pyarrow.parquet as pq
import argparse

def most_placed_color(start_date: str, end_date: str, path: str = "2022_place_canvas_history.parquet"):

    color_counts = {}
    coord_counts = {}

    try:
        start = dt.strptime(start_date, "%Y-%m-%d %H")
        end = dt.strptime(end_date, "%Y-%m-%d %H")
    except ValueError as e:
        raise ValueError("Dates must be in format 'YYYY-MM-DD HH' (example: '2022-04-04 12').") from e
    
    if end <= start:
        raise ValueError("End hour must be after start hour.")
    
    t0 = time.perf_counter_ns()

    window = (
        pl.scan_parquet(path)
        .select(["timestamp", "pixel_color", "coordinate"]) 
        .filter((pl.col("timestamp") >= pl.lit(start)) & (pl.col("timestamp") < pl.lit(end)))
    )

    top_color_df = (
        window
        .group_by("pixel_color")
        .len()
        .sort("len", descending=True)
        .select("pixel_color")
        .collect(engine="streaming")
    )

    top_pixel_df= (
        window
        .group_by("coordinate")
        .len()
        .sort("len", descending=True)
        .select("coordinate")
        .collect(engine="streaming")
    )

    top_color = top_color_df.item(0,0)
    top_pixel = top_pixel_df.item(0,0)


    t1 = time.perf_counter_ns()
    ms = (t1 - t0) // 1_000_000
    return top_color, top_pixel, ms

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






