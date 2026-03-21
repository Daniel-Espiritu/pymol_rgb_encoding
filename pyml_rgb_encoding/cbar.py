# This script was made to create a custom color gradient
# bar to acompany custom pymol residue coloring
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize


def plt_colorbar(color_fpath, outpath=None):

    # Read in color data
    col_data = pd.read_table(color_fpath, header=None)

    # Normalize breaks
    original_breaks = col_data[0]
    min_val = min(original_breaks)
    max_val = max(original_breaks)
    break_range = max_val - min_val
    breaks = [(i - min(original_breaks)) / break_range for i in original_breaks]

    # Normalize and reformat colors
    colors = [eval(i) for i in col_data[1]]
    rgb_reformat = lambda x: (x[0]/255, x[1]/255, x[2]/255)
    colors = [rgb_reformat(i) for i in colors]

    # Re-merge breaks and colors
    col_data = [(i, j) for i, j in zip(breaks, colors)]

    # Custom color map
    cmap = LinearSegmentedColormap.from_list('cmap', col_data)

    # Create Normalize object for mapping data → colormap scale
    norm = Normalize(vmin=min_val, vmax=max_val)

    # Create a gradient image using normalized data
    gradient_data = np.linspace(min_val, max_val, 256).reshape(1, -1)

    # Plot gradient
    fig, ax = plt.subplots(figsize=(6, 1))
    im = ax.imshow(gradient_data, aspect='auto', cmap=cmap, norm=norm)
    ax.set_axis_off()

    # Add colorbar with real data values
    cbar = plt.colorbar(
        im,
        ax=ax,
        orientation='horizontal',
        fraction=0.05,
        pad=0.2
    )
    cbar.set_ticks(original_breaks)

    if outpath is not None:
        plt.savefig(outpath, dpi=300, bbox_inches='tight')
        plt.show()

    else:
        plt.show()


if __name__ == '__main__':

    import os

    cur_dir = os.path.dirname(__file__)

    # Build an absolute path to test colour selections
    test_col_fpath = os.path.join(cur_dir, "./test/test_cols.tsv")
    test_col_fpath = os.path.abspath(test_col_fpath)

    plt_colorbar(test_col_fpath)
