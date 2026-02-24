#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 16:47:33 2024
This code writes main keyfiles for simulation of homogenized axon embedded inside EAM that will be used in 
optimization of material properties of EAM. The main keyfile contains the data about nodes and elements of the 
model and includes the material, control, boundary and constraint files to the keyfile and defines the termination
time and maximum time step as parameters based on the rate of deformation. 
@author: maryamma
"""

import numpy as np
import os

# # Read the CSV file into a NumPy array
# csv_file_dir = '/home/maryamma/project/All/ANN/sampling/'
# directory = '/home/maryamma/project/All/ANN/sampling'


def main_keyfile(directory, sample_key_file, modes, rates, max_strain):
    """
    This functions writes main keyfiles for simulation of heterogenized axon embedded inside EAM. Data about nodes and elements of the model are derived from the 
    nsample_key_file and the material, control, boundary and constraint files are inculded manually to the 
    keyfile. Termination time and maximum time step are calculated based on the rate of deformation. 
    :param directory: str, directory of the sample files we want to write the keyfiles for. e.g: 'path/to/dir'
    :param sample_key_file: str, The sample file based on which we want to write the keyfiles. e.g: 'path/to/dir'
    :param modes: list, list of deformations we want to simulate. Available sims are ['compD1', 'compD2', 'shearD1', 'shearD2', 'shearD3', 'tenD1', 'tenD2']
    :param rates: dict, a dictionary of rates we want to simulate and their corresponding experimental definition. Available rates for Xin-Jin are {'0.5': 'low', '5': 'mid', '30': 'high'}
    :param max_strain: int, Maximum strain applied to the models. e.g: 0.2
    :return: Nan; files are saved in all directories that start with 'Sample'
    """
    with open(os.path.join(sample_key_file), 'r') as file:
        lines = file.readlines()
    os.chdir(directory)
    samples = [d for d in sorted(os.listdir(directory))
            if os.path.isdir(os.path.join(directory, d)) and d.startswith('sample')]
    samples.sort(key=lambda x: int(x.replace('sample', '')))
    for sample_num, sample in enumerate(samples):
        for mode in modes:
            for rate in rates:
                print(f'CR_{sample}_{mode}_X{rate}.k')
                if not os.path.exists(f'{sample}/{mode}_X{rate}'):
                    os.makedirs(f'{sample}/{mode}_X{rate}')
                with open(os.path.join(
                        directory, str(sample),f'{mode}_X{rate}' , f'CC_key_file_X{rate}.k'), 'w') as file:
                    for line_num, line in enumerate(lines):
                        if line.startswith('*NODE'):
                            file.write('*PARAMETER\n')
                            termt = max_strain/float(rate)
                            # import pdb; pdb.set_trace()
                            file.write(f'    RTERMT{termt:10.4}\n')
                            file.write('*PARAMETER\n')
                            rts = 3*10**(-4)/float(rate)
                            file.write(f'       RTS{rts:10.3}\n')
                            file.write('*PARAMETER\n')
                            DISP = (8.04*(mode == 'compD1') + 8.04*(mode == 'shearD3') + 8.04*(mode == 'tenD1') 
                                    + 2*(mode == 'compD2') + 2*(mode == 'shearD1') + 2*(mode == 'shearD2') +  + 2*(mode == 'tenD2')) * max_strain/2
                            file.write(f'     RDISP{DISP:10.3}\n')
                            file.write('*INCLUDE\n')
                            file.write(f'../../rate/BC_{mode}.k\n')
                        file.write(line)

if __name__ == "__main__":
    pass