#  vim: set foldmethod=indent foldcolumn=8 :
#!/usr/bin/env python3

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display_html
from matplotlib.ticker import MaxNLocator
from mpl_toolkits import mplot3d

from sklearn.model_selection import train_test_split, validation_curve


def plot_validation_curve(
    model,
    X,
    y,
    param_range=np.arange(2, 4),
    param_name="min_samples_split",
    cv_range=np.arange(2, 4),
    test_size=0.2,
):

    title = "validation score"

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=24
    )
    if isinstance(X_test, pd.DataFrame):
        X_test = X_test.values
    if isinstance(X_train, pd.DataFrame):
        X_train = X_train.values

    N = len(cv_range)
    val_score_arr = np.zeros((N, param_range.size), dtype=float)
    train_score_arr = val_score_arr.copy()
    fig, ax = plt.subplots(1, N, figsize=(12, 3), sharey=True)
    for index, cv in enumerate(cv_range):
        axi = ax[index]
        train_score, val_score = validation_curve(
            model,
            X_train,
            y_train,
            param_name=param_name,
            param_range=param_range,
            cv=cv,
        )
        val_score_arr[index] = np.median(val_score, 1)
        # median because each cv has its own scores
        train_score_arr[index] = np.median(train_score, 1)
        axi.plot(
            param_range, np.median(train_score, 1), color="blue", label="training score"
        )
        axi.plot(param_range, np.median(val_score, 1), color="red", label=title)
        axi.set_title(f"cv = {cv}", fontsize=6)
        axi.tick_params(axis="x", labelsize=6)
        # axi.set_xlabel(param_name, fontsize=6)
        if index == 0:
            axi.set_ylabel(title)
        else:
            axi.yaxis.set_tick_params(length=0)
        if index == (N - 1):
            axi.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        for spine in axi.spines.values():
            spine.set_visible(False)

    plt.suptitle(param_name, y=-0.1)
    min_score = np.min([np.min(train_score_arr), np.min(val_score_arr)])
    max_score = np.max([np.max(train_score_arr), np.max(val_score_arr)])
    min_score = 0 if not isinstance(min_score, (float, int)) else min_score
    max_score = 1 if not isinstance(min_score, (float, int)) else max_score
    del train_score_arr
    for index, _ in enumerate(cv_range):
        axi = ax[index]
        axi.set_ylim(min_score, max_score)
    plt.tight_layout(pad=0.4)
    plt.show()

    val_score_arr[val_score_arr < 0] = 0  # Subtract Unless Negative Then Return 0

    Xplot, Yplot, Zplot = param_range, cv_range, val_score_arr
    df = pd.DataFrame(Zplot.T, index=Xplot, columns=Yplot)
    df_percentage = 100 * df
    # highlight_max(axis=1) --> max each row
    # highlight_min(axis=1) --> min each row
    display_html(
        df_percentage.T.style.highlight_max(axis=1)
        .highlight_min(color="lightblue", axis=1)
        .format("{:.01f}")
        .set_caption(title)
    )

    # ------------------------------------------------------------
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    plt.subplots_adjust(wspace=3.5)

    i = 0
    sns.heatmap(df.T, cmap="coolwarm", annot=False, ax=ax[i])
    ax[i].set_xlabel(param_name)
    ax[i].set_ylabel("cv")
    ax[i].set_title(title)

    i += 1
    contours = ax[i].contour(Xplot, Yplot[::-1], Zplot, 3, colors="black")
    ax[i].clabel(contours, inline=True, fontsize=8)
    ax[i].imshow(
        Zplot[::-1],
        extent=[Xplot.min(), Xplot.max(), Yplot.min(), Yplot.max()],
        origin="lower",
        cmap="coolwarm",
        alpha=0.9,
        aspect="auto",
    )
    ax[i].set_xlabel(param_name)
    ax[i].set_yticks([])
    ax[i].set_yticklabels([])
    # ax[i].colorbar()
    ax[i].set_title(title)

    i += 1
    ax[i].plot(Yplot, Zplot.max(axis=1), "o-", color="blue")
    ax[i].set_xlabel("cv")
    ax2 = ax[i].twinx()
    ax2.plot(Yplot, param_range[Zplot.argmax(axis=1)], "o-", color="red")
    for label in ax[i].get_yticklabels():
        label.set_color("blue")
    for label in ax2.get_yticklabels():
        label.set_color("red")
    ax[i].set_ylabel("max validation score", fontsize=14, color="blue")
    ax2.set_ylabel(f"respective\n{param_name}", fontsize=14, color="red")
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    if 0:
        i += 1
        Xmesh, Ymesh = np.meshgrid(Xplot, Yplot)
        ax[i] = plt.axes(projection="3d")
        ax[i].plot_surface(
            Xmesh,
            Ymesh,
            Zplot,
            rstride=1,
            cstride=1,
            cmap="coolwarm",
            linewidth=0,
            antialiased=False,
        )
        ax[i].view_init(70, 15)

    plt.tight_layout(pad=0.1)
    plt.show()

    return None


