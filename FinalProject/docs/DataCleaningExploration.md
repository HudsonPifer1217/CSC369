# Data Cleaning and Exploratory Analysis  
## U.S. Domestic Flight Delays (2020–2025)

## 1. Overview

For this project, I am analyszing U.S. domestic flight performance data from January 2020 through November 2025. My primary research question was:

> What factors most strongly predict flight delays in U.S. domestic travel, and how do these factors differ by airport and airline?
---

## 2. Data Cleaning Decisions

### Getting the Data (challenge)

I had downloaded the flight data month by month from the Beauro of Transportation Statistics website. This left me with 71 separate CSV files from January 2020 to Novemeber 2025 totaling ~17 GB.

I then used a DuckDB script to combine these CSV files into one massive CSV file.

This was difficult because it took forever to download that much data month by month.

### Column Selection

The raw dataset contains a very large number of columns (over 100). I selected a focused subset of variables that directly support my research question. These included:

- **Time variables**: `Year`, `Month`, `DayOfWeek`, `CRSDepTime`, etc.
- **Airline identifiers**: `Reporting_Airline`, `DOT_ID_Reporting_Airline`
- **Airport/location variables**: `Origin`, `Dest`, `OriginState`, `DestState`
- **Flight characteristics**: `Distance`, `AirTime`, `TaxiOut`, `CRSElapsedTime`
- **Delay metrics**: `DepDelayMinutes`, `ArrDelayMinutes`, etc.
- **Delay cause breakdown**: `CarrierDelay`, `WeatherDelay`, `NASDelay`, `SecurityDelay`, `LateAircraftDelay`

I intentionally removed:

- Tail numbers
- Flight numbers
- All diversion-related columns
- Gate return fields
- Redundant identifiers

Making these decisions took a long time because there are so many columns and it was hard to know which ones I would actually end up using. To deal with this I figured it wouldn't hurt too much to leave in columns I was on the fence about, as they could lead to something interesting down the line.

---

### Removing Cancelled and Diverted Flights

To simplify the analysis and avoid inconsistent delay measurements, I removed:

- `Cancelled = 1`
- `Diverted = 1`

Cancelled flights do not have meaningful arrival delays, and diverted flights introduce null values and structural irregularities. While interesting in their own right, including them would complicate interpretation of delay distributions.

---

### Creating a Clean Parquet File

After filtering and column selection, I created a new file: clean_flights.parquet, from the massive CSV file.

The resulting clean parquet file was only 900 mb.

---

## 3. Challenges Encountered

### 1. Extremely Skewed Delay Distribution

The histogram of `DepDelayMinutes` revealed:

- A massive spike at 0 minutes
- A heavy right tail
- Extreme outliers exceeding 2000 minutes

This indicates a **zero-inflated, heavily right-skewed distribution**.

This posed two challenges:

- The mean delay is misleading.
- Linear modeling assumptions (normality) do not hold.

To better visualize the distribution, I:
- Applied log-scaling to the frequency axis
- Trimmed extreme outliers for clearer plots

---

### 2. Structural Break in 2020 (COVID)

The monthly time series of delay rates showed a dramatic drop in 2020.

This was clearly due to:
- Reduced air traffic during COVID
- Lower congestion
- Operational changes

This makes me trust the data because it aligns with my historical knowledge of flight delays during Covid.

---

### 3. Performance Considerations

With over 37 million rows, full-table plotting was impractical.

To address this, I:
- Used `USING SAMPLE` in DuckDB queries
- Aggregated data before plotting
- Created a cleaned Parquet file to reduce overhead

---

## 4. Key Exploratory Findings

### Distribution of Delays

- Most flights depart on time or within a small delay window.
- A small subset of flights experience extreme delays.
- The delay distribution is heavy-tailed and non-normal.

---

### Monthly Delay Rate (2020–2025)

The time series revealed:

- A sharp drop in delays during mid-2020 (COVID effect)
- Return to higher delay rates post-2021
- Recurring seasonal spikes
- Peaks exceeding 30% in certain months

This suggests:
- Strong seasonality
- Congestion effects
- System-level variability

---

### Time of Day Effects (Preliminary Insight)

Although not fully modeled yet, initial aggregation suggests delays accumulate later in the day. This aligns with cascading delay effects from earlier flights.

