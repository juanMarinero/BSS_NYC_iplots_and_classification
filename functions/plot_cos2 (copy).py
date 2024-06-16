#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :


# --------------------------------------------
# MineriaDatos: JuanGabrielMarineroTarazona-PEC1.html
# cos2
# --------------------------------------------


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def get_close_vectors(x_arr, y_arr, threshold=0.1):  # closeness
    def distance(x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    n = len(x_arr)
    grouped_indices = [[k] for k in list(range(n))]

    # Iterate through each pair of points
    for i in range(n):
        # Initialize a list to store indices of points close to the current point
        close_indices = []

        # Compare the current point with all other points after it
        for j in range(n):
            if j != i:
                # Calculate the distance between the current point and the other point
                dist = distance(x_arr[i], y_arr[i], x_arr[j], y_arr[j])

                # If the distance is below the threshold, add the index of the other point to close_indices
                if dist < threshold:
                    close_indices.append(j)

        # If there are close points, add their indices to grouped_indices
        if close_indices:
            grouped_indices[i].extend(close_indices)
        # print(grouped_indices)

    return [np.sort(k).tolist() for k in grouped_indices]


def shift_annot(x, y, shift=-0.15):
    # to make  annotations clearer, make it go further away
    return (
        x + shift * (x < 0) + (-shift) * (x > 0),
        y + shift * (y < 0) + (-shift) * (y > 0),
    )


def plot_cos2(
    pca,
    cols,
    figsize=(6, 5),
    cbar_bool=True,
    cmap="RdYlBu",
    radius_min_to_annotate=0.001,  # TODO
    closeness=0.1,
):
    # Extract explained variance ratio and eigenvectors
    exp_var = pca.explained_variance_ratio_
    eigenvectors = pca.components_

    # Scale eigenvectors
    s_eigenvectors = np.sqrt(exp_var)[:, np.newaxis] * eigenvectors
    #  s_eigenvectors = eigenvectors.T * np.sqrt(exp_var)  # equivalent

    # Plot correlation circle
    fig, ax = plt.subplots(figsize=figsize)
    ax.set(frame_on=False, xticks=[], yticks=[], xlabel="X-axis", ylabel="Y-axis")
    shift = 0.2
    ax.set_xlim([-1 - shift, 1 + shift])
    ax.set_ylim([-1 - shift, 1 + shift])
    radius_arr = [
        np.sqrt(s_eigenvectors[0, i] ** 2 + s_eigenvectors[1, i] ** 2)
        for i in range(len(cols))
    ]

    radius_arr_sorted = list(np.sort(radius_arr)[::-1])
    sorted_indices = np.argsort(radius_arr)[::-1]
    cols_sorted = [cols[i] for i in sorted_indices]
    s_eigenvectors_sorted = s_eigenvectors[:, sorted_indices]

    max_radius = radius_arr[np.argmax(radius_arr)]
    cmap = plt.cm.get_cmap(cmap)
    x_arr, y_arr = list(), list()
    for i, var_name in enumerate(cols_sorted):
        x = s_eigenvectors_sorted[0, i] / max_radius
        y = s_eigenvectors_sorted[1, i] / max_radius
        x_arr.append(x)
        y_arr.append(y)
    grouped_indices = get_close_vectors(x_arr, y_arr, threshold=closeness)
    max_radius = 1.0  # not to scale arrows
    c = np.array(radius_arr_sorted) / max_radius
    sc = ax.scatter(x_arr, y_arr, c=c, cmap=cmap, s=0.1)
    sc.set_clim(min(c), max(c))  # sc.set_clim(0, 1)
    if cbar_bool:
        cbar = fig.colorbar(sc, shrink=0.7, pad=0.15)
        cbar.set_ticklabels(
            ["{:.2f}".format(tick) for tick in cbar.get_ticks()]
        )  # FixedFormatter warning
    colors = sc.to_rgba(c)

    var_name_len_max = int(np.max([len(k) for k in cols]))
    for i, var_name in enumerate(cols_sorted):
        r = radius_arr_sorted[i] / max_radius
        ax.arrow(
            0,
            0,
            x_arr[i],
            y_arr[i],
            head_width=0.05,
            head_length=0.1,
            fill=True,
            lw=0.2,
            fc=colors[i],
            ec="k",
            alpha=1,
            label=f"{var_name:{var_name_len_max}s} {r:.3f}",
        )
        if (r > radius_min_to_annotate) and (grouped_indices[i][-1] == i):
            if len(grouped_indices[i]) < 4:
                text = " ~ ".join(
                    [cols_sorted[indices] for indices in grouped_indices[i]]
                )
            else:
                text = "\n".join(
                    [cols_sorted[indices] for indices in grouped_indices[i]]
                )
            ax.annotate(
                text,
                xy=shift_annot(x_arr[i], y_arr[i]),
                ha="center",
                va="center",
                fontfamily="monospace",
                fontsize=10,
                weight="bold",
            )  # , color=colors[i])

    legend = plt.legend(
        loc="upper center", bbox_to_anchor=(1.7, 0.7), frameon=False, title="Radio"
    )
    for text in legend.get_texts():
        text.set_fontfamily("monospace")
    plt.xlabel("PC1 ({:.1f}%)".format(exp_var[0] * 100))
    plt.ylabel("PC2 ({:.1f}%)".format(exp_var[1] * 100))

    return c, cols_sorted


def plot_cos2_coord(
    cos2,
    coord,
    cols,
    figsize=(12, 6),
    sharey=False,  # "row",
    closeness=[0.02, 0.005],
    radius_min_to_annotate=0.0000001,  # TODO
):

    fig, axs = plt.subplots(1, 2, figsize=figsize, sharey=sharey)
    fig.subplots_adjust(wspace=0.5)

    def plot_ax(ax, x, cols, xlabel, ylabel, title, closeness):
        x = x.T

        x_arr = x.values[:, 0]
        y_arr = x.values[:, 1]
        ax.scatter(x_arr, y_arr, marker="x")

        grouped_indices = get_close_vectors(x_arr, y_arr, threshold=closeness)

        for i, text in enumerate(cols):
            r = np.sqrt(x_arr[i] ** 2 + y_arr[i] ** 2)
            if (r > radius_min_to_annotate) and (grouped_indices[i][-1] == i):
                if len(grouped_indices[i]) < 4:
                    text = " ~ ".join([cols[indices] for indices in grouped_indices[i]])
                else:
                    text = "\n".join([cols[indices] for indices in grouped_indices[i]])
                ax.annotate(text, (x.values[i, 0], x.values[i, 1]), weight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=20)

    plot_ax(axs[0], coord, cols, "PC-0", "PC-1", "coord", closeness[0])
    plot_ax(
        axs[1],
        cos2,
        cols,
        "Squared Cosine PC-0",
        "Squared Cosine PC-1",
        "cos2",
        closeness[1],
    )

    for ax in axs:
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(y=0, color="black", linestyle="--", alpha=0.2)
        ax.axvline(x=0, color="black", linestyle="--", alpha=0.2)

    return fig, axs
