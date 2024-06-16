#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_freq(
    df,
    col_main,
    cols_twin=["temp", "RH", "wind", "rain"],
    colors=["red", "teal", "grey", "green"],
    figsize=(8, 5),
    custom_order=None,
    title="Media cada ",
    func="mean",
):

    n = len(cols_twin)
    if n > len(colors):
        cmap = plt.get_cmap("tab10")  # You can choose from various colormaps
        colors = [cmap(i) for i in np.linspace(0, 1, n)]
    rightPositions = [1 + 0.2 * i for i in range(n)]

    freq = df[col_main].value_counts().reindex(custom_order)

    # main bar plot for the month counts
    fig, ax1 = plt.subplots(figsize=figsize)
    ax1.bar(freq.index.values, freq, alpha=0.3)
    ax1.set_ylabel("Counts")
    if func == "std":
        title = "Variación estándar cada "
    ax1.set_title(title + col_main)

    # twin axes
    if n == 0:
        return fig, ax1
    axes = [ax1]  # Include the main axis in the list
    for i, column in enumerate(cols_twin):
        ax2 = ax1.twinx()  # create a twin axis
        if func == "mean":
            means = df.groupby(col_main)[column].mean()  # mean of column for each month
        elif func == "std":
            means = df.groupby(col_main)[column].std()  # mean of column for each month
        means = means.reindex(freq.index)
        ax2.plot(
            means.index,
            means,
            label=column,
            color=colors[i],
            alpha=0.5,
            linestyle="--",
            marker="*",
        )
        ax2.set_ylabel(func + " " + column, fontsize=18, color=colors[i])
        ax2.spines["right"].set_position(("axes", rightPositions[i]))
        for label in ax2.get_yticklabels():
            label.set_color(colors[i])
        axes.append(ax2)
    plt.legend(handles=[l for ax in axes[1:] for l in ax.lines], labels=cols_twin)

    return fig, ax1
