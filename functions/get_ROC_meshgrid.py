#  vim: set foldmethod=indent foldcolumn=8 :
#!/usr/bin/env python3

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier

try:  # make it explicit that import is from current directory of current script, not from home folder of main script (or notebook)
    from .plot_confussion_matrix_F1score_matrix_ROC_curve import (
        plot_confussion_matrix_F1score_matrix_ROC_curve,
    )
except ImportError:
    # run current script from current directory: if __name__ == "__main__":
    from plot_confussion_matrix_F1score_matrix_ROC_curve import (
        plot_confussion_matrix_F1score_matrix_ROC_curve,
    )


def f01(
    cv,
    model,
    model_kwargs,
    print_scores,
    matrix_conf_and_metrics_plot,
    X_resampled,
    y_resampled,
):
    if cv == 0:
        cv = None
    clf, scores = plot_confussion_matrix_F1score_matrix_ROC_curve(
        model(**model_kwargs),
        X_resampled,
        y_resampled,
        cv=cv,
        matrix_conf_and_metrics_plot=matrix_conf_and_metrics_plot,
        print_basic_scores=print_scores,
        figsize=(18, 5),
    )
    return scores


def f01_plot(
    cv_range, param_range, grid_values, param_name, title, ax, i, divide_by_xticks
):
    im = sns.heatmap(
        grid_values, cmap="RdYlBu", ax=ax, xticklabels=param_range, yticklabels=cv_range
    )
    ax.set_xlabel(param_name)
    ax.set_ylabel("cv")
    ax.set_title(title)
    if i > 0:
        ax.yaxis.set_tick_params(length=0)

    # Customize xticklabels to show only half
    xticks = ax.get_xticks()
    xtick_labels = [
        label if i % divide_by_xticks == 0 else ""
        for i, label in enumerate(param_range)
    ]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)


def get_ROC_meshgrid(
    X_resampled,
    y_resampled,
    cv_range,
    param_range,
    param_name="min_samples_split",
    score_index=[-1],
    print_scores=False,
    matrix_conf_and_metrics_plot=False,
    figsize=(12, 4),
    divide_by_xticks=2,
    model=DecisionTreeClassifier,
):

    n_plots = len(score_index)
    cv_grid, k_grid = np.meshgrid(cv_range, param_range)
    title_array = ["Accuracy", "Recall", "F1-Score", "ROC"]
    grid_values = [np.zeros_like(cv_grid, dtype=float) for _ in range(n_plots)]
    for i, cv in enumerate(cv_range):
        if print_scores:
            print(40 * "- " + f"\ncv = \033[1m{cv}\033[0m\n")
        for j, param_val in enumerate(param_range):
            if print_scores:
                print(40 * "- " + f"\nmin_samples_split = \033[1m{val}\033[0m\n")
            model_kwargs = {param_name: param_val}
            scores = f01(
                cv,
                model,
                model_kwargs,
                print_scores,
                matrix_conf_and_metrics_plot,
                X_resampled,
                y_resampled,
            )  # scores are [acc, recall, f1, roc_auc]

            for index, index_val in enumerate(score_index):
                grid_values[index][j, i] = scores[index_val]

    fig, ax = plt.subplots(1, n_plots, figsize=figsize, sharey=True)
    plt.subplots_adjust(wspace=0.5)
    for index, index_val in enumerate(score_index):
        f01_plot(
            cv_range,
            param_range,
            grid_values[index].T,
            param_name,
            title_array[index_val],
            ax[index],
            index,
            divide_by_xticks,
        )
