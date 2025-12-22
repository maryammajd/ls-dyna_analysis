#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 2 11:34:51 2024

This code gets the coordinates of beam elements saved by ls-prepost plots,
along with the keyfile in which the elements are saved in, and calculates the 
strain of each element.

The files you need: 
save the x-, y- and z-coordination of the beam nodes (or all nodes) as beam_x, 
beam_y, beam_z, respectively.
provide the keyfile where the elements are saved in as keyfile.k

@author: maryamma
"""

import json
import os
import numpy as np
import pdb; pdb.set_trace()


source_dir = "/home/maryamma/project/dardel/CR/60.56_notaufail/"
# dirs = [d for d in sorted(os.listdir(source_dir))
        # if os.path.isdir(os.path.join(source_dir, d))]
dirs = ['tenD1/']
# label = ["Cortex", "Myelin", "Node-of-Ranvier"]
colors = ['red', 'blue', 'purple', 'pink', 'yellow', 'orange', 'salmon']
# markers = ['o', '*']
section = ["beam_x", 'beam_y', "beam_z"]
# strain_rate = 0.02  # 0.0067
# rate_disc = {'X0.5': 'low', 'X5': 'mid', 'X30': 'high'}

print('starting simulation; make sure that you have changed the area parameter based on the model :)')


def separator(folder, sect):
    val_1, val_0 = {}, {}
    node_coord = {}
    section_num = []
    node_num = []
    file_path = os.path.join(folder, sect)
    # Read lines that start with space or 'endcurve'
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if "#" in line:
                node_num.append(line.split()[0])
            if "@" in line:
                # print(line)
                # Split the line into words using whitespace as a separator
                words = line.split()
                # Find the index of the search word in the list of words
                index = words.index('@')
                # Print the word that follows the search word (if available)
                if index < len(words) - 1:
                    section_num.append(words[index + 1])
            if line.startswith(' ') or line.strip() == 'endcurve':
                lines.append(line)
    # Join the filtered lines into a single string
    text = ''.join(lines)

    parts = text.split('endcurve')
    # Adjusting to re-add 'endcurve' to the parts
    parts= [part.strip().replace('endcurve', '')
             for part in parts if part.strip()]
    # Displaying the separated parts
    for idx, part in enumerate(parts):
        # print(f"Part {idx}:\n{part}\n")
        node = node_num[idx]
        temp = np.genfromtxt(part.splitlines(), dtype=float)
        val_0[node] = np.array(temp[0::1, 0])
        val_1[node] = np.array(temp[0::1, 1])

    return val_0, val_1

for dir_num, dir in enumerate(dirs):
    try: 
        current_dir = source_dir + '/' + dir 
        time, x = separator(current_dir, section[0]) 
        time, y = separator(current_dir, section[1])
        time, z = separator(current_dir, section[2])
    except:
        print(f'stress and strain files for {current_dir} does not exist')


def map_node_to_element(file_path):
    part_separated = {}
    reading_elements = False  # <--- NEW FLAG

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Detect start of an element block
            if line.startswith("*ELEMENT"):
                ele_type = line[9:]
                reading_elements = True
                continue

            # Detect start of a NEW keyword → stop reading element lines
            if line.startswith("*") and not line.startswith("*ELEMENT"):
                reading_elements = False
                continue

            # Skip comments or empty lines
            if not reading_elements or line.startswith("$") or not line:
                continue

            # Now we are inside an ELEMENT block
            parts = list(map(int, line.split()))
            part_separated.setdefault(ele_type, []).append(parts)

    return part_separated

def distance_nodes(x, y, z, node1, node2):
    distance = np.sqrt((x[str(node1)] - x[str(node2)])**2 + (y[str(node1)] - y[str(node2)])**2 + (z[str(node1)] - z[str(node2)])**2)
    return distance

part_nodes = map_node_to_element("keyfile.k")
# part_10 = find_nodes_used_in_part(part_nodes, target_part=10)
# shared_node_coords = {nid: nodes[nid] for nid in part_10 if nid in nodes}


list_of_beams= [i[:4] for i in np.array(part_nodes['BEAM'])]

tau_beams = [beam for beam in list_of_beams if beam[1]==5]
nf_beams = [beam for beam in list_of_beams if beam[1]==3]
dist_dict = {}
for beam in tau_beams:
    print(beam)
    dist_dict[beam[0]] = distance_nodes(x, y, z, beam[2], beam[3])

broken_elements = []
for element_num, dist in dist_dict.items():
    if np.any((dist - dist[0]) / dist[0] >= 1) :
        broken_elements.append(element_num)
        # print(element_num, dist)

print(broken_elements)