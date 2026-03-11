# Response to Peer and Teacher Feedback

1. To address the formatting and introductory feedback, I added a longer background section, fixed all typos, and corrected the file paths so the visualizations render properly.

2. Analytically, I moved away from looking at factors independently and instead implemented a balanced logistic regression model with a train/test split. This allowed me to evaluate the combined predictive power of these variables, including interaction effects, while controlling for confounders. I also expanded my target variable beyond a simple binary definition by categorizing delay severity (Mild, Moderate, Severe) to see if factors like weather disproportionately cause extreme delays.

3. Finally, to address the missing weather and airport analyses, I incorporated robust statistical tests (Chi-Square, Kruskal-Wallis) and generated spatial-temporal map visualizations to explicitly evaluate geographic and seasonal weather heterogeneity.