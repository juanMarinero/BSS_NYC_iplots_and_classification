#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import pandas as pd


def plot_feature_importances(clf, x_cols):
    """
    visualizar la importancia de las características (features) en un modelo de
    clasificación basado en árboles de decisión (clf)
    """
    xcol = "Atributos"
    ycol = "Importancia"

    feat_import = {xcol: x_cols, ycol: clf.feature_importances_}
    dataset = pd.DataFrame(data=feat_import)

    _df = dataset.sort_values(by="Importancia", ascending=True)
    ax = _df.plot.barh(x=xcol, y=ycol, figsize=(15, 8))
    tresh = "0.001"
    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=8,
            padding=2,
            labels=[
                f"{k:.3f}" if k >= float(tresh) else "<" + tresh for k in _df[ycol]
            ],
        )
    return ax
