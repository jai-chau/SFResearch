''' 

Signal - Betting Against Beta
Variation - Classic 
Data Required - Barra Predicted Beta (predbeta/predicted_beta/pred_beta/etc...)

Explanation:
Instead of computing the beta for each security manually we just use the predicted betas that Barra gives us.
Since our signal is going short high beta stocks and long low beta stocks, we use (-1 * predbeta) as our signal (since once we z-score we get the desired distribution)

'''

import polars as pl 
from scipy.stats import norm
import numpy as np

data = pl.DataFrame()

# Start of Signal Code
# We ran our 'predbeta' within each date and scaling to [0, 1].
ranked_df = (
    data.sort(["date", "predbeta"])
    .with_columns(
        (
            (pl.col("predbeta").rank("average").over("date") - 1)
            / (pl.col("predbeta").count().over("date") - 1)
        ).alias("rank_scaled")
    )
)

# We then apply the inverse CDF of the standard normal distribution to remove skewness
transformed_df = ranked_df.with_columns(
    pl.col("rank_scaled").map_elements(lambda x: norm.ppf(np.clip(x, 1e-6, 1 - 1e-6)), return_dtype=pl.Float64).alias("noskew_predbeta")
)

# We then multiply by -1 to get the desired signal (Long low beta and short high beta)
signals = transformed_df.with_columns(pl.col("noskew_predbeta") * -1).select(["date", "barrid", "noskew_predbeta"]).sort(["barrid", "date"])