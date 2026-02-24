#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on some date on 2024

This code takes the directory and name of the keyfile you want to extract the nodes for and saves all 
the data about nodes including their coordinates in Nodes.k file :)

@author: maryamma
"""


import os
import numpy as np
import sys

def extract_nparray_data(file_path, start_marker, end_marker, save_to_file=None):
    data = []
    inside_array = False

    with open(file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                inside_array = True
                continue
            elif end_marker in line.lower():
                if inside_array:
                    inside_array = False
            elif inside_array and not any(c.isalpha() for c in line):
                values = line.split()  # Split by spaces
                # Convert and add to the data list
                data.extend(map(float, values))

    data_array = np.array(data)

    # Save the data to a text file if a save_to_file path is provided
    if save_to_file:
        with open(save_to_file, 'w') as save_file:
            for item in data_array:
                save_file.write(f'{item}\n')

    return data_array


def extract_array_data(file_path, start_marker, end_marker, save_to_file=None):
    data = []
    inside_array = False

    with open(file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                inside_array = True
                if save_to_file:
                    data.append(line)  # Save the start_marker line
                continue
            elif end_marker in line:
                if inside_array:
                    inside_array = False
                    if save_to_file:
                        data.append(line)  # Save the end_marker line
                    break

            if inside_array:
                data.append(line)  # Save the lines inside the array

    # Save the data to a text file if a save_to_file path is provided
    if save_to_file:
        with open(save_to_file, 'w') as save_file:
            for line in data:
                save_file.write(line)

    return data


def node_extract(directori, keyfile):
    print('allstep1')
    file_path = os.path.join(str(directori), str(keyfile))
    end_array_marker = "*"
    start_array_marker = '*NODE'

    # Extract the data and save it to a text file
    save_file_path = str(directori) + "/Nodes.k"
    node = extract_array_data(file_path, start_array_marker,
                            end_array_marker, save_to_file=save_file_path)
    return node


if __name__ == "__main__":
    pass