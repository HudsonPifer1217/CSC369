import duckdb as db

PATH = '2022_place_canvas_history.parquet'

con = db.connect()

rect_query = f"""
WITH base AS (
    SELECT
        user_id,
        timestamp,
        pixel_color,
        coordinate,
        regexp_extract_all(coordinate, '-?\\d+') as nums
    FROM read_parquet('{PATH}')
),

rects AS (
    SELECT
        user_id,
        timestamp,
        pixel_color,
        coordinate,
        nums,
        array_length(nums) AS n_nums,

        CAST(nums[1] AS INTEGER) AS x1,
        CAST(nums[2] AS INTEGER) AS y1,
        CAST(nums[3] AS INTEGER) AS x2,
        CAST(nums[4] AS INTEGER) AS y2
    FROM base
    WHERE array_length(nums) = 4
),

norm AS (
    SELECT
        user_id,
        timestamp,
        pixel_color,
        coordinate,
        x1, y1, x2, y2,

        LEAST(x1, x2) AS min_x,
        GREATEST(x1, x2) AS max_x,
        LEAST(y1, y2) AS min_y,
        GREATEST(y1, y2) AS max_y
    FROM rects
)

SELECT
    timestamp,
    user_id,
    pixel_color,
    coordinate,
    min_x, max_x, min_y, max_y,
    (max_x - min_x) * (max_y - min_y) AS area,
    (max_x - min_x) AS width,
    (max_y - min_y) AS height
FROM norm
ORDER BY timestamp
"""

counts_query = f"""
WITH base AS (
  SELECT regexp_extract_all(coordinate, '-?\\d+') AS nums
  FROM read_parquet('{PATH}')
)
SELECT
  SUM(CASE WHEN array_length(nums) = 2 THEN 1 ELSE 0 END) AS two_number_rows,
  SUM(CASE WHEN array_length(nums) = 4 THEN 1 ELSE 0 END) AS four_number_rows,
  SUM(CASE WHEN array_length(nums) NOT IN (2,4) THEN 1 ELSE 0 END) AS other_rows
FROM base;
"""

print("== Row type counts ==")
print(con.execute(counts_query).fetchdf())

print("\n== Extracting rectangle events ==")
rect_df = con.execute(rect_query).fetchdf()
print(rect_df)

rect_df.to_csv("bucket_rectangles_events.csv", index=False)
print("\nSaved: bucket_rectangles_events.csv")