import pandas as pd
from datetime import datetime as dt
import time
from collections import Counter
import pyarrow.parquet as pq
import argparse



def most_placed_color(start_date: str, end_date: str, path: str = "2022_place_canvas_history.parquet"):
    
    color_counts = {}
    coord_counts = {}

    try:
        start = pd.to_datetime(start_date, format="%Y-%m-%d %H", utc=True)
        end = pd.to_datetime(end_date, format="%Y-%m-%d %H", utc=True)
    except ValueError as e:
        raise ValueError(
            "Start/end must be in format 'YYYY-MM-DD HH' (example: '2022-04-04 00')."
        ) from e
    
    if end <= start:
        raise ValueError("End hour must be after start hour.")

    t0 = time.perf_counter_ns()

    pf = pq.ParquetFile(path)

    for rowGroup in range(pf.num_row_groups):
        table = pf.read_row_group(rowGroup, columns=["timestamp", "pixel_color", "coordinate"])
        df_chunk = table.to_pandas()
        df_chunk["timestamp"] = pd.to_datetime(df_chunk["timestamp"], utc=True, errors="coerce")
        
        df_chunk = df_chunk[(df_chunk["timestamp"] >= start) & (df_chunk["timestamp"] < end)]
        
        
        for color in df_chunk["pixel_color"].dropna():
            color_counts[color] = color_counts.get(color, 0) + 1

        for coord in df_chunk["coordinate"].dropna():
            coord_counts[coord] = coord_counts.get(coord, 0) + 1    

    if not color_counts:
        raise ValueError("No placements found in the given time range.")

    most_color = max(color_counts, key=color_counts.get)
    most_pixel = max(coord_counts, key=coord_counts.get)

    t1 = time.perf_counter_ns()
    ms = (t1 - t0) // 1_000_000  
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

                   