import pandas as pd
import plotly.express as px

df = pd.read_csv("bucket_precision_user_timing_summary.csv")

fig = px.histogram(
    df,
    x="std_delta_seconds",
    nbins=200,
    title="Distribution of Timing Variability Across Users",
)

fig.update_layout(
    xaxis_title="Standard deviation of inter-placement time (seconds)",
    yaxis_title="Number of users",
)

fig.write_html("plots/std_delta_histogram.html", include_plotlyjs="cdn")
print("Wrote std_delta_histogram.html")

fig.show()

