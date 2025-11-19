''' 

Signal - Momentum
Variation - Volatility Scaled Momentum
Data Required - Returns and Specific Risk (from Barra)

Explanation:
Divide momentum by volatility

'''

import polars as pl 

data = pl.DataFrame()

# Start of Signal Code
df = (
    data.lazy()
    .sort(["barrid", "date"])
    # --- Converting return and specific risk into fractional space ---
    .with_columns(
        pl.col('specific_risk').truediv(100)
    )
    # --- Momentum = rolling sum of past 12-2 months returns ---
    .with_columns(
        pl.col("ret").log1p().alias("logret")
        )
    .with_columns(
        pl.col("logret").rolling_sum(11, min_periods=11).over("barrid").alias("mom")
        )
    .with_columns(
        pl.col("mom").shift(1).over("barrid")
        )
    # --- Vol adjustment using Barra's specific_risk ---
    .with_columns(
            (pl.col("momentum_12m") / pl.col("specific_risk")).alias("momentum_12m_voladj"),
    )
)