import numpy as np
import pdb; pdb.set_trace()
import json



class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, cls=NumpyEncoder)


def parse_nodes(file_path):
    nodes = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("*NODE") or line.startswith("$") or line.startswith("*"):
                continue
            parts = line.strip().split()
            if len(parts) >= 4:
                nid = int(parts[0])
                x, y, z = map(float, parts[1:4])
                nodes[nid] = (x, y, z)
    return nodes

def map_node_to_parts(file_path):
    node_parts = {}
    current_type = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("*ELEMENT"):
                current_type = line.upper()
                continue
            if line.startswith("*") or line.startswith("$") or not line:
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            pid = int(parts[1])

            # Determine how many nodes to extract based on element type
            if "*ELEMENT_BEAM" in current_type:
                # Beam: eid pid n1 n2 n3 rt1 rr1 rt2 rr2 local → nodes = parts[2:5]
                nids = list(map(int, parts[2:5]))
            else:
                # Generic: assume all after pid are node IDs
                nids = []
                for val in parts[2:]:
                    try:
                        nids.append(int(val))
                    except ValueError:
                        break  # stop at first non-integer (e.g., material or flags)

            for nid in nids:
                if nid not in node_parts:
                    node_parts[nid] = set()
                node_parts[nid].add(pid)

    return node_parts

def find_nodes_used_in_part(node_parts, target_part=10):
    return {nid for nid, parts in node_parts.items() if target_part in parts}

def find_nodes_used_only_in_part(node_parts, target_part=9):
    return {nid for nid, parts in node_parts.items() if parts == {target_part}}

def filter_nodes_at_x_zero(nodes, node_ids, x_coord_value):
    return {nid: coord for nid, coord in nodes.items() if nid in node_ids and np.round(coord[0], 3) == np.round(x_coord_value, 3)}

import csv

clusters = {}

with open("clusters.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cluster_id = int(row["Cluster"])
        node_id = int(row["Node ID"])
        x = float(row["X"])
        y = float(row["Y"])
        z = float(row["Z"])
        
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append((node_id, (x, y, z)))


nodes = parse_nodes("source/tenD1/node.k")
part_nodes = map_node_to_parts("source/element.k")
part_10 = find_nodes_used_in_part(part_nodes, target_part=10)
shared_node_coords = {nid: nodes[nid] for nid in part_10 if nid in nodes}

def write_element_solid_file(elements, filename="solid_elements.k"):
    with open(filename, "w") as f:
        f.write("*ELEMENT_SOLID\n")
        for e in elements:
            eid, pid, n1, n2, n3, n4, n5, n6, n7, n8 = e
            f.write(f"{eid} {pid} {n1} {n2} {n3} {n4} {n5} {n6} {n7} {n8}\n")




exclusive_stars = find_nodes_used_only_in_part(part_nodes, target_part=9)
star_mid_coord = filter_nodes_at_x_zero(nodes, exclusive_stars, 0.0)

save_json(star_mid_coord, "star_mid_coord.json")
print("all mid-stars are saved in star_mid_coord.json")
