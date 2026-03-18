# This script was made to write .pml code
# for residue custom color selections
# Authored by Daniel Espiritu, August 11th, 2025
import numpy
import os
from encode_gradients import *
from pml_selection_encoding import *

def encode_pml_rgb(data_fpath, color_fpath, pml_outpath, append=False):

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
