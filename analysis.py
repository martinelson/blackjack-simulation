import pandas as pd
from math import sqrt
from scipy import stats


def batch_means(df, threshold, path, b=30):
    n = len(df)
    m = n // b
    y_bar_n = df['Player_Return'].mean()
    v_hat_b = 0
    ci = .95
    alpha = (1-ci) / 2
    batch_means_list = []
    for i in range(b):
        df_batch = df[m*i:m*(i+1)]
        batch_mean = df_batch['Player_Return'].mean()
        v_hat_b += (batch_mean - y_bar_n)**2
        batch_means_list.append(batch_mean)

    v_hat_b = (m / (b-1))*v_hat_b
    t_score = stats.t.ppf(1-alpha, (b-1))
    half_length = t_score * sqrt(v_hat_b / n)
    upper_bound = y_bar_n + half_length
    lower_bound = y_bar_n - half_length

    s1 = pd.Series(batch_means_list)
    s1.to_csv(path)

    return f"Hitting until over {threshold} will yield an average return of {y_bar_n} with a {ci*100}% confidence " \
           f"interval between {upper_bound} and {lower_bound}"
