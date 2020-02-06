import numpy as np
import pandas as pd
import pandas.util.testing as pd_samples
from pandas.testing import assert_frame_equal, assert_series_equal
from scipy.spatial.distance import squareform
from scipy.special import comb

import pytest

from pandasbikeshed.basic_ops import flat_corr

ex_df = pd_samples.makeDataFrame()
ex_missing_df = pd_samples.makeMissingDataframe()

def test_flat_corr_shape():
    assert flat_corr(ex_df).shape[0] == comb(ex_df.shape[1], 2, exact=True)
    assert flat_corr(ex_df).shape[0] == squareform(ex_df.corr(), checks=False).shape[0]
    assert flat_corr(ex_df, columnns=[*'ABC']).shape[0] == comb(3, 2, exact=True)

def test_flat_corr_shape_nans():
    assert flat_corr(ex_missing_df).shape[0] == comb(ex_missing_df.shape[1], 2, exact=True)
    assert flat_corr(ex_missing_df).shape[0] == squareform(ex_missing_df.corr(), checks=False).shape[0]
    assert flat_corr(ex_missing_df, columnns=[*'ABC']).shape[0] == comb(3, 2, exact=True)

def test_flat_corr_arrangement():
    res = flat_corr(ex_df)
    res_asc = flat_corr(ex_df, ascending=True)
    np.testing.assert_allclose(res_asc['pearson'], np.sort(squareform(ex_df.corr(), checks=False)))
    assert res.iloc[0,0] > res.iloc[-1,0]
    assert res_asc.iloc[0,0] < res_asc.iloc[-1,0]

def test_flat_corr_method():
    assert flat_corr(ex_df, method='spearman').notna().all(None)

@pytest.mark.xfail
def test_flat_corr_int_columns():
    assert flat_corr(ex_df, columnns=slice(1)).shape[0] == comb(ex_df.shape[1] - 1, 2, exact=True)

@pytest.mark.xfail
def test_flat_corr_nan_column():
    nan_col_df = ex_df.copy(deep=True)
    nan_col_df.iloc[:,0] = np.nan
    assert flat_corr(nan_col_df).shape[0] == comb(nan_col_df.shape[1], 2, exact=True)


