#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 11:51:25 2024

@author: maryamma
"""

import numpy as np  # type: ignore
import json
import os
import pdb; pdb.set_trace()

def json_for_params(folder): 
    file_path_1 = os.path.join(folder, 'Nodes.k')
    with open(file_path_1, 'r') as file:
        lines = [line.strip() for line in file if not (
            line.startswith('*') or line.startswith('$'))]
        max_line_length = max(len(line.split()) for line in lines)
        padded_lines = []

        for line in lines:
            values = line.split()
            while len(values) < max_line_length:
                values.append('0')  # Add zeros to the end
            padded_lines.append(values)

    # Convert to numpy array
    text1 = np.array(padded_lines, dtype=float)

    # =============================================================================
    # file_path_2 = os.path.join(folder, 'SetNodeCards.k')
    #
    # # Initialize variables
    # sections = {}  # Dictionary to store sections
    # current_section = None  # Current section identifier
    #
    #
    # with open(file_path_2, 'r') as file:
    #     for line in file:
    #         if line.startswith('*SET'):
    #             current_section = None  # Reset the current section identifier
    #         elif current_section is None:
    #             # Use the first line after '*' as the section identifier
    #             current_section = line.strip()
    #             # Initialize an empty list for the section
    #             sections[current_section] = []
    #         elif current_section is not None:
    #             # Add lines to the current section
    #             sections[current_section].append(line.strip())
    # # Now, sections is a dictionary where keys are section identifiers (lines starting with '*')
    # # and values are lists containing the lines for each section.
    #
    #
    # def is_numeric(line):
    #     try:
    #         # Try to convert the line to a list of floats
    #         _ = [float(x) for x in line.strip().split()]
    #         return True
    #     except ValueError:
    #         return False
    #
    #
    # for key, value in sections.items():
    #     if key[0] != '$':
    #         array_each_line = []
    #         for i in range(0, len(value)):
    #             if is_numeric(value[i]):
    #                 array_each_line.append(np.array(value[i].split(), dtype=float))
    #         globals()[key] = np.concatenate(array_each_line, axis=None)
    #
    # =============================================================================

    NodeLookUpTable = np.round(text1, 3)

    distances = {}
    # Input distances
    # for key, value in set_nodes.items():
    #     if key in ['BACK', 'RIGHT', 'TOP']:
    distances['FRONT'] = max(NodeLookUpTable[:, 1])
    distances['RIGHT'] = max(NodeLookUpTable[:, 2])
    distances['TOP'] = max(NodeLookUpTable[:, 3])
    distances['BACK'] = min(NodeLookUpTable[:, 1])
    distances['LEFT'] = min(NodeLookUpTable[:, 2])
    distances['BOTTOM'] = min(NodeLookUpTable[:, 3])
    # print('distances', distances)

    dimensions = {'zdir':distances['TOP']-distances['BOTTOM'] , 'ydir': distances['RIGHT']- distances['LEFT'], 'xdir': distances['FRONT']- distances['BACK']}
    set_nodes = {}
    # all the nodes in each face. Center nodes, edge and corners will be removed from the final face groups.

    set_nodes['BACK'] = NodeLookUpTable[np.round(NodeLookUpTable[:, 1], 3) == np.round(
        distances['BACK'], 3), 0]
    set_nodes['FRONT'] = NodeLookUpTable[np.round(NodeLookUpTable[:, 1], 3) == np.round(
        distances['FRONT'], 3), 0]
    set_nodes['RIGHT'] = NodeLookUpTable[np.round(NodeLookUpTable[:, 2], 3) == np.round(
        distances['RIGHT'], 3), 0]
    set_nodes['LEFT'] = NodeLookUpTable[np.round(NodeLookUpTable[:, 2], 3) == np.round(
        distances['LEFT'], 3), 0]

    set_nodes['TOP'] = NodeLookUpTable[np.round(NodeLookUpTable[:, 3], 3) == np.round(
        distances['TOP'], 3), 0]
    set_nodes['BOTTOM'] = NodeLookUpTable[np.round(NodeLookUpTable[:, 3], 3) == np.round(
        distances['BOTTOM'], 3), 0]

    # print(set_nodes)
    def process_and_count_data(data):
        data_vec = data[data != 0]
        num_elem = len(data_vec)
        return data_vec, num_elem


    edges = {}

    matches_tr = np.isin(set_nodes['TOP'], set_nodes['RIGHT'])
    edges['edge_top_right'] = set_nodes['TOP'][matches_tr]

    matches_br = np.isin(set_nodes['BOTTOM'], set_nodes['RIGHT'])
    edges['edge_bottom_right'] = set_nodes['BOTTOM'][matches_br]

    matches_tf = np.isin(set_nodes['TOP'], set_nodes['FRONT'])
    edges['edge_top_front'] = set_nodes['TOP'][matches_tf]

    matches_bf = np.isin(set_nodes['BOTTOM'], set_nodes['FRONT'])
    edges['edge_bottom_front'] = set_nodes['BOTTOM'][matches_bf]


    matches_fr = np.isin(set_nodes['FRONT'], set_nodes['RIGHT'])
    edges['edge_front_right'] = set_nodes['FRONT'][matches_fr]

    matches_fl = np.isin(set_nodes['FRONT'], set_nodes['LEFT'])
    edges['edge_front_left'] = set_nodes['FRONT'][matches_fl]

    edges = {key: [elem for elem in value if elem != 0]
            for key, value in edges.items()}

    # print(edges)
    import pdb; pdb.set_trace()


    corners = {}
    corners['corner_front_right_top'] = set_nodes['TOP'][np.isin(
        set_nodes['TOP'], set_nodes['RIGHT']) & np.isin(set_nodes['TOP'], set_nodes['FRONT'])]
    corners['corner_front_left_top'] = set_nodes['TOP'][np.isin(
        set_nodes['TOP'], set_nodes['LEFT']) & np.isin(set_nodes['TOP'], set_nodes['FRONT'])]
    corners['corner_back_right_top'] = set_nodes['TOP'][np.isin(
        set_nodes['TOP'], set_nodes['RIGHT']) & np.isin(set_nodes['TOP'], set_nodes['BACK'])]
    corners['corner_back_left_top'] = set_nodes['TOP'][np.isin(
        set_nodes['TOP'], set_nodes['LEFT']) & np.isin(set_nodes['TOP'], set_nodes['BACK'])]
    corners['corner_front_right_bottom'] = set_nodes['BOTTOM'][np.isin(
        set_nodes['BOTTOM'], set_nodes['RIGHT']) & np.isin(set_nodes['BOTTOM'], set_nodes['FRONT'])]
    corners['corner_front_left_bottom'] = set_nodes['BOTTOM'][np.isin(
        set_nodes['BOTTOM'], set_nodes['LEFT']) & np.isin(set_nodes['BOTTOM'], set_nodes['FRONT'])]
    corners['corner_back_right_bottom'] = set_nodes['BOTTOM'][np.isin(
        set_nodes['BOTTOM'], set_nodes['RIGHT']) & np.isin(set_nodes['BOTTOM'], set_nodes['BACK'])]
    corners['corner_back_left_bottom'] = set_nodes['BOTTOM'][np.isin(
        set_nodes['BOTTOM'], set_nodes['LEFT']) & np.isin(set_nodes['BOTTOM'], set_nodes['BACK'])]
    corners = {key: [elem for elem in value if elem != 0]
            for key, value in corners.items()}


    # print(corners)

    set_node_data = {}
    for key, value in set_nodes.items():
        set_node_data[key + '_vec'], set_node_data[key +
                                                '_len'] = process_and_count_data(value)


    # Create a lookup table
    centers = {}
    # print([(distances['BACK']+distances['FRONT'])/2, distances['LEFT'],
    #     (distances['TOP'] + distances['BOTTOM'])/2])
    # Loop to find centers
    for i in range(len(NodeLookUpTable)):
        if (NodeLookUpTable[i, 1:4] == [distances['BACK'], round((distances['RIGHT']+distances['LEFT'])/2, 4), round((distances['TOP'] + distances['BOTTOM'])/2, 4)]).all():
            # print('BK', NodeLookUpTable[i, 0])
            centers['back'] = NodeLookUpTable[i, 0]
        if (NodeLookUpTable[i, 1:4] == [distances['FRONT'], round((distances['RIGHT']+distances['LEFT'])/2, 4), round((distances['TOP'] + distances['BOTTOM'])/2, 4)]).all():
            # print('F', NodeLookUpTable[i, 0])
            centers['front'] = NodeLookUpTable[i, 0]
        if (NodeLookUpTable[i, 1:4] == [round((distances['BACK']+distances['FRONT'])/2, 4), distances['RIGHT'], round((distances['TOP'] + distances['BOTTOM'])/2, 4)]).all():
            # print('R', NodeLookUpTable[i, 0])
            centers['right'] = NodeLookUpTable[i, 0]
        if (NodeLookUpTable[i, 1:4] == [round((distances['BACK']+distances['FRONT'])/2, 4), distances['LEFT'], round((distances['TOP'] + distances['BOTTOM'])/2, 4)]).all():
            # print('L', NodeLookUpTable[i, 0])
            centers['left'] = NodeLookUpTable[i, 0]
        if (NodeLookUpTable[i, 1:4] == [round((distances['BACK']+distances['FRONT'])/2, 4), round((distances['RIGHT']+distances['LEFT'])/2, 4), distances['TOP']]).all():
            # print('T', NodeLookUpTable[i, 0])
            centers['top'] = NodeLookUpTable[i, 0]
        if (NodeLookUpTable[i, 1:4] == [round((distances['BACK']+distances['FRONT'])/2, 4), round((distances['RIGHT']+distances['LEFT'])/2, 4), distances['BOTTOM']]).all():
            # print('BM', NodeLookUpTable[i, 0])
            centers['bottom'] = NodeLookUpTable[i, 0]
    # =============================================================================
    #     if (NodeLookUpTable[i, 1:4] == [round((distances['BACK']+distances['FRONT'])/2, 4), round((distances['RIGHT']+distances['LEFT'])/2, 4), round((distances['TOP'] + distances['BOTTOM'])/2, 4)]).all():
    #         centers['center'] = NodeLookUpTable[i, 0]
    # =============================================================================
        if (NodeLookUpTable[i, 1:4] == [distances['FRONT'], round((distances['RIGHT']+distances['LEFT'])/2, 4), distances['TOP']]).all():
            centers['FT'] = NodeLookUpTable[i, 0]
        if (NodeLookUpTable[i, 1:4] == [round((distances['FRONT']+distances['BACK'])/2, 4),
                                        round((distances['RIGHT']+distances['LEFT'])/2, 4),
                                        round((distances['TOP'] + distances['BOTTOM'])/2, 4)]).all():
            centers['midpoint'] = NodeLookUpTable[i, 0]
    # print(centers)

    # print(set_nodes.keys())

    edges['TOP'] = np.isin(set_nodes['TOP'], set_nodes['RIGHT']) | np.isin(
        set_nodes['TOP'], set_nodes['LEFT']) | np.isin(set_nodes['TOP'], set_nodes['FRONT']) | np.isin(set_nodes['TOP'], set_nodes['BACK']) | np.isin(set_nodes['TOP'], centers['top'])
    edges['FRONT'] = np.isin(set_nodes['FRONT'], set_nodes['RIGHT']) | np.isin(
        set_nodes['FRONT'], set_nodes['LEFT']) | np.isin(set_nodes['FRONT'], set_nodes['TOP']) | np.isin(set_nodes['FRONT'], set_nodes['BOTTOM']) | np.isin(set_nodes['FRONT'], centers['front'])
    edges['RIGHT'] = np.isin(set_nodes['RIGHT'], set_nodes['FRONT']) | np.isin(
        set_nodes['RIGHT'], set_nodes['BACK']) | np.isin(set_nodes['RIGHT'], set_nodes['TOP']) | np.isin(set_nodes['RIGHT'], set_nodes['BOTTOM']) | np.isin(set_nodes['RIGHT'], centers['right'])

    set_node_data['TOP_vec'] = set_node_data['TOP_vec'][~edges['TOP']]
    set_node_data['FRONT_vec'] = set_node_data['FRONT_vec'][~edges['FRONT']]
    set_node_data['RIGHT_vec'] = set_node_data['RIGHT_vec'][~edges['RIGHT']]
    


    corner_top_right = np.isin(edges['edge_top_right'], [
        corners['corner_front_right_top'][0], corners['corner_back_right_top'][0]])
    corner_bottom_right = np.isin(edges['edge_bottom_right'], [
        [corners['corner_front_right_bottom'][0], corners['corner_back_right_bottom'][0]]])
    corner_top_front = np.isin(edges['edge_top_front'], [
        [corners['corner_front_right_top'][0], corners['corner_front_left_top'][0]]])
    corner_bottom_front = np.isin(edges['edge_bottom_front'], [
        [corners['corner_front_right_bottom'][0], corners['corner_front_left_bottom'][0]]])
    corner_front_right = np.isin(edges['edge_front_right'], [
        [corners['corner_front_right_top'][0], corners['corner_front_right_bottom'][0]]])
    corner_front_left = np.isin(edges['edge_front_left'], [
        [corners['corner_front_left_top'][0], corners['corner_front_left_bottom'][0]]])  
    
    

    edges['edge_top_right'] = np.array(edges['edge_top_right'])[~corner_top_right]
    edges['edge_bottom_right'] = np.array(edges['edge_bottom_right'])[
        ~corner_bottom_right]
    edges['edge_top_front'] = np.array(edges['edge_top_front'])[~corner_top_front]
    edges['edge_bottom_front'] = np.array(edges['edge_bottom_front'])[
        ~corner_bottom_front]
    edges['edge_front_right'] = np.array(edges['edge_front_right'])[
        ~corner_front_right]
    edges['edge_front_left'] = np.array(edges['edge_front_left'])[
        ~corner_front_left]

    # Remove the mid surface from faces and edges:
    middle_surface = NodeLookUpTable[np.round(NodeLookUpTable[:, 1], 3) == np.round(round((distances['FRONT']+distances['BACK'])/2, 4), 3), 0]
    set_node_data['TOP_vec'] = np.array(set_node_data['TOP_vec'][~np.isin( set_node_data['TOP_vec'], middle_surface)])
    set_node_data['RIGHT_vec'] = np.array(set_node_data['RIGHT_vec'][~np.isin(set_node_data['RIGHT_vec'], middle_surface)])
    edges['edge_top_right'] = np.array(edges['edge_top_right'])[~np.isin(np.array(edges['edge_top_right']), middle_surface)]
    edges['edge_bottom_right'] = np.array(edges['edge_bottom_right'])[~np.isin(np.array(edges['edge_bottom_right']), middle_surface)]



    PBC_edges = {}

    PBC_edges['edge_top_right_bottom_left'] = find_correspondent_nodes(NodeLookUpTable, 
        edges['edge_top_right'], [0, -1, -1]*np.round([0,
                                                    (distances['RIGHT'] - distances['LEFT']), (distances['TOP'] - distances['BOTTOM'])], 3))


    PBC_edges['edge_bottom_right_top_left'] = find_correspondent_nodes(NodeLookUpTable, 
        edges['edge_bottom_right'], [0, -1, 1]*np.round([0,
                                                        (distances['RIGHT'] - distances['LEFT']), (distances['TOP'] - distances['BOTTOM'])], 3))

    PBC_edges['edge_top_front_bottom_back'] = find_correspondent_nodes(NodeLookUpTable, 
        edges['edge_top_front'],  [-1, 0, -1]*np.round([(distances['FRONT'] - distances['BACK']),
                                                        0, (distances['TOP'] - distances['BOTTOM'])], 3))

    PBC_edges['edge_bottom_front_top_back'] = find_correspondent_nodes(NodeLookUpTable, 
        edges['edge_bottom_front'],  [-1, 0, 1]*np.round([(distances['FRONT'] - distances['BACK']),
                                                        0, (distances['TOP'] - distances['BOTTOM'])], 3))

    PBC_edges['edge_front_right_back_left'] = find_correspondent_nodes(NodeLookUpTable, 
        edges['edge_front_right'],   [-1, -1, 0]*np.round([(distances['FRONT'] - distances['BACK']),
                                                        (distances['RIGHT'] - distances['LEFT']), 0], 3))

    PBC_edges['edge_front_left_back_right'] = find_correspondent_nodes(NodeLookUpTable, 
        edges['edge_front_left'],  [-1, 1, 0]*np.round([abs(distances['FRONT'] - distances['BACK']),
                                                        abs(distances['RIGHT'] - distances['LEFT']), 0], 3))
    # print(PBC_edges)
    


    # Create a lookup table
    NodeLookUpTable = np.round(text1, 4)
    for key, value in distances.items():
        if key.upper() in ['FRONT', 'RIGHT', 'TOP']:

            set_node_data[key + '_offset'] = [abs(value - distances['BACK']) if key == 'FRONT' else 0,
                                            abs(value - distances['LEFT']) if key == 'RIGHT' else 0, abs(value - distances['BOTTOM']) if key == 'TOP' else 0]
            # print(key, set_node_data[key + '_offset'])
    PBC = {}
    for key in set_nodes.keys():
        # print(key)
        if key.upper() in ['FRONT', 'RIGHT', 'TOP']:
            # print(key)
            # print('offset is ', [2, 2, 2]*np.round(np.array(
            #     NodeLookUpTable[centers['midpoint'] == NodeLookUpTable[:, 0], 1:4]), 3))
            PBC[key] = find_correspondent_nodes(NodeLookUpTable, 
                set_node_data[key + '_vec'], [-1, -1, -1]*np.array(set_node_data[key + '_offset']))
            # print(key, ' is ready')


    json_file_1 = folder + '/centers.json'
    # # print the resulting dictionary
    with open(json_file_1, 'w') as file:
        json.dump(centers, file, indent=4)
        print('centers saved')

    json_file_2 = str(folder) + '/PBC_faces.json'
    # Save the resulting dictionary
    with open(json_file_2, 'w') as file:
        json.dump(PBC, file, indent=4)
        print('faces saved')


    json_file_3 = folder + '/PBC_edges.json'
    # # print the resulting dictionary
    with open(json_file_3, 'w') as file:
        json.dump(PBC_edges, file, indent=4)
        print('edges saved')

    json_file_4 = folder + '/corners.json'
    # # print the resulting dictionary
    with open(json_file_4, 'w') as file:
        json.dump(corners, file, indent=4)
        print('corners saved')

    json_file_4 = folder + '/corners.json'
    # # print the resulting dictionary
    with open(json_file_4, 'w') as file:
        json.dump(corners, file, indent=4)
        print(corners, folder)
        print('corners saved')


    json_file_5 = folder + '/dimensions.json'
    # # print the resulting dictionary
    with open(json_file_5, 'w') as file:
        json.dump(dimensions, file, indent=4)
        print('dimensions saved')


def find_correspondent_nodes(NodeLookUpTable, data_vec, offset):
    correspondent_nodes = []

    for i in range(len(data_vec)):
        master = NodeLookUpTable[data_vec[i]
                                == NodeLookUpTable[:, 0], 1:4]
        nodeA = data_vec[i]
        slave = master[0] + offset
        nodeB = NodeLookUpTable[np.all(np.round(
            NodeLookUpTable[:, 1:4], 3) == np.round(slave, 3), axis=1), 0]
        # if len(nodeB) != 1:
        print(nodeA, nodeB, slave, master[0])
        correspondent_nodes.append([nodeA, nodeB[-1]])
    return correspondent_nodes



if __name__ == "__main__":
    pass
