#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text


def adjust_text_subplot(
    ax,
    X,
    Y,
    S,
    force_points=1,
    arrowprops=dict(arrowstyle="-", color="k", lw=0.5),
    textSize=9,
    **kwargs,
):
    texts = [ax.text(x, y, s, size=textSize) for x, y, s in zip(X, Y, S)]
    adjust_textVar = adjust_text(
        texts,
        force_points=force_points,
        arrowprops=arrowprops,
        ax=ax,
        **kwargs,
    )
    return adjust_textVar


def plot_statisticsEachCat(
    df,
    ax=None,
    colCat="month",
    colNum="count",
    ylabel=True,
    custom_order=None,
):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    print(f"{colCat}:")
    meanArr, stdArr = [], []
    unique_values = df.drop(columns=[colNum])[colCat].unique()
    colCatVals = sorted(unique_values, key=lambda x: custom_order.index(x))
    for k in colCatVals:
        x = df.loc[df[colCat] == k, colNum]
        mean = np.mean(x)
        std = np.std(x)
        meanArr.append(mean)
        stdArr.append(std)
        print(f" · {k:13s}: \u03BC {mean:5.2f};  \u03C3 {std:6.2f}")

    scatter = ax.scatter(x=meanArr, y=stdArr)

    adjust_text_subplot(
        ax,
        X=meanArr,
        Y=stdArr,
        S=colCatVals,
        force_points=4,
    )
    ax.set_title(colNum + " ~ " + colCat)
    ax.set_xlabel("mean")
    if ylabel:
        ax.set_ylabel("std")

    return fig, ax
