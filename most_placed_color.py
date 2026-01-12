import csv
from datetime import datetime as dt
import time
from collections import Counter

'''
input start and end hours in format: YYYY-MM-DD HH
    must validate that end hour is after start hour

return most placed color in format: #FFFFFF
    and most placed pixel location in format: (x, y)

use time.perf_counter() to measure execution time

in md file (test_results_week_1.md) document ahow results with:
    A 1-hour timeframe.
    A 3-hour timeframe.
    A 6-hour timeframe.

For each time frame, include:
    - The start and end times used.
    - The number of miliseconds it took to compute the result.
    - The output: most place color and most place pixel location

'''

def most_placed_color(start_date: str, end_date: str):
    start_hour = dt.strptime(start_date, '%Y-%m-%d %H')
    end_hour = dt.strptime(end_date, '%Y-%m-%d %H')

    if end_hour <= start_hour:
        raise ValueError("End hour must be after start hour")

    color_count = Counter()
    pixel_count = Counter()
    
    start = time.perf_counter_ns()

    with open('2022_place_canvas_history.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        i = 0
        for row in reader:
            # Timestamp format: 2022-04-04 00:53:51.577 UTC
            # Slice first 19 chars to ignore milliseconds/timezone: 2022-04-04 00:53:51
            i += 1
            if i % 100 == 0:
                print(f"Processed {i} rows", flush=True)

            try:
                row_dt = dt.strptime(row[0][:19], '%Y-%m-%d %H:%M:%S')
                
                if start_hour <= row_dt < end_hour:
                    color_count[row[2]] += 1
                    pixel_count[row[3]] += 1
            except (ValueError, IndexError):
                continue

    end = time.perf_counter_ns()
    ms = (end - start) / 1_000_000
    
    return color_count.most_common(1)[0][0], pixel_count.most_common(1)[0][0], ms 


if __name__ == "__main__":
    start = '2022-04-01 12'
    end = '2022-04-01 18'
    color, pixel, duration = most_placed_color(start, end)
    print(f"From {start} to {end}:")
    print(f"Computation time: {duration:.2f} ms")
    print(f"Most placed color: {color}")
    print(f"Most placed pixel location: {pixel}")
    


