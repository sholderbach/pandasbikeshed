import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr


def robust_hist(x, color=None, label=None, **kwargs):
    mask = np.isfinite(x)
    plt.hist(x[mask], color=color, label=label, **kwargs)

def robust_scatter(x, y, color=None, label=None, size=0.5, alpha=0.3, **kwargs):
    mask = np.isfinite(x) & np.isfinite(y)
    sns.scatterplot(x[mask], y[mask], color=color, label=label, size=size, alpha=alpha, **kwargs)

def robust_kde(x, y=None, color=None, label=None, **kwargs):
    if y:
        mask = np.isfinite(x) & np.isfinite(y)
        sns.kdeplot(x[mask], y[mask], color=color, label=label, **kwargs)
    else:
        mask = np.isfinite(x)
        sns.kdeplot(x[mask], color=color, label=label, **kwargs)



def robust_info(x, y, color=None, label=None, **kwargs):
    mask = np.isfinite(x) & np.isfinite(y)
    n = np.sum(mask)
    pear_r, pear_p = pearsonr(x[mask], y[mask])
    spea_r, spea_p = spearmanr(x[mask], y[mask])
    ax = plt.gca()
    ax.annotate(
             f'N = {n} \n'
             f'Pearson:\nr={pear_r:.3f} p={pear_p:.2E}\n'
             f'Spearman:\nr={spea_r:.3f} p={spea_p:.2E}',
             xy=(0.5, 0.5),
             xycoords='axes fraction',
             va='center', ha='center',
             wrap=True,
             **kwargs)

def robust_pairplot(df, lower_kind='scatter', upper_kind='info', diag_kind='hist', **kwargs):
    diag_methods = {'hist': robust_hist, 'kde': robust_kde}
    tria_methods = {'scatter': robust_scatter, 'kde': robust_kde, 'info': robust_info}
    g = sns.PairGrid(df)
    g.map_diag(diag_methods[diag_kind])
    g.map_upper(tria_methods[upper_kind])
    g.map_lower(tria_methods[lower_kind])
