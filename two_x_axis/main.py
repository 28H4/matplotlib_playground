#!/usr/bin/env python
"""This script plots an overview of different plasma applications and their typical
pressure range respectively the occurring mean free path using 2 x-axes."""

import matplotlib.pyplot as plt

import matplotlib.patches as mpatch

from scipy import constants


def set_up_base_fig(figsize=(14/2.5, 5/2.5), **ax_kwargs):
    """
    Set up the base figure with invisble y axis.

    Parameters
    ----------
    figsize: tuple
        figsize in inches.
    ax_kwargs
        Kwars passed to ax.set().

    Returns
    -------
    matplotlib.axes.Axes
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.set(**ax_kwargs)

    ax.axes.get_yaxis().set_visible(False)

    return ax


def x_tranform_functions(temperature=400, cross_section=1E-18):
    """Provides functions for converting pressure to mean free path and vice versa."""

    def pressure_to_mean_free_path(pressure):
        return (constants.k * temperature) / (pressure * cross_section) * 1E6

    def mean_free_path_to_pressure(mean_free_path):
        return (constants.k * temperature) / (mean_free_path * cross_section) * 1E-6

    return pressure_to_mean_free_path, mean_free_path_to_pressure


if __name__ == '__main__':
    ax = set_up_base_fig(
        # title='Typical pressure ranges for different plasma applications',
        xlabel='Pressure [Pa]',
        xscale='log',
        xlim=(0.01, 1000),
        ylim=(-0.1, 4.1),
    )

    secax = ax.secondary_xaxis('top', functions=x_tranform_functions())
    secax.set_xlabel('Mean free path [µm]')

    ALPHA=0.2
    FACECOLOR='green'

    rectangles = {'PVD': mpatch.Rectangle((0.05, 0), 3.95, 0.9, alpha=ALPHA,
                                          facecolor=FACECOLOR),
                  'ICP': mpatch.Rectangle((0.5, 1), 9.5, 0.9, alpha=ALPHA,
                                          facecolor=FACECOLOR),
                  'CCP': mpatch.Rectangle((1, 2), 49, 0.9, alpha=ALPHA,
                                          facecolor=FACECOLOR),
                  'CVD': mpatch.Rectangle((100, 3), 700, 0.9, alpha=ALPHA,
                                          facecolor=FACECOLOR)
                  }

    for r in rectangles:
        ax.add_artist(rectangles[r])

    HEIGHT = 0.25
    ax.text(0.3, HEIGHT, 'PVD')
    ax.text(0.7, 1+HEIGHT, 'dry etching (ICP)')
    ax.text(2, 2+HEIGHT, 'dry etching (CCP)')
    ax.text(170, 3+HEIGHT, 'PE-CVD')

    plt.tight_layout()
    plt.show()
