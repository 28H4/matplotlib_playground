#!/usr/bin/env python
"""This script is used to draw the data from some file. This file contains one
column for x-data and several columns for y-data. The data points are connected
by a spline for better visualization. The color cycler of matplotlib is
adjusted so that no color is repeated."""

# pylint: disable=invalid-name

import linecache

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splev, splrep


def get_line(file_path, header_line=0, uppercase=True, delimiter=None):
    """
    Reads a line of a file and splits it.

    Parameters
    ----------
    file_path : str
        Path of the file which is read.
    header_line : int, optional, default: 0
        Line which is to be split.
    uppercase : bool, optional, default: True
        If True strings will be uppercase.
    delimiter : str or None, optional, default: None
        Specifies the used delimiter. The default, None, corresponds
        to consecutive whitespace.

    Returns
    -------
    list
        A list of strings representing the columns of the line.

    """
    line = linecache.getline(file_path, header_line + 1)

    if uppercase:
        line = line.upper()

    return line.split(delimiter)


def set_color_cycle(ax, colormap, num_colors):
    """
    Changes the color cycle of an matplotlib.axes.Axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object whose color cycle properties are changed.
    colormap : matplotlib.colors.Colormap or str or None
        Colormap from which the colours for the color cycle are selected.
    num_colors : int
        Number of colors, which the color cycle will contain.

    """
    cm = plt.get_cmap(colormap)
    ax.set_prop_cycle(color=[cm(1. * i / num_colors) for i in range(num_colors)])


def plot_fit(ax, x, y, linear_condition=None, **kwargs):
    """
    Plot the B-spline representation of the x-y curve.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes instance used to plot the fit.
    x : scalar or array-like, shape (n,)
        The x data positions.
    y : scalar or array-like, shape (n,)
        The y data positions.
    linear_condition : function, optional, default: None
        If linear_condition is True, the applied fit will be linear.
        (Example: lambda x, y: y[-1] < 10).
    color : color, optional, default: last used color.
        Color.
    splrep_kwargs : dict, optional, default: None
        Kwargs which will be passed to scipy.interpolate .splrep().
    """
    if linear_condition:
        if linear_condition(x, y):
            kwargs["splrep_kwargs"] = dict(kwargs.get("splrep_kwargs", {}), k=1)

    spl = splrep(x, y, **kwargs.get("splrep_kwargs", {}))
    x_interpolation = np.linspace(**kwargs.get("linspace_kwargs"))

    ax.plot(x_interpolation, splev(x_interpolation, spl),
            color=kwargs.get("color", plt.gca().collections[-1].get_facecolors()[0]))


def plot_data(x_data, y_data, labels, **kwargs):
    """
    Plots x-y1-y2-y3...yN as scatter plot and adds B-spline fit.

    Parameters
    ----------
    x_data : scalar or array-like, shape (n, 1)
        The x data positions (Same for all y datasets).
    y_data : scalar or array-like, shape (n, m)
        The y data positions.
    labels : iterable object
        Used for labeling the individual y-data sets in the legend.
    color_cycle : optional, default: None
        A Colormap instance or registered colormap name.
    linear_condition : optional, default: viridis
        If linear_condition is True, the applied fit will be linear.
        (Example: lambda x, y: y[-1] < 10).
    fig_kwargs : dict, optional, default: None
        Kwargs which will be passed to plt.subplots().
    ax_kwargs : dict, optional, default: None
        Kwargs which will be passed to ax.set().
    legend_kwargs : dict, optional, default: None
        Kwargs which will be passed to ax.legend().
    """

    fig, ax = plt.subplots(1, 1, **kwargs.get('fig_kwargs'))
    set_color_cycle(ax, kwargs.get('color_cycle', 'viridis'), len(labels))

    for i in range(y_data.shape[1]):
        y = y_data[:, i]
        ax.scatter(x_data, y)
        plt.draw()

        scatter_color = plt.gca().collections[-1].get_facecolors()[0]

        plot_fit(ax, x_data, y,
                 linear_condition=kwargs.get('linear_condition'),
                 linspace_kwargs={'start': x_data[0], 'stop': x_data[-1]}
                 )

        ax.plot([], [], '-o', label=labels[i - 1], color=scatter_color)

    ax.set(**kwargs.get('ax_kwargs'))

    ax.legend(**kwargs.get('legend_kwargs'))

    plt.tight_layout()


if __name__ == "__main__":
    FILE_PATH = r'example_data.pid'
    LABELS = get_line(FILE_PATH)
    DATA = np.genfromtxt(FILE_PATH, skip_header=2)

    AX_KWARGS = {
        "title": "Interaction of the ions with the side walls",
        "xlabel": "Height in hole [µm]",
        "ylabel": "Number of Ions",
        "xlim": (0, 31),
        "ylim": (0, 8000),
    }

    LEGEND_KWARGS = {
        'bbox_to_anchor': (1.05, 1),
        'loc': 'upper left',
        'title': 'Ion flux',
    }

    FIG_KWARGS = {
        "figsize": (15 / 2.5, 10 / 2.5),
    }

    plot_data(x_data=DATA[:, 0] * 1E3,
              y_data=DATA[:, 1:],
              labels=LABELS,
              linear_condition=lambda x, y: y[-1] < 10,
              fig_kwargs=FIG_KWARGS,
              ax_kwargs=AX_KWARGS,
              legend_kwargs=LEGEND_KWARGS,

              )

    plt.show()
