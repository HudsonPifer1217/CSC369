import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("bucket_rectangles_events.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

COLOR = "#FFA500"

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[df["timestamp"].min()],
    y=[0.5],
    mode="lines",
    line=dict(width=3),
    name="Rectangle wipe event (admin action)",
    hoverinfo="skip",
    showlegend=True
))

fig.add_trace(go.Scatter(
    x=[df["timestamp"].min()],
    y=[0.5],
    mode="markers",
    marker=dict(size=10),
    name="Hover target (shows metadata)",
    hoverinfo="skip",
    showlegend=True
))

for _, r in df.iterrows():
    fig.add_shape(
        type="line",
        x0=r["timestamp"], x1=r["timestamp"],
        y0=0, y1=1,
        line=dict(width=3),
        opacity=0.9
    )

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=[0.5] * len(df),
    mode="markers",
    marker=dict(color=COLOR, size=12, opacity=0.8),
    customdata=df[[
        "pixel_color","coordinate",
        "min_x","min_y","max_x","max_y",
        "width","height","area","user_id"
    ]],
    hovertemplate=(
        "<b>%{x|%Y-%m-%d %H:%M:%S UTC}</b><br>"
        "color=%{customdata[0]}<br>"
        "coord=%{customdata[1]}<br>"
        "box=(%{customdata[2]},%{customdata[3]})→(%{customdata[4]},%{customdata[5]})<br>"
        "w×h=%{customdata[6]}×%{customdata[7]} area=%{customdata[8]}<br>"
        "user=%{customdata[9]}<extra></extra>"
    ),
    showlegend=False
))

fig.update_layout(
    title=dict(
        text="Administrative Rectangle Wipe Events on r/place (2022)<br><sup>Each vertical line indicates a bulk moderation action encoded as (x1,y1,x2,y2)</sup>",
        x=0.5
    ),
    xaxis_title="Time (UTC)",
    yaxis=dict(visible=False, range=[0, 1]),
    legend=dict(
        title="Key",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.01
    ),
    margin=dict(l=40, r=40, t=90, b=40),
)

fig.update_xaxes(showgrid=True)

fig.add_annotation(
    x=df["timestamp"].min(),
    y=1.15,
    xref="x",
    yref="paper",
    text=f"Total rectangle wipes detected: {len(df)}",
    showarrow=False
)

fig.write_html("plots/rectangles_timeline.html", include_plotlyjs="cdn")
print("Wrote rectangles_timeline.html")

fig.show()