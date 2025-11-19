''' 

Signal - Momentum
Variation - Classic 12-2 Momentum
Data Required - Returns

Explanation:
Its momentum

'''

import polars as pl 

data = pl.DataFrame()

# Start of Signal Code
df = (
    data.lazy()
    .sort(["barrid", "date"])
    # --- Momentum = rolling sum of past 12-2 months returns ---
    .with_columns(pl.col("ret").log1p().alias("logret"))
    .with_columns(pl.col("logret").rolling_sum(11, min_periods=11).over("barrid").alias("mom"))
    .with_columns(pl.col("mom").shift(1).over("barrid"))
)