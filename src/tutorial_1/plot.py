import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from typing import List


#########################################################
#                         PLOT                          #
#########################################################
def cage(ax: plt.Figure, HT: List[np.ndarray]):
    """Plot Homogeneous Transfrom with coordinate system."""
    if len(HT) == 0:
        raise ValueError("List is empty.")

    i = 0
    for ht in HT:
        ax.scatter(ht[0, 3], ht[1, 3], ht[2, 3], c='k')
        plot_axes(ax, ht, name="$O_"+str(i)+"$",
                  axis_name=True, length=0.2)
        i += 1

    # Set the view angles
    ax.view_init(elev=15, azim=-120)

    # Axis limits
    ax.set_xlim([-0.5, 0.5])
    ax.set_ylim([-0.4, 0.4])
    ax.set_zlim([-0.4, 0.4])


def polygon(ax: plt.Figure, HT: List[np.ndarray], color):
    """Draw an area using polygon. First one is not counted."""
    if len(HT) == 0:
        raise ValueError("List is empty.")

    size = len(HT)

    points = []
    for j in range(0, size):
        ht = HT[j]
        t = ht[0:3, 3]
        # plot vertices
        ax.scatter(ht[0, 3], ht[1, 3], ht[2, 3], c='k')
        # plot axes
        plot_axes(ax, ht, name="$O_"+str(j)+"$")

        if j > 0:
            points.append(t)

        if j == size-1:
            points = np.array(points)
            patch = Poly3DCollection([points], facecolor=color, alpha=0.5)
            ax.add_collection3d(patch)

    # Set the view angles
    ax.view_init(elev=15, azim=-120)

    # Axis limits
    ax.set_xlim([0, 3])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-2, 2])


def plot_axes(ax: plt.Figure, ht: np.ndarray, name=None,
              axis_name=False, length=0.15):
    """Plot rotated axes."""
    colors = ("#FF0000", "#00FF00", "#0000FF")  # Colorblind-safe RGB
    R = ht[:3, :3]
    t = ht[:3, 3]
    loc = np.array([t, t])

    for i, (axis, c) in enumerate(zip((ax.xaxis, ax.yaxis, ax.zaxis), colors)):
        axlabel = axis.axis_name
        axis.set_label_text(axlabel)
        line = np.zeros((2, 3))
        line[1, i] = length
        line_rot = R@line.T
        line_plot = line_rot.T + loc
        ax.plot(line_plot[:, 0], line_plot[:, 1],
                line_plot[:, 2], c, zorder=10)
        if axis_name:
            text_loc = line[1]*1.25
            text_loc_rot = R@text_loc.T
            text_plot = text_loc_rot.T + loc[0]
            ax.text(*text_plot, axlabel.upper(), color=c,
                    va="center", ha="center")

    ax.text(t[0]+0.05, t[1]+0.05, t[2], name, color="k", va="center",
            ha="center", fontsize=12, zorder=20)
