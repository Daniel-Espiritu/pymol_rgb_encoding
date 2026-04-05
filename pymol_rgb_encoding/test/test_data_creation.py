# This script was made to generate test data for script usage
# This script creates ./test.csv and ./test_cols.tsv
# Authored by Daniel Espiritu, August 11th 2025
import os
import numpy as np



def parse_pdb_chains_resids(pdb_path):

    chains = {}

    with open(pdb_path, "r") as f:

        for line in f:

            if line.startswith(("ATOM", "HETATM")):

                chain = line[21].strip()
                resi = line[22:26].strip()
                resi = int(resi)

                if chain not in chains:
                    chains[chain] = []

                if resi not in chains[chain]:
                    chains[chain].append(resi)

    return chains



if __name__ == '__main__':

    # Get the directory of the current file
    cur_dir = os.path.dirname(__file__)

    # Build an absolute path to 7k5y.pdb
    pdb_path = os.path.join(cur_dir, "./7k5y.pdb")
    pdb_path = os.path.abspath(pdb_path)

    # Build dictionary
    chain_dict = parse_pdb_chains_resids(pdb_path)

    test_data = []


    # Generate samples from a normal distribution
    samples = np.random.normal(loc=0, scale=20, size=20000)
    samples = samples[(samples >= -100) & (samples <= 100)]

    for key in chain_dict.keys():

        if key in ['U', 'C', 'G', 'D', 'H', 'A', 'E', 'B', 'F']:

            for resi in chain_dict[key]:

                rand_val = np.random.choice(samples)
                test_data.append([key, resi, rand_val])

    test_data = np.array(test_data, dtype=object)

    test_col_data = [
        [-100,[0,0,255]], # Blue
        [0,[255,255,255]], # White
        [100, [255,0,0]] # Red
        ]

    test_col_data = np.array(test_col_data, dtype=object)

    test_outpath = os.path.join(cur_dir, "./input_data/test.csv")
    test_outpath = os.path.abspath(test_outpath)

    test_col_outpath = os.path.join(cur_dir, "./input_data/test_cols.tsv")
    test_col_outpath = os.path.abspath(test_col_outpath)

    with open(test_outpath, 'w') as f:

        for i in range(0, len(test_data)):

            line_data = test_data[i]

            if i != (len(test_data) - 1):
                line = f'{line_data[0]}, {line_data[1]}, {line_data[2]}\n'
            
            else:
                line = f'{line_data[0]}, {line_data[1]}, {line_data[2]}'

            f.write(line)

    with open(test_col_outpath, 'w') as f:

        for i in range(0, len(test_col_data)):

            line_data = test_col_data[i]

            if i != (len(test_col_data) - 1):
                line = f'{line_data[0]}\t{line_data[1]}\n'
            
            else:
                line = f'{line_data[0]}\t{line_data[1]}'

            f.write(line)

    with open(test_outpath, 'r') as f:
        print(f.readlines()[0])

    with open(test_col_outpath, 'r') as f:
        print(f.readlines()[0])
