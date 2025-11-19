''' 

Signal - Betting Against Beta
Variation - Classic 
Data Required - Barra Predicted Beta (predbeta/predicted_beta/pred_beta/etc...)

Explanation:
Instead of computing the beta for each security manually we just use the predicted betas that Barra gives us.
Since our signal is going short high beta stocks and long low beta stocks, we use (-1 * predbeta) as our signal (since once we z-score we get the desired distribution)

'''

df = (
    data.lazy()
    .sort(["barrid", "date"])
    # --- BAB = -predicted_beta ---
    .with_columns([
        (-pl.col("predicted_beta")).alias("bab")
    ])
)