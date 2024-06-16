#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_hist2d(
    df,
    period,
    custom_order,
    x_col="start_lat",
    y_col="start_lng",
    simple_plot=False,
    num_bins_x=20,
    num_bins_y=20,
):

    if simple_plot:
        h = plt.hist2d(
            _df_merge[x_col], _df_merge[y_col], cmap="RdYlBu"
        )  # number of fires in each bin
        plt.colorbar(h[3])
        return

    fig = plt.figure(figsize=(16, 16))
    grid = plt.GridSpec(num_bins_x, num_bins_y, hspace=-0.2, wspace=0.2)
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_xticks([])  # Remove x-axis ticks
    main_ax.set_yticks([])  # Remove y-axis ticks

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], frameon=False)
    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], frameon=False)
    # print(x_hist.get_position())
    x_hist_position = x_hist.get_position()
    new_y_position = [x_hist_position.x0, 0.06, x_hist_position.width, 0.07]  # play
    x_hist.set_position(new_y_position)

    # ---------
    # 2D histogram as a heatmap
    hist2d, xedges, yedges = np.histogram2d(
        df[x_col], df[y_col], bins=(num_bins_x, num_bins_y)
    )
    im = main_ax.imshow(
        hist2d.T,
        extent=(xedges[0], xedges[-1], yedges[0], yedges[-1]),
        aspect="auto",  # adjust aspect ratio automatically
        origin="lower",
        cmap="RdYlBu",
    )
    cbar_ax = fig.add_axes(
        [0.95, 0.2, 0.02, 0.58]
    )  # position and size of the colorbar axis
    cbar = plt.colorbar(im, cax=cbar_ax)

    # to be included left extreme in pd.cut
    # print(xedges,yedges)
    xedges[0] -= 1e-5
    yedges[0] -= 1e-5

    # ---------
    # x_hist and y_hist
    group_col = period

    # Binning data based on edges
    df["x_bin"] = pd.cut(df[x_col], bins=xedges, right=True)
    df["y_bin"] = pd.cut(df[y_col], bins=yedges, right=True)

    # Grouping by x_bin and group_col and summing up
    grouped_data_x = (
        df.groupby(["x_bin", group_col], observed=False)[x_col]
        .count()
        .unstack()
        .reindex(columns=custom_order)
    )
    grouped_data_y = (
        df.groupby(["y_bin", group_col], observed=False)[y_col]
        .count()
        .unstack()
        .reindex(columns=custom_order)
    )

    grouped_data_x.plot(kind="bar", stacked=True, ax=x_hist, width=0.5)
    grouped_data_y.plot(kind="barh", stacked=True, ax=y_hist, width=0.5)

    x_hist.invert_yaxis()
    y_hist.invert_xaxis()

    x_hist.legend(
        loc="center left", bbox_to_anchor=(1.3, 9), fontsize=20
    ).get_frame().set_visible(
        False
    )  # legend in x_hist, locate it to the far right
    y_hist.get_legend().remove()  # remove the legend from y_hist

    x_hist.set_xlabel("Latitud", fontsize=30)
    y_hist.set_ylabel("Longitud", fontsize=30)

    x_hist.tick_params(which="both", length=0)
    y_hist.tick_params(which="both", length=0)

    return
