# This script is designed to write .pml code for setting up
# custom gradient colorings for select residues in a structure
import pandas as pd
import numpy as np
from encode_gradients import *



def encode_selections(csv_path, col_path):
    
    """
    Obtains encoded colors.
    """

    sele_data = pd.read_csv(csv_path, header=None)
    sele_data = np.array(sele_data, dtype=object)
    
    col_data = pd.read_table(col_path, header=None)
    col_data[1] = [eval(i) for i in col_data[1]]
    col_data = np.array(col_data)

    cols = assign_ncolor(
        values=sele_data[:,2],
        breaks=col_data[:,0],
        break_colors=col_data[:,1],
        return_dict=True
        )
    
    sele_data = [list(i) + [cols[i[2]]] for i in sele_data]
    
    return sele_data



def create_selections(sele_data):

    """
    Generates lines for .pml script residue selections
    CSV columns should be chain, position, value
    """

    create_selection = lambda x:(
        f'select {x[0]}_{x[1]}, chain {x[0]} and resi {x[1]}'
        )
    selections = [create_selection(i) for i in sele_data]
    
    return selections



def set_colors(sele_data):

    """
    Generates lines for .pml script color values.
    """

    set_color = lambda x:(
        f'set_color {x[0]}_{x[1]}_color=[{x[3][0]}, {x[3][1]}, {x[3][2]}]'
    )
    colors = [set_color(i) for i in sele_data]

    return colors



def color_selections(sele_data):

    """
    Generates lines for .pml script residue coloring.
    """

    color_selection = lambda x: f'color {x[0]}_{x[1]}_color, {x[0]}_{x[1]}'
    colored_selections = [color_selection(i) for i in sele_data]
    
    return colored_selections



def write_pml_from_lsts(outpath, append=False, *args):

    """
    Writes out lists to .pml file.
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
