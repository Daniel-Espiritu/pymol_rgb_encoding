# This script was designed to test this python package
# Authored by Daniel Espiritu, August 11th, 2025
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),'..'
            )))
from encode_gradients import *
from pml_selection_encoding import *
from cbar import plt_colorbar



# Get the directory of the current file
cur_dir = os.path.dirname(__file__)

# Build an absolute path to test data
test_fpath = os.path.join(cur_dir, "./input_data/test.csv")
test_fpath = os.path.abspath(test_fpath)

# Build an absolute path to test colour selections
test_col_fpath = os.path.join(cur_dir, "./input_data/test_cols.tsv")
test_col_fpath = os.path.abspath(test_col_fpath)

# Build an absolute path for file to write out
pml_outpath = os.path.join(cur_dir, "./output_data/test.pml")
pml_outpath = os.path.abspath(pml_outpath)

with open(pml_outpath, 'w') as f:
    f.write('reinit\n')
    f.write('fetch 7K5Y\n')
    f.write('\n')
    f.write('bg_color white\n')
    f.write('\n')
    f.write('hide everything, chain M\n')
    f.write('hide everything, chain N\n')
    f.write('\n')

encode_pml_rgb(test_fpath, test_col_fpath, pml_outpath, append=True)

with open(pml_outpath, 'a') as f:
    f.write('\n')
    f.write('color gray70, chain I\n')
    f.write('color gray70, chain J\n')
    f.write('deselect\n')


# Build an absolute path for color bar plot to write out
grad_outpath = os.path.join(cur_dir, "./output_data/test_gradient.tiff")
grad_outpath = os.path.abspath(grad_outpath)

plt_colorbar(test_col_fpath, grad_outpath)
