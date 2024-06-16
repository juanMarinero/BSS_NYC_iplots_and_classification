#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (
    train_test_split,
    cross_val_predict,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
)
import re


def plotROC(y_test, y_test_pred, ax=None, plot_bool=True):
    fpr, tpr, thresholds = roc_curve(y_test, y_test_pred)
    roc_auc = auc(fpr, tpr)

    if plot_bool:
        if ax is None:
            plt.figure(figsize=(5, 5))
            ax = plt.gca()

        lw = 2
        ax.plot(
            fpr,
            tpr,
            color="darkorange",
            lw=lw,
            label="ROC curve (area = %0.2f)" % roc_auc,
        )
        ax.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("False Positive Rate", weight="bold")
        ax.set_ylabel("True Positive Rate", weight="bold")
        ax.set_title("Receiver Operating Characteristic (ROC)", weight="bold")
        ax.legend(loc="lower right")

        if ax is None:
            plt.show()
    return roc_auc


def classification_report_csv(report):
    report_data = []
    lines = report.split("\n")

    def find(lst, match):
        return [i for i, x in enumerate(lst) if x == match]

    lines = lines[0 : find(lines, "")[1]]  # avoid form 2nd blankline on
    for line in lines[2:]:
        row = {}
        row_data = re.split(r"\s+", line)
        # row['class'] = row_data[0]
        row["precision"] = float(row_data[2])
        row["recall"] = float(row_data[3])
        row["f1_score"] = float(row_data[4])
        row["support"] = float(row_data[5])
        report_data.append(row)
        df = pd.DataFrame.from_dict(report_data)
    return df


def plot_get_ax_bold(ax):

    # Set xlabel and ylabel to bold
    ax.set_xlabel(ax.get_xlabel(), fontweight="bold")
    ax.set_ylabel(ax.get_ylabel(), fontweight="bold")

    # Set xticklabels and yticklabels to bold
    for label in ax.get_xticklabels():
        label.set_fontweight("bold")
    for label in ax.get_yticklabels():
        label.set_fontweight("bold")

    return ax


def print_scores(model, X_test, y_test, cv):
    # Cross-validated scores
    scores = cross_val_score(model, X_test, y_test, cv=cv)

    for i, k in enumerate(scores):
        print(f"Accuracy of cross validation {i+1:3d}-th: {k*100:6.2f} %")

    print(
        "\nMean accuracy: %.2f%% (+/- %.2f%%)"
        % (1e2 * scores.mean(), 1e2 * scores.std() * 2)
    )


def plot_confussion_matrix_F1score_matrix_ROC_curve(
    model,
    X,
    y,
    ROC_plot=False,
    matrix_conf_and_metrics_plot=True,
    average="macro",
    fontsize=15,
    figsize=(15, 6),
    test_size=0.2,
    cv=None,
    print_basic_scores=True,
    print_scores_bool=False,
):

    if ROC_plot:
        average = "binary"

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=24
    )
    if isinstance(X_test, pd.DataFrame):
        X_test = X_test.values
    if isinstance(X_train, pd.DataFrame):
        X_train = X_train.values

    if cv is None:
        model.fit(X_train, y_train)  # model training
        y_pred = model.predict(X_test)
    else:
        # Stratified K-Folds cross-validator
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=24)

        if print_scores_bool:
            print(f"cv: {cv}\t\tlen(X_test): {len(X_test)}")
            print_scores(model, X_test, y_test, skf)

        # Cross-validated predictions
        y_pred = cross_val_predict(model, X_test, y_test, cv=skf)

    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm)
    cm_df.index.name = "True"
    cm_df.columns.name = "Predicted"

    if matrix_conf_and_metrics_plot:
        fig, axs = plt.subplots(1, 2 + int(ROC_plot), figsize=figsize)
        plt.subplots_adjust(wspace=0.5)

        # matriz de confusion
        sns.heatmap(
            cm_df,
            annot=True,
            fmt="2d",
            cmap="RdYlBu",
            cbar=False,
            square=True,
            annot_kws={"fontsize": fontsize},
            ax=axs[0],
        )
        plot_get_ax_bold(axs[0])
    else:
        fig = None

    # Calcular la exactitud para los datos de prueba
    acc = accuracy_score(y_test, y_pred)

    # Calcular sensibilidad (recall)
    recall = recall_score(y_test, y_pred, average=average)

    # F1 score
    f1 = f1_score(y_test, y_pred, average=average)

    # classification_report
    report = classification_report(y_test, y_pred)
    if matrix_conf_and_metrics_plot:
        sns.heatmap(
            classification_report_csv(report).iloc[:, :-1] * 100,
            annot=True,
            cmap="RdYlBu",
            fmt=".0f",
            annot_kws={"fontsize": fontsize},
            ax=axs[1],
        )
        plot_get_ax_bold(axs[1])
    
    # ROC curve
    if len(set(y)) <= 2: # ROC just for binary models
        roc_auc = plotROC(y_test, y_pred, ax=axs[2] if ROC_plot else None, plot_bool=ROC_plot)
    else:
        roc_auc = None

    if print_basic_scores:
        print(f"Accuracy del modelo  {acc:.4f}")
        print(f"Recall del modelo    {recall:.4f}")
        print(f"F1 score del modelo  {f1:.4f}")
        if len(set(y)) <= 2:
            print(f"ROC                  {roc_auc:.4f}")

    return model, [acc, recall, f1, roc_auc]
