#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:25:31 2024
This code reads the json files containing the data about 'centers', 'PBC_faces',
'PBC_edges', 'corners' nodes and writes the file for *CONSTRAINED_MULTIPLE_GLOBAL
in LS-DYNA.
To get the json files run the code called step2_json_node_maker.py
@author: maryamma
"""

import json
import os

def write_PBC(dir):
    # Replace with the desired file format (e.g., ".txt")
    files = ['centers', 'PBC_faces', 'PBC_edges', 'corners']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0


    couples = [['front', 'back'], ['right', 'left'], ['top', 'bottom']]
    output_file_path = os.path.join(dir, 'CONSTRAINED_MULTIPLE_GLOBAL.txt')
    with open(output_file_path, 'w') as TextOut:
        for params in files:
            # print(globals()[params])
            if params == 'centers':
                # Write the *CONSTRAINED_MULTIPLE_GLOBAL header
                for axes in range(1, 4):
                    cmg_id += 1
                    TextOut.write('*CONSTRAINED_MULTIPLE_GLOBAL\n')
                    TextOut.write(f'{cmg_id:10.0f}\n')
                    for couple_num in range(len(couples)):
                        TextOut.write('         2\n')
                        # 1
                        node1 = globals()[
                            'centers'][couples[couple_num][0]]
                        TextOut.write(f'{node1:10.0f}')
                        # direction and coefficient
                        TextOut.write(f'{axes:10.0f}{1.0:10.1f}\n')
                        # 2
                        node2 = globals()[
                            'centers'][couples[couple_num][1]]
                        TextOut.write(f'{node2:10.0f}')
                        # direction and coefficient
                        TextOut.write(f'{axes:10.0f}{1.0:10.1f}\n')
            elif params == 'PBC_faces':
                for axes in range(1, 4):
                    for face in (globals()['PBC_faces']):
                        RefNode_face = globals()[
                            'centers'][face.split('_')[0].lower()]
                        cmg_id += 1
                        TextOut.write('*CONSTRAINED_MULTIPLE_GLOBAL\n')
                        TextOut.write(f'$ {face} \n')
                        TextOut.write(f'{cmg_id:10.0f}\n')
                        for node_pair in range(len(globals()['PBC_faces'][face])):
                            TextOut.write('         3\n')
                            node1 = globals()[
                                'PBC_faces'][face][node_pair][0]
                            TextOut.write(f'{node1:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{1.0:10.1f}\n')
                            # 2
                            node2 = globals()[
                                'PBC_faces'][face][node_pair][1]
                            TextOut.write(f'{node2:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{-1.0:10.1f}\n')
                            TextOut.write(f'{RefNode_face:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{-2.0:10.1f}\n')
            elif params == 'PBC_edges':
                for axes in range(1, 4):
                    for edge in (globals()['PBC_edges']):
                        # print(edge)
                        RefNode1_edge = (globals()['centers'][edge.split('_')[1]])
                        RefNode2_edge = (globals()['centers'][edge.split('_')[2]])
                        cmg_id += 1
                        TextOut.write('*CONSTRAINED_MULTIPLE_GLOBAL\n')
                        TextOut.write(f'$ {edge}\n')
                        TextOut.write(f'{cmg_id:10.0f}\n')
                        for node_pair in range(len(globals()['PBC_edges'][edge])):
                            TextOut.write('         4\n')
                            node1 = globals()[
                                'PBC_edges'][edge][node_pair][0]
                            TextOut.write(f'{node1:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{1.0:10.1f}\n')
                            # 2
                            node2 = globals()[
                                'PBC_edges'][edge][node_pair][1]
                            TextOut.write(f'{node2:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{-1.0:10.1f}\n')
                            TextOut.write(f'{RefNode1_edge:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{-2.0:10.1f}\n')
                            TextOut.write(f'{RefNode2_edge:10.0f}')
                            # direction and coefficient
                            TextOut.write(f'{axes:10.0f}{-2.0:10.1f}\n')
            elif params == 'corners':
                for axes in range(1, 4):
                    cmg_id += 1
                    TextOut.write('*CONSTRAINED_MULTIPLE_GLOBAL\n')
                    TextOut.write(f'{cmg_id:10.0f}\n')
                    for rl in [0, 1]:
                        for tb in [0, 1]:
                            node1_name = 'corner_' + couples[0][0] + '_' + \
                                couples[1][rl] + '_' + couples[2][tb]
                            node2_name = 'corner_' + couples[0][1] + '_' + \
                                couples[1][1-rl] + '_' + couples[2][1-tb]
                            node1 = globals()[
                                'corners'][node1_name][0]
                            node2 = globals()[
                                'corners'][node2_name][0]
                            # print(node1, node2)
                            RefNode1_corner = globals()[
                                'centers'][couples[0][0]]
                            RefNode2_corner = globals()[
                                'centers'][couples[1][rl]]
                            RefNode3_corner = globals()[
                                'centers'][couples[2][tb]]
                            # print(node1_name, RefNode1_corner, RefNode2_corner, RefNode3_corner)
                            TextOut.write('         5\n')
                            # node 1 data
                            TextOut.write(f'{node1:10.0f}')
                            TextOut.write(f'{axes:10.0f}{1.0:10.1f}\n')
                            # node 2 data
                            TextOut.write(f'{node2:10.0f}')
                            TextOut.write(f'{axes:10.0f}{-1.0:10.1f}\n')
                            # ref node 1 data
                            TextOut.write(f'{RefNode1_corner:10.0f}')
                            TextOut.write(f'{axes:10.0f}{-2.0:10.1f}\n')
                            # ref node 2 data
                            TextOut.write(f'{RefNode2_corner:10.0f}')
                            TextOut.write(f'{axes:10.0f}{-2.0:10.1f}\n')
                            # ref node 3 data
                            TextOut.write(f'{RefNode3_corner:10.0f}')
                            TextOut.write(f'{axes:10.0f}{-2.0:10.1f}\n')

if __name__ == "__main__":
    pass