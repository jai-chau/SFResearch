''' 

Signal - Betting Against Beta
Variation - Skew Adjustment 
Data Required - Barra Predicted Beta (predbeta/predicted_beta/pred_beta/etc...)

Explanation:
We found that our distribution of betas is right-skewed while we want a normal distribution for our beta calculations.
So, we run our betas through a rank transform and a reverse cdf to get our desired distribution.
And since our signal is going short high beta stocks and long low beta stocks, we use (-1 * skewadjusted_predbeta) as our signal

'''

import polars as pl 

data = pl.DataFrame()

# Start of Signal Code
df = (
    data.lazy()
    .sort(["barrid", "date"])
    # --- BAB = -predicted_beta ---
    .with_columns([
        (-pl.col("predicted_beta")).alias("bab")
    ])
)