# Irregular Activity on r/place (2022)
### Hudson Pifer

The following analysis identifies two major buckets of irregular (non-human) activity in the
r/place 2022 dataset.

---

## Bucket 1: Administrative Rectangle Wipe Events

In the r/Place cavas data timelapse, there are several instances of a black or solid color rectangle being placed over an area, likely to censor something inappropriate. I decided to analyze those events as they seemed automated and non-human. I found 19 times that a rectangle was placed, most were black but there were a few other colors.

- [Timeline of rectangle wipe events](https://hudsonpifer1217.github.io/CSC369/Week4/rectangles_timeline.html)

 
In the timeline visualization above, vertical lines represent a rectangle placement. They are encoded as a four-coordinate rectangle. These placements are very rare: 19 in about 160 million events, and they occur in short bursts, consistent with reactive moderation rather than organic user behavior. The sparsity and scale of these actions clearly distinguish them from normal pixel placements. 

- [Distribution of rectangle wipe areas](https://hudsonpifer1217.github.io/CSC369/Week4/rectangles_area_hist.html)

In the above histogram, we can see the distribution of areas affected by administrative rectangle wipe events on r/Place. Most moderation actions are relatively small (16/19), but a small number of wipes affect tens of thousands of pixels in a single operation. This long-tailed distribution highlights the capacity of administrative actions to remove large regions of the canvas instantaneously, a capability unavailable to regular users.


**Detection script:** `bucket_rectangles.py`

In the Python file bucket_rectangles.py, I used DuckDB to query the r/place 2022 Parquet dataset directly and identify non-human moderation actions encoded as rectangular coordinate updates. The script extracts all numeric values from the coordinate field and isolates rows containing four numbers, which correspond to administrative rectangle wipe events rather than normal pixel placements. These coordinates are normalized to compute each rectangle’s width, height, and affected area. I also counted how many rows in the dataset represent normal pixels versus rectangle wipes as a sanity check. The resulting rectangle events were saved to a CSV file for visualization and further analysis.

---

## Bucket 2: Highly Regular, Long-Duration Placement Behavior

I also searched the data set for irregular, precise placements over a sustained period of time. In the actual r/Place competition, there was a cool down period of 300 seconds or 5 minutes between a users pixels placements. I assumed that if a user's time between placements stayed close to or exactly 300 seconds over a long period of time, then this behavior could be catagorized as non-human. Two users stuck out the most. One had 94.2% of 106 placements within 301 seconds of each other over an 8.69 hour period, and the other had 92.9% of 100 placements within 301 second timeframe over 7.84 hours. Both of these seem impossible for a human to perform.

The following scatterplot shows that cooldown-aware behavior is common among users, but highly consistent timing is rare. The small cluster of users in the bottom right with near-perfect cooldown usage and very low timing variability stands out as likely automated behavior. 

- [Cooldown usage vs timing precision](https://hudsonpifer1217.github.io/CSC369/Week4/precision_scatter.html)

This histogram shows the distribution of timing variability across highly active r/Place users, measured as the standard deviation of time between pixel placements. The distribution is strongly right-skewed: most users cluster on the left, with relatively low to moderate variability, while a long tail extends to the right representing users with extremely irregular timing. Within the far left edge of the distribution, a very small subset exhibits exceptionally low variability, indicating near-perfect timing consistency that is difficult to reconcile with sustained human behavior.

- [Distribution of timing variability](https://hudsonpifer1217.github.io/CSC369/Week4/std_delta_histogram.html)


**Detection script:** `user_precision_bucket.py`

I also used DuckDB in user_precision_bucket.py to query the r/Place 2022 Parquet file and compute per-user timing summaries from normal (two-number) pixel placement events. The script computes inter-placement deltas per user, then aggregates each user’s placements, active span (hours), mean/std/min/max of delta seconds, and two behavioral fractions: how often placements fall near the ~300s cooldown (within 1 second) and how often they occur within 10s. It filters to users with at least 50 placements, orders by cooldown-aligned behavior, and writes the top results to bucket_precision_user_timing_summary.csv. The output is designed to surface users whose sustained, low-variance timing patterns are suspiciously consistent with automated or script-assisted activity.

---

## Conclusion

Together, these two buckets capture two different forms of irregular activity on r/Place. Administrative rectangle wipes represent explicit system-level moderation actions that are clearly non-human, while highly regular, long-duration placement behavior reflects emergent automation operating within the same rules as human participants. Importantly, this analysis distinguishes between cooldown-aware human coordination and truly machine-like precision sustained over time. By focusing on rarity, consistency, and duration rather than single metrics alone, these buckets provide a conservative and interpretable view of non-human activity in the r/place 2022 event. One other bucket not analyzed was how the canvas expands twice during the competition. This coul be seen as irregular activity, but due to time constraints I did not include it in my analysis.