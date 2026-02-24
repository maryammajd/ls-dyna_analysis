#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on some date on 2024

This code takes the directory and name of the keyfile you want to extract the nodes for and saves all 
the data about nodes including their coordinates in Nodes.k file :)

@author: maryamma
"""


import json
import os, sys

sys.path.append(os.path.abspath('/run/media/maryamma/One Touch/FEM/Python_codes/study4/auto'))

from auto_ALL_step1_node_extract import node_extract
from auto_EAMAXON_step2_json_node_maker_del_noMidSurf import json_for_params
from aauto_EAMAXON_step3_write_PBC_from_json import write_PBC
from auto_Boundary_for_all import *

source_dir = input(
    "Please enter the directory: ")
model =input(
    "Please enter the keyfile: ")

# source_dir = '/run/media/maryamma/One Touch/FEM/Python_codes/PBC/tests'
# model = 'test_model.k'


# code_dir = "/run/media/maryamma/One Touch/FEM/Python_codes/PBC/auto/"
# material_keyfile(source_dir, source_dir)

node_extract(source_dir, model)
print('extracting nodes')
json_for_params(source_dir)
write_PBC(source_dir)
# directory =source_dir+ '/rate'
print(directory)
if not os.path.exists(directory):
    print('creating rate folder')
    os.makedirs(directory)

# compressionD1(source_dir, 0.30, 'rate')
# compressionD2(source_dir, 0.30, 'rate')
# tensionD1(source_dir, 0.30, 'rate')
# tensionD2(source_dir, 0.30, 'rate')
# shearD1(source_dir, 0.30, 'rate')
# shearD2(source_dir, 0.30, 'rate')
# shearD3(source_dir, 0.30, 'rate')


