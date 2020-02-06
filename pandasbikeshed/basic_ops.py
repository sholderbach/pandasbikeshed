import numpy as np
import pandas as pd

def flat_corr(df, columnns=slice(None), method='pearson', ascending=False):
    """
    Computes correlation ignoring NaN values with `method` of the columns in `df`
    Returns: a dataframe with a sorted column named after `method` and a MultiIndex describing the pairings
    """
    res = df.loc[:,columnns].corr(method)
    res[np.tri(res.shape[0], dtype=np.bool)] = np.nan
    res = res.stack().dropna().sort_values(ascending=ascending).to_frame(name=method)
    return res
