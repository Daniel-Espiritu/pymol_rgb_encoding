# This script is designed to write .pml code for setting up
# custom gradient colorings for select residues in a structure
import pandas as pd
import numpy as np
from encode_gradients import assign_ncolor


def encode_selections(csv_path, col_path):

    """Obtains encoded colors.

    Parameters
    ----------
    csv_path : str
        Path to CSV file where each line details a PDB chain, resi, and a given
        numerical value to be RGB encoded.
    col_path : str
        Path to TSV file where each line details a vale and a corresponding RGB
        code.

    Returns
    -------
    nested list
        Each sub list contains a chain ID, resi, and RGB color code obtained
        from value conversion.
    """

    sele_data = pd.read_csv(csv_path, header=None)
    sele_data = np.array(sele_data, dtype=object)

    col_data = pd.read_table(col_path, header=None)
    col_data[1] = [eval(i) for i in col_data[1]]
    col_data = np.array(col_data)

    cols = assign_ncolor(
        values=sele_data[:, 2],
        breaks=col_data[:, 0],
        break_colors=col_data[:, 1],
        return_dict=True
        )

    sele_data = [list(i) + [cols[i[2]]] for i in sele_data]

    return sele_data


def create_selections(sele_data):

    """Generates lines for .pml script residue selections
    CSV columns should be chain, position, value

    Parameters
    ----------
    sele_data : nested list
        Each sub list contains a chain ID, resi, and RGB color code obtained
        from value conversion. This list is obtained from encode_selections().

    Returns
    -------
    list
        List of strings that can be used to create selections in PyMol.
    """

    create_selection = lambda x: (
        f'select {x[0]}_{x[1]}, chain {x[0]} and resi {x[1]}'
        )
    selections = [create_selection(i) for i in sele_data]

    return selections


def set_colors(sele_data):

    """Generates lines for .pml script color values.

    Parameters
    ----------
    sele_data : nested list
        Each sub list contains a chain ID, resi, and RGB color code obtained
        from value conversion. This list is obtained from encode_selections().

    Returns
    -------
    list
        List of strings that can be used to create custom colors in PyMol.
    """

    set_color = lambda x: (
        f'set_color {x[0]}_{x[1]}_color=[{x[3][0]}, {x[3][1]}, {x[3][2]}]'
    )
    colors = [set_color(i) for i in sele_data]

    return colors


def color_selections(sele_data):

    """Generates lines for .pml script residue coloring.

    Parameters
    ----------
    sele_data : nested list
        Each sub list contains a chain ID, resi, and RGB color code obtained
        from value conversion. This list is obtained from encode_selections().

    Returns
    -------
    list
        List of strings that can be used to color selections with custom
        colors in PyMol.
    """

    color_selection = lambda x: f'color {x[0]}_{x[1]}_color, {x[0]}_{x[1]}'
    colored_selections = [color_selection(i) for i in sele_data]

    return colored_selections


def write_pml_from_lsts(outpath, append=False, *args):

    """Writes out lists to .pml file.

    Parameters
    ----------
    outpath : str
        Path of .pml file to be written to.
    append : bool, optional
         Determines if file in outpath is to be appended (False) or overwritten
         (True).
    *args : nested list
        Sub lists contain lines (str) to be written to a .pml file.

    Returns
    -------
    None
        Writes out to "outpath".
    """

    if append:
        x = 'a'
    else:
        x = 'w'

    with open(outpath, f'{x}') as f:

        for lst in args:

            for i in lst:

                line = f'{i}\n'
                f.write(line)

            f.write('\n')


def encode_pml_rgb(data_fpath, color_fpath, pml_outpath, append=False):

    """ Aggregates previous functions for centralizing .pml file creation

    Parameters
    ----------
    data_fpath : str
        Path to CSV file where each line details a PDB chain, resi, and a given
        numerical value to be RGB encoded.
    color_fpath : str
        Path to TSV file where each line details a vale and a corresponding RGB
        code.
    pml_outpath : str
        Path of .pml file to be written to.
    append : bool, optional
        Determines if file in outpath is to be appended (False) or overwritten
        (True).

    Returns
    -------
    None
        Writes out to "Outpath"
    """

    sele_data = encode_selections(data_fpath, color_fpath)

    selections = create_selections(sele_data)

    colors = set_colors(sele_data)

    colored_selections = color_selections(sele_data)

    write_pml_from_lsts(
        pml_outpath,
        append,
        selections,
        colors,
        colored_selections
        )
