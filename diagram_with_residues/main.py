#!/usr/bin/env python
"""Plot x_data-y-diagram including fit and residues (in an additional axes)."""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from numpy.random import default_rng
from scipy import stats


def linear_test_function(slope, y_intercept):
    """Returns linear function f(x_data)=slope * x_data + y_intercept."""
    def function(x):
        return slope * x + y_intercept

    return function


def create_noisy_y_data(x_data, function, sigma=3):
    """Returns noisy y-data for the specified function."""
    rng = default_rng()
    noise = rng.normal(0, sigma, len(x_data))

    return np.apply_along_axis(function, 0, x_data) + noise


if __name__ == '__main__':
    # Create x and y data
    x = np.arange(-10, 11)
    y = create_noisy_y_data(x, linear_test_function(4, 0))

    # Set up fig with two axes
    fig, ax = plt.subplots()
    ax_divider = make_axes_locatable(ax)
    ax_residues = ax_divider.new_vertical(size="30%", pad=0.1, pack_start=True)
    ax.tick_params(labelbottom=False)
    fig.add_axes(ax_residues)

    # Perform fit and get residuals
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    y_residuals = y - (intercept + slope * x)

    # Plot data, fit and residues
    ax.scatter(x, y, label='noisy data')
    ax.plot(x, slope * x + intercept, label='noisy')
    ax_residues.scatter(x, y_residuals, marker="x", label='data')

    # axis settings
    ax.set(ylabel="y label [a.u.]")
    ax_residues.set(xlabel="x label [a.u.]",
                    ylabel="residues [a.u.]",
                    ylim=(-6,6))

    # Set up common legend for all axes
    handles, labels = [], []
    for axis in fig.get_axes():
        handles_, labels_ = axis.get_legend_handles_labels()
        handles.append(handles_)
        labels.append(labels_)

    labels = sum(labels,[])
    handles = sum(handles,[])

    ax.legend(handles, labels, loc="upper left")

    plt.tight_layout()
    plt.show()
