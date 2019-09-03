import numpy as np
import pandas as pd
import pandas.util.testing as pd_samples
from pandas.testing import assert_frame_equal, assert_series_equal

import pytest

from pandasbikeshed.fancyfilter import me

ex_df = pd_samples.makeDataFrame()
ex_df.iloc[0,:] = 0
ex_df.iloc[1,:] = np.nan
ex_df.iloc[2,:] = np.inf

ex_df2 = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': ['c', 'b', 'a']})
ex_df2.set_index('B', inplace=True)

ex_series = pd_samples.makeFloatSeries('test')

def test_nullindexing():
    assert_frame_equal(ex_df[me], ex_df)
    assert_series_equal(ex_series[me], ex_series)

@pytest.mark.parametrize('fancy,traditional', [(ex_df[me.A < 0], ex_df[ex_df.A < 0]),
                                            (ex_df[me.A <= 0], ex_df[ex_df.A <= 0]),
                                            (ex_df[me.A == 0], ex_df[ex_df.A == 0]),
                                            (ex_df[me.A != 0], ex_df[ex_df.A != 0]),
                                            (ex_df[me.A >= 0], ex_df[ex_df.A >= 0]),
                                            (ex_df[me.A > 0], ex_df[ex_df.A > 0]),]
)
def test_comparison(fancy, traditional):
    assert_frame_equal(fancy, traditional)

@pytest.mark.parametrize('fancy,traditional', [((me < 0)(ex_series), ex_series < 0),
                                            ((me <= 0)(ex_series), ex_series <= 0),
                                            ((me == 0)(ex_series), ex_series == 0),
                                            ((me != 0)(ex_series), ex_series != 0),
                                            ((me >= 0)(ex_series), ex_series >= 0),
                                            ((me > 0)(ex_series), ex_series > 0),]
)
def test_series_comparison(fancy, traditional):
    assert_series_equal(fancy, traditional)

@pytest.mark.parametrize('fancy,traditional', [(ex_df[me.A.isna()], ex_df[ex_df.A.isna()]),
                                            (ex_df[me.A.notna()], ex_df[ex_df.A.notna()]),
                                            (ex_df[me.A.isfinite()], ex_df[np.isfinite(ex_df.A)]),]
)
def test_additional_methods(fancy, traditional):
    assert_frame_equal(fancy, traditional)

def test_isin():
    names = ['a', 'c']
    assert_frame_equal(ex_df2[me.A.isin(names)], ex_df2[ex_df2.A.isin(names)])
    assert_frame_equal(ex_df2[me.A.notin(names)], ex_df2[~ex_df2.A.isin(names)])
    names = ['a', 'd']
    assert_frame_equal(ex_df2[me.A.isin(names)], ex_df2[ex_df2.A.isin(names)])
    assert_frame_equal(ex_df2[me.A.notin(names)], ex_df2[~ex_df2.A.isin(names)])

@pytest.mark.parametrize('fancy,traditional', [(ex_df[me.A < me.B], ex_df[ex_df.A < ex_df.B]),
                                            (ex_df[me.A <= me.B], ex_df[ex_df.A <= ex_df.B]),
                                            (ex_df[me.A == me.B], ex_df[ex_df.A == ex_df.B]),
                                            (ex_df[me.A != me.B], ex_df[ex_df.A != ex_df.B]),
                                            (ex_df[me.A >= me.B], ex_df[ex_df.A >= ex_df.B]),
                                            (ex_df[me.A > me.B], ex_df[ex_df.A > ex_df.B]),]
)
def test_inframe_comparison(fancy, traditional):
    assert_frame_equal(fancy, traditional)

def test_index_errors():
    with pytest.raises(KeyError) as raised:
        ex_df2[me.wrong_key]
    assert 'wrong_key' in str(raised.value)

    with pytest.raises(KeyError) as raised:
        ex_df2[me['wrong_key']]
    assert 'wrong_key' in str(raised.value)

    with pytest.raises(TypeError) as raised:
        ex_df2[me[('A', 'B')]]

def test_truthiness():
    assert_frame_equal(ex_df[me.A], ex_df[ex_df.A.astype('bool')])

def test_bool_combine():
    mask = ex_df.C > 0
    other_mask = ex_df.A < 0
    assert_frame_equal(ex_df[(me.A<0) & (me.C>0)], ex_df[other_mask & mask])
    assert_frame_equal(ex_df[(me.A<0) | (me.C>0)], ex_df[other_mask | mask])
    assert_frame_equal(ex_df[(me.A<0) ^ (me.C>0)], ex_df[other_mask ^ mask])

def test_boolmask():
    mask = np.array(ex_df.C > 0)
    other_mask = ex_df.A < 0
    assert_frame_equal(ex_df[(me.A<0) & mask], ex_df[other_mask & mask])
    assert_frame_equal(ex_df[(me.A<0) | mask], ex_df[other_mask | mask])
    assert_frame_equal(ex_df[(me.A<0) ^ mask], ex_df[other_mask ^ mask])

@pytest.mark.xfail
def test_boolmask_inverted():
    mask = np.array(ex_df.C > 0)
    other_mask = ex_df.A < 0
    assert_frame_equal(ex_df[mask & (me.A<0)], ex_df[other_mask & mask])
    assert_frame_equal(ex_df[mask | (me.A<0)], ex_df[other_mask | mask])
    assert_frame_equal(ex_df[mask ^ (me.A<0)], ex_df[other_mask ^ mask])

def test_not_operator():
    assert_frame_equal(ex_df2[~(me.A == 'b')], ex_df2[me.A != 'b'])
