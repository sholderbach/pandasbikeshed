import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.util.testing as pd_samples
from pandas.testing import assert_frame_equal, assert_series_equal

import pytest

from pandasbikeshed.plot import (robust_hist,
                                 robust_scatter,
                                 robust_info,
                                 robust_kde,
                                 robust_pairplot,
                                 corr_heatmap,
                                 dist_catplot)

nan_df = pd_samples.makeMissingDataframe()
nan_a = nan_df['A']
nan_b = nan_df['B']

def test_robust_hist():
    assert isinstance(robust_hist(nan_a), plt.Axes)
    assert isinstance(robust_hist(nan_a.values), plt.Axes)

def test_robust_scatter():
    assert isinstance(robust_scatter(nan_a, nan_b), plt.Axes)
    assert isinstance(robust_scatter(nan_a.values, nan_b.values), plt.Axes)

def test_robust_kde():
    assert isinstance(robust_kde(nan_a), plt.Axes)
    assert isinstance(robust_kde(nan_a, nan_b), plt.Axes)

def test_robust_info():
    assert isinstance(robust_info(nan_a, nan_b), plt.Axes)
    assert isinstance(robust_info(nan_a.values, nan_b.values), plt.Axes)

@pytest.mark.parametrize('kwargs_dict', [dict(), {'lower_kind': 'kde'}, {'diag_kind': 'kde'}])
def test_robust_pairplot(kwargs_dict):
    res = robust_pairplot(nan_df, **kwargs_dict)
    assert isinstance(res, sns.PairGrid)
    assert len(res.axes) == len(nan_df.columns)

def test_corr_heatmap():
    assert isinstance(corr_heatmap(nan_df), plt.Axes)
    assert isinstance(corr_heatmap(nan_df, method='spearman'), plt.Axes)
    assert isinstance(corr_heatmap(nan_df, triangle_only=False), plt.Axes)

