#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA


def plot_pca_variance(pca, n_components, figsize=(5, 3)):
    fig, ax1 = plt.subplots(figsize=figsize)

    pca_xticks = ["PC-" + str(k) for k in range(n_components)]
    bars = ax1.bar(pca_xticks, height=pca.explained_variance_ratio_)
    plt.bar_label(bars, fmt="%.2f")
    ax2 = ax1.twinx()
    ax2.plot(np.cumsum(pca.explained_variance_ratio_), "r--")
    ax2.grid(visible=False)

    ax1.set_xlabel("number of components")
    ax1.set_ylabel("explained variance")
    ax2.set_ylabel("cumulative explained variance")

    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_visible(False)

    return pca_xticks


def plot_PCA_coef_portion(pca, cols, n_components, legendbool=True):
    pca_xticks = ["PC-" + str(k) for k in range(n_components)]
    df_coef = pd.DataFrame(
        np.abs(pca.components_[:n_components, :]),
        index=pca_xticks,
        columns=cols,
    )

    # https://github.com/juanMarinero/bicingBarcelona/blob/master/main.ipynb
    df_coef.fillna(0)
    df_coef_portion = df_coef.copy()
    for index, row in df_coef_portion.iterrows():
        df_coef_portion.loc[index] = df_coef.loc[index] / df_coef.loc[index].sum() * 100

    ax = df_coef_portion.plot(kind="bar", stacked=True, figsize=(25, 20))

    ax.legend(
        bbox_to_anchor=(1.2, 0.5),
        ncol=1,
        markerscale=12,  # marker-size
        prop={"size": 22},
    )
    if not legendbool:
        ax.get_legend().remove()

    y_offset = -4
    index_num = 0
    for index, row in df_coef_portion.iterrows():
        df_coef_cumsum = np.cumsum(row)
        i = 0
        for col, val in df_coef_portion.loc[index].items():
            if val > 4:
                ax.text(
                    index_num,
                    df_coef_cumsum.iloc[i] + y_offset,
                    f"{val:.1f}%\n{col}",
                    ha="center",
                    weight="bold",
                    fontsize=20,
                )
                # print(index_num, df_coef_cumsum[i] + y_offset, round(val))
            i += 1
        index_num += 1
    ax.tick_params(labelsize=24)

    ax.plot(100 * np.cumsum(pca.explained_variance_ratio_), "--", linewidth=3)

    for spine in ax.spines.values():
        spine.set_visible(False)

    return df_coef
