import pandas as pd
import plotly.express as px

df = pd.read_csv("bucket_precision_user_timing_summary.csv")

fig = px.scatter(
    df,
    x="frac_near_300s",
    y="std_delta_seconds",
    color="active_span_hours",
    hover_data=["placements"],
    title="Timing precision vs cooldown usage across users",
)

fig.update_layout(
    xaxis_title="Fraction of placements near cooldown (~300s)",
    yaxis_title="Timing variability (std dev of inter-placement time, seconds)",
)

fig.write_html("plots/precision_scatter.html", include_plotlyjs="cdn")
print("Wrote precision_scatter.html")

fig.show()