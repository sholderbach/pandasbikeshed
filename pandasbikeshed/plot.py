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
    if y:
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

    Returns:
        sns.PairGrid
    """
    diag_methods = {'hist': robust_hist, 'kde': robust_kde}
    tria_methods = {'scatter': robust_scatter, 'kde': robust_kde, 'info': robust_info}
    g = sns.PairGrid(df)
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
    mask = (~np.tri(corrmat.shape, k=-1, dtype=np.bool)) if triangle_only else None
    locator = mpl.ticker.MultipleLocator(0.25)
    return sns.heatmap(corrmat, ax=ax, mask=mask,
                       vmin=-1., vmax=1., center=0, cbar_kws={'ticks': locator},
                       linewidths=linewidths, **heat_map_kwargs)