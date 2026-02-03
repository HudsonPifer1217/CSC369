import pandas as pd
import plotly.express as px

df = pd.read_csv("bucket_rectangles_events.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

fig = px.histogram(
    df,
    x="area",
    nbins=19,
    title="Distribution of Admin Rectangle Wipe Areas in r/Place Data Set",
    hover_data=["timestamp", "pixel_color", "coordinate", "width", "height", "user_id"],
)

fig.update_layout(
    xaxis_title="Rectangle area (spixels squared)",
    yaxis_title="Count of Admin Wipe Events",
)

fig.write_html("plots/rectangles_area_hist.html", include_plotlyjs="cdn")
print("Wrote rectangles_area_hist.html")

fig.show()