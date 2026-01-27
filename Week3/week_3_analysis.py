import duckdb as dd
import time
from datetime import datetime as dt
from collections import Counter
import pyarrow.parquet as pq
import numpy as np
import argparse

COLOR_MAP = {"#000000": "black", "#00756F": "dark teal", "#009EAA": "teal", "#00A368": "dark green", "#00CC78": "green", "#00CCC0": "light teal",
"#2450A4": "dark blue", "#3690EA": "blue", "#51E9F4": "light blue", "#94B3FF": "pale blue", "#493AC1": "indigo", "#6A5CFF": "violet",
"#811E9F": "dark purple", "#B44AC0": "magenta", "#E4ABFF": "lavender", "#FF3881": "pink", "#DE107F": "dark pink", "#FF4500": "orange red",
"#BE0039": "dark red","#6D001A": "maroon", "#FFA800": "orange", "#FFB470": "peach", "#FFD635": "yellow", "#FFF8B8": "light yellow",
"#9C6926": "brown", "#6D482F": "dark brown", "#515252": "dark gray", "#898D90": "gray", "#D4D7D9": "light gray", "#FFFFFF": "white",
"#FF99AA": "light pink", "#7EED56": "ligt green"
}


def function(start_date: str, end_date: str, path: str = '2022_place_canvas_history.parquet'):

       try:
              start = dt.strptime(start_date, "%Y-%m-%d %H")
              end = dt.strptime(end_date, "%Y-%m-%d %H")
       except ValueError as e:
              raise ValueError("Dates must be in format 'YYYY-MM-DD HH' (example: '2022-04-04 12').") from e

       if end <= start:
              raise ValueError("End hour must be after start hour")
    
       con = dd.connect()

       t0 = time.perf_counter_ns()

       rows_color = con.execute(
              f"""
              SELECT pixel_color, COUNT(DISTINCT user_id) AS distint_users
              FROM read_parquet('{path}')
              WHERE timestamp >= ? AND timestamp < ?
              GROUP BY pixel_color
              ORDER BY distint_users DESC, pixel_color ASC
              """,
              [start, end]
       ).fetchall()

       ranking = [(COLOR_MAP.get(code, "UNKNOWN"), code, n_users)
              for (code, n_users) in rows_color]

       avg_seesion_length = con.execute(
              f"""
              WITH events AS (
                     SELECT user_id, CAST(timestamp AS TIMESTAMP) AS ts
              FROM read_parquet('{path}')
              WHERE timestamp >= ? AND timestamp < ?
              ),

              WITH_PREV AS (
              SELECT
                     user_id,
                     ts,
                     LAG(TS) OVER (PARTITION BY user_id ORDER BY ts) AS prev_ts
              FROM events
              ),
              
              with_gaps AS (
              SELECT
                     user_id,
                     ts,
                     prev_ts,
                     CASE
                            WHEN prev_ts IS NULL THEN NULL
                            ELSE DATEDIFF('second', prev_ts, ts)
                     END AS gap_seconds
              FROM with_prev
              ), 

              flagged AS (
              SELECT
                     user_id,
                     ts,
                     CASE
                            WHEN prev_ts IS NULL THEN 1
                            WHEN gap_seconds > 900 THEN 1
                            ELSE 0
                     END AS start_of_session
              FROM with_gaps
              ),

              sessions AS (
              SELECT
                     user_id,
                     ts,
                     SUM(start_of_session) OVER (
                     PARTITION BY user_id 
                     ORDER BY ts
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                     ) AS session_id
              FROM flagged
              ),

              session_stats AS(
              SELECT
                     user_id,
                     session_id,
                     COUNT(*) AS n_events,
                     DATEDIFF('second', MIN(ts), MAX(ts)) AS session_length_seconds
              FROM sessions
              GROUP BY user_id, session_id
              )

              SELECT AVG(session_length_seconds)
              FROM session_stats
              WHERE n_events > 1
              """,
              [start, end]
       ).fetchone()[0]

       
       user_counts_rows = con.execute(
              f"""
              SELECT user_id, COUNT(*) AS pixels
              FROM read_parquet('{path}')
              WHERE timestamp >= ? AND timestamp < ?
              GROUP BY user_id
              """,
              [start, end]
       ).fetchall()
       counts = [r[1] for r in user_counts_rows]
       if counts: 
              p50, p75, p90, p99 = np.percentile(counts, [50, 75, 90, 99]).tolist()
       
       else: 
              p50, p75, p90, p99 = 0, 0, 0, 0
       
       first_time_count = con.execute(
              f"""
              WITH first_times AS (
                     SELECT user_id, MIN(timestamp) AS first_time
                     FROM read_parquet('{path}')
                     GROUP BY user_id
              )
              SELECT COUNT(*)
              FROM first_times
              WHERE first_time >= ? AND first_time < ?
              """,
              [start, end]
       ).fetchone()[0]

       t1 = time.perf_counter_ns()
       ms = (t1 - t0) // 1_000_000

       return {
             'color ranking': ranking,
             'average session length': avg_seesion_length,
             'percentiles': {'p50': p50, 'p75': p75, 'p90': p90, 'p99': p99},
             'first time users': first_time_count,
             'run time': ms
       }

def main():
    parser = argparse.ArgumentParser(description="FAnalyze r/place 2022 activity for a given time window")
    parser.add_argument("start_date", type=str, help="Start date in format 'YYYY-MM-DD HH'")
    parser.add_argument("end_date", type=str, help="End date in format 'YYYY-MM-DD HH'")
    parser.add_argument("--path", type=str, default="2022_place_canvas_history.parquet", help="Path to the Parquet file")
    args = parser.parse_args()

    results  = function(args.start_date, args.end_date, args.path)
    
    print(f"\nTimeframe: {args.start_date} to {args.end_date}\n")

    print("Ranking of Colors by Distinct Users:")
    for i, (name, hex_code, users) in enumerate(results["color ranking"], start=1):
        print(f"{i:2d}. {name}: {users} users")

    print(f"\nAverage Session Length: {results['average session length']:.2f} seconds")


    print("\nPercentiles of Pixels Placed:")
    for k, v in results["percentiles"].items():
        print(f"  {k}: {v:.2f}")

    print(f"\nFirst-time users: {results['first time users']}")

    print(f"\nTotal runtime: {results['run time']} ms")


if __name__ == "__main__":
     main()












    

    
    