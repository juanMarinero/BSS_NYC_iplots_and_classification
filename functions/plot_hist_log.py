#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_hist_log(df, bins, figsize=(10, 6), n_bars=200):
    # Plot histogram
    fig = plt.figure(figsize=figsize)
    plt.hist(df["count"], bins=n_bars, color="skyblue", alpha=0.7, log=True)
    plt.xscale("log")  # Set x-axis to log scale

    # Plot vertical lines at percentile boundaries
    for bin_edge in bins:
        plt.axvline(x=bin_edge, color="red", linestyle="--")

    # Add labels and title
    plt.xlabel("Count")
    plt.ylabel("Frecuencia")
    plt.title("Histograma con marcas de percentiles")
    plt.grid(True)

    return fig
