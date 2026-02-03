import duckdb as db

PATH = '2022_place_canvas_history.parquet'

con = db.connect()

print(con.execute("DESCRIBE SELECT * FROM read_parquet('2022_place_canvas_history.parquet')").fetchdf())


time_dif_query = f"""
WITH base AS (
    SELECT
        timestamp,
        user_id,
        pixel_color,
        regexp_extract_all(coordinate, '-?\\d+') AS nums
    FROM read_parquet('{PATH}')
),

events AS (
    SELECT
        timestamp,
        user_id
    FROM base
    WHERE array_length(nums) = 2
),

deltas AS (
    SELECT
        timestamp,
        user_id,
        LAG(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) AS prev_timestamp
    FROM events
),

per_event AS (
    SELECT
        timestamp,
        user_id,
        prev_timestamp,
        EXTRACT(EPOCH FROM (timestamp - prev_timestamp)) AS delta_seconds
    FROM deltas
    WHERE prev_timestamp IS NOT NULL
)

SELECT
    user_id,
    (COUNT(*) + 1) AS placements,
    MIN(timestamp) AS first_timestamp,
    MAX(timestamp) AS last_timestamp,
    (EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))) / 3600.0) AS active_span_hours,

    AVG(delta_seconds) AS mean_delta_seconds,
    STDDEV_SAMP(delta_seconds) AS std_delta_seconds,
    MIN(delta_seconds) AS min_delta_seconds,
    MAX(delta_seconds) AS max_delta_seconds,
    
    AVG(CASE WHEN delta_seconds BETWEEN 295 AND 301 THEN 1 ELSE 0 END) AS frac_near_300s,
    AVG(CASE WHEN delta_seconds <= 10 THEN 1 ELSE 0 END) as frac_less_10s

FROM per_event
GROUP BY user_id
HAVING COUNT(*) >= 50
ORDER BY frac_near_300s DESC
LIMIT 2000
"""

df = con.execute(time_dif_query).fetchdf()
df.to_csv("bucket_precision_user_timing_summary.csv", index=False)
print("\nSaved: bucket_precision_user_timing_summary.csv")
print(df.head(20))






