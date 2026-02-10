# Predicting Sustained Activity in r/Place 2022

## Question:
I wanted to know, given recent activity at a pixel, can we predict whether that pixel will experience sustained interaction (conflict) in the near future?

## Data and Preproccessing:
I started with my "2022_place_canvas_history.parquet" file that I created in a previos analysis task. Then I aggregated the data further into pixel-minute units:
- Each row represents a single pixel (x,y) furing a single minute
- for each pixel-minute:
    - edits: number of edits
    - users: number of unique users

For feature engineering I defined temporal windows. So for each pixel-minute at time t:
- Features (past window): activity in the previous 5 minutes:
    - past_5m_edits: number of edits in the past 5 minutes
    - past_5m_users: number of unique users in the past 5 minutes
- Label (future window): activity in the next 5 minutes

Then I defined **conflict**. I said a pixel is labeled as having **future condlict** if it receives **>= 5 edits in the next 5 minutes**. This filters out trivial churn and focuses the task on sustained, high-intensity interaction rather than a couple follow up edits.

Also, it is important to note that features only use past information and labels use only future information to avoid temporal leakage.

## Evaluation Strategy:
Since the r/Place data is highly time-dependent, I used forward-chaining (rolling) cross validation. In my evaluation:
- Data is split by hour
- For each fold:
    - Train on all earlier hours within a defined window
    - Test on the immediately following hour
This was so I could evaluate the model's ability to generalize forward in time.

## Time Windows Analyzed:
I chose two time windows that both had a lot of activity and analyzed the separately:
- First: 2022-04-03 16:00 to 2022-04-04 00:00
- Second: 2022-04-04 16:00 to 2022-04-05 00:00
The same feature set, label definition, and evaluation pipeline were applied to both windows to enable direct comparison.

## Model:
A logistic regression model was used as baseline classifier:
The inputs were:
- past_5m_edits
- past_5m_users
The output was:
- probablity of a future conflict

## Quantitative Results:
### First Window:
Average across folds:
- Precision: ~0.72
- Recall: ~0.36
- F1: ~0.48

### Second Window:
Average across folds:
- Precision: ~0.79
- Recall: ~0.45
- F1: ~0.57

### Interpretation:
These results show our models performance improves substatially in the later window. This suggests that pixel conflict becomes more predictable later in the event.

## Visuals:
To visualize the data, I created a heat maps of the canvas for each time frame. In the images, pixels with more edits in that time frame appear more intense (red and yellow) and pixels with less edits appear darker or black. They wer also plotted using a logarithmic color scale to account for the heavy-tailed distribution of activity.

### First Window:
[First Window Heat Map] (pixel_activity_heatmap_1.png)
In the earlier window, activity is spread out across the canvas, with many small hotspots scattered across the canvas. Large, well-defined regions are less common, and borders between regions are relatively fuzzy.


### Second Window:
[Second Window Heat Map] (pixel_activity_heatmap_2.png)
In the later window, activity is more concentrated into larger, clearly defined regions. Contested borders and defended areas are more visible, and interaction is less evenly distributed across the canvas.

### Connection to Model:
These images help explain why my model was more accurate in the later time frame. Since the data was in more defined areas it was easier to predict which pixels would experience high conflict.

## Limitations:
A few limitations for this analysis were:
- The analysis only focused on active pixels, not the entire canvas.
- the results are for selected timeframes that had high-activity, not the full dataset.
- Logisitic regression gives a basseline but doesn't show any complex non linear relationships.

## Conclusion:
My analysis shows that the r/Place dataset can be meanfully modeled as a space and time prediction problem. Just with simple temporal features, future pixel activity can be predicted with reasonable accuracy, especially later on in the event.


