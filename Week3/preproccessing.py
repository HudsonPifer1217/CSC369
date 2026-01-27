import duckdb as dd

#Preproccessing

dd.sql("""
COPY (
   SELECT
      timestamp,
      hash(user_id) AS user_id,
      pixel_color,
      coordinate
   FROM read_csv('2022_place_canvas_history.csv')
   ORDER BY timestamp ASC
)
TO '2022_place_canvas_history.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);
""")
       




