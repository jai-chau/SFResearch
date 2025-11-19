''' 

Signal - Mean Reversion
Variation - Classic 1 month Mean Reversion
Data Required - Returns and Specific Risk (from Barra)

Explanation:
Its just 1 month mean reversion

'''

import polars as pl 

data = pl.DataFrame()

# Start of Signal Code
df = (
    data.lazy()
    .sort(["barrid", "date"])
    # --- Mean Reversion = rolling sum of past 1 months returns ---
    .with_columns([
            pl.col("log_return")
              .rolling_sum(window_size=22)
              .over("barrid")
              .alias("meanrev_temp")
        ])
        .with_columns([
            (-pl.col("meanrev_temp").shift(1).over("barrid")).alias("meanrev_1m")
        ])
)