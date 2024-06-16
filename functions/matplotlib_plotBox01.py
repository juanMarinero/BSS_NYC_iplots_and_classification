#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.express as px

import warnings

from sklearn import datasets


def matplotlib_plotBox01(
    df,
    cols=None,
    plotlyBool=True,
    percentilesTitle=[5, 95],
    proportionInPercentiles=95,
    fig_width=13,
    row_height=4,
    fig_cols=5,
    plotTitle="",
    shareyBool=False,
    color_low_percentage="k",  # "r"
):
    if cols is None:
        cols = df.columns

    fig_rows = int(np.ceil(len(cols) / fig_cols))
    figsize = (fig_width, row_height * fig_rows)

    if plotlyBool:
        figsize = np.array(figsize) * 75  # pixels. Later applied on fig.update_layout()
        fig = make_subplots(fig_rows, fig_cols, shared_yaxes=shareyBool)
    else:
        fig, axs = plt.subplots(fig_rows, fig_cols, figsize=figsize, sharey=shareyBool)
        fig.subplots_adjust(hspace=0.4, wspace=0.4)

    for i in range(fig_cols * fig_rows):
        row = i // fig_cols
        col = i % fig_cols

        if i < len(cols):
            colName = cols[i]
            x = df[colName].values

            percentiles = [np.percentile(x, k) for k in percentilesTitle]
            percent_range = (
                1 - ((sum(x < percentiles[0]) + sum(x > percentiles[-1])) / len(x))
            ) * 100
            color = "k"
            if percent_range < proportionInPercentiles:
                color = color_low_percentage
            subplotTitle = f"{percent_range:.0f}% ∈ {[round(g,2) for g in percentiles]}"
            if not plotlyBool:
                subplotTitle = r"$\bf{" + colName + "}$" + "\n" + subplotTitle

            if plotlyBool:
                row += 1  # start at cell (1,1)
                col += 1
                fig_boxplot = px.box(df[[colName]], points="all")
                fig_boxplot.update_traces(
                    marker=dict(size=5, opacity=0.5), selector=dict(type="box")
                )
                for trace in fig_boxplot.data:
                    fig.add_trace(trace, row=row, col=col)
                fig.update_xaxes(title_text=subplotTitle, row=row, col=col)

            else:
                ax = axs[row, col]
                sns.boxplot(
                    x,
                    showfliers=False,
                    showbox=False,
                    whis=[2.5, 97.5],
                    color="w",
                    ax=ax,
                )
                violin_fig = sns.violinplot(x, inner="point", linewidth=0.01, ax=ax)
                plt.setp(violin_fig.collections, alpha=0.5)
                violin_fig.set_title(subplotTitle, color=color)
                ax.set_xticks([])
        else:
            if not plotlyBool:
                axs[row, col].axis("off")

    if plotlyBool:
        fig.update_layout(
            title=plotTitle,
            width=figsize[0],
            height=figsize[1],
            margin=dict(l=10, r=10, b=10, t=30),
        )
        fig.show()

    return fig


def getDF(targetCol="MEDV"):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if targetCol == "MEDV":
            data = datasets.load_boston()
        if targetCol == "target":
            data = datasets.load_diabetes()
    X = data["data"]  # 13 features
    y = data["target"]  # median value: MEDV
    df = pd.concat(
        [
            pd.DataFrame(data=X, columns=data["feature_names"]),
            pd.DataFrame(data=y, columns=[targetCol]),
        ],
        axis="columns",
    )
    return df


if __name__ == "__main__":
    print("matplotlib_plotBox01!")

    shareyBool = False

    # play
    if 0:
        df = getDF()  # boston housing
    if 1:
        df = getDF("target")  # diabetes
    if 0:
        df = getDF("target")  # diabetes
        df.drop(columns=["target", "sex"], inplace=True)  # to set shareyBool
        shareyBool = True

    with warnings.catch_warnings():
        matplotlib_plotBox01(df, plotlyBool=False, shareyBool=shareyBool)
        plt.show()

    with warnings.catch_warnings():
        print("In Jupyter-Notebook")
        print(
            "Nota. Si no se renderiza a HTML: restart kernel y reejecuta esta celda y de las que depende."
        )
        matplotlib_plotBox01(df, plotlyBool=True, shareyBool=shareyBool)
