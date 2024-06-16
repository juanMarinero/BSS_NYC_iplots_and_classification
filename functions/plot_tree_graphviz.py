#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :


from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus


def plot_tree_graphviz(clf, feature_names, class_names):
    dot_data = StringIO()
    export_graphviz(
        clf,
        out_file=dot_data,
        filled=True,
        rounded=True,
        feature_names=feature_names,
        special_characters=True,
        class_names=class_names,
    )
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    dot_data.getvalue()

    return Image(
        graph.create_png()
    )  # abrir en pestaña nueva, esperar a que se cargue y enfocar (zoom in)
