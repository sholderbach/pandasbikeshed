import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr


def robust_hist(x, ax=None, **kwargs):
    """
    Wrapper function to `plt.hist` dropping values that are not finite

    Returns:
        Axes
    """
    mask = np.isfinite(x)
    ax = ax or plt.gca()
    ax.hist(x[mask], **kwargs)
    return ax

def robust_scatter(x, y, size=0.5, alpha=0.3, **kwargs):
    """
    Wrapper function to `sns.scatterplot` dropping value pairs that are not finite

    Sets default `size` of 0.5 and `alpha` to 0.3

    Returns:
        Axes
    """
    mask = np.isfinite(x) & np.isfinite(y)
    return sns.scatterplot(x[mask], y[mask], size=size, alpha=alpha, **kwargs)

def robust_kde(x, y=None, **kwargs):
    """
    Wrapper function to `sns.kdeplot` dropping values or value pairs that are not finite

    Returns:
        Axes
    """
    if y is not None:
        mask = np.isfinite(x) & np.isfinite(y)
        return sns.kdeplot(x[mask], y[mask], **kwargs)
    else:
        mask = np.isfinite(x)
        return sns.kdeplot(x[mask], **kwargs)



def robust_info(x, y, ax=None, **kwargs):
    """
    Prints correlation information of two arrays into axis.

    Useful for `sns.PairGrid` (see `pb.plot.robust_pairplot`).
    As non finite value pairs are dropped prints number of comparisons.
    Pearson and Spearman correlation values with associated p-value.

    Returns:
        Axes
    """
    mask = np.isfinite(x) & np.isfinite(y)
    n = np.sum(mask)
    pear_r, pear_p = pearsonr(x[mask], y[mask])
    spea_r, spea_p = spearmanr(x[mask], y[mask])
    ax = ax or plt.gca()
    ax.annotate(
             f'N = {n} \n'
             f'Pearson:\nr={pear_r:.3f} p={pear_p:.2E}\n'
             f'Spearman:\nr={spea_r:.3f} p={spea_p:.2E}',
             xy=(0.5, 0.5),
             xycoords='axes fraction',
             va='center', ha='center',
             wrap=True,
             **kwargs)
    return ax

def robust_pairplot(df, lower_kind='scatter', upper_kind='info', diag_kind='hist', **kwargs):
    """
    Similar function to `sns.pairplot` that drops non-finite value pairs instead of all rows containing NaNs

    Args:
        lower_kind: {'scatter', 'kde', 'info'}
        upper_kind: {'scatter', 'kde', 'info'}
        diag_kind: {'hist', 'kde'}
        **kwargs: passed to sns.PairGrid

    Returns:
        sns.PairGrid
    """
    diag_methods = {'hist': robust_hist, 'kde': robust_kde}
    tria_methods = {'scatter': robust_scatter, 'kde': robust_kde, 'info': robust_info}
    g = sns.PairGrid(df, **kwargs)
    g.map_diag(diag_methods[diag_kind])
    g.map_upper(tria_methods[upper_kind])
    g.map_lower(tria_methods[lower_kind])
    return g

def corr_heatmap(df, method='pearson', triangle_only=True,
                 ax=None,
                 cmap='RdBu_r', linewidths=0.1,
                 **heat_map_kwargs):
    """
    Plot a correlation heatmap directly from a dataframe

    Args:
        df: pd.DataFrame
        method: {'pearson', 'spearman'}
        triangle_only: bool
            Hide the diagonal and upper triangle.
            default=True

    Returns:
        Axes
    """
    corrmat = df.corr(method=method)
    mask = (~np.tri(corrmat.shape[0], dtype=np.bool)) if triangle_only else None
    locator = mpl.ticker.MultipleLocator(0.25)
    return sns.heatmap(corrmat, ax=ax, mask=mask,
                       vmin=-1., vmax=1., center=0, cbar_kws={'ticks': locator},
                       linewidths=linewidths, cmap=cmap,
                       **heat_map_kwargs)

def dist_catplot(data=None, x=None, kind='hist', dist_columns=None,
                 col=None, row=None, hue=None, col_wrap=None,
                 **facet_kwargs):
    """
    Make faceted histograms or kdeplots either from tidy longform data or columns of a wide DataFrame

    Args:
        data: pd.DataFrame
        x: str, None
            Defines a column in tidy data, from which to take the values for the histogram.
            If unspecified, numeric columns are considered for the histograms
        kind: {'hist', 'kde'}
        dist_columns: Iterable column names, optional
            If x unspecified, defines the columns to be considered for histograms
        col, row, hue: str, optional
            Column names to facet the data.
        col_wrap: int, optional
            breaks cols, if no row specified

    Returns:
        sns.FacetGrid
    """
    if x is None:
        if dist_columns is not None:
            numeric_columns = dist_columns
        else:
            numeric_columns = [name
                                for name, dtype
                                in data.dtypes.items()
                                if pd.api.types.is_numeric_dtype(dtype)]
        non_numeric_columns = data.columns.difference(numeric_columns)
        cols_name = data.columns.name or 'columns'
        hist_col = 'value' if 'value' not in data.columns else 'histogram_value'
        dat = data.melt(id_vars=non_numeric_columns,
                        value_vars=numeric_columns,
                        var_name=cols_name,
                        value_name=hist_col)
        if col is None:
            col = cols_name
        elif row is None and col_wrap is None:
            row = cols_name
        elif hue is None:
            hue = cols_name
        else:
            raise ValueError('No dimension available to unpack the numeric columns.')
    else:
        dat = data
        hist_col = x
    plt_funcs = {'hist': plt.hist, 'kde': sns.kdeplot}
    g = sns.FacetGrid(dat, col=col, row=row, hue=hue, col_wrap=col_wrap, **facet_kwargs)
    g.map(plt_funcs[kind], hist_col)
    return g
