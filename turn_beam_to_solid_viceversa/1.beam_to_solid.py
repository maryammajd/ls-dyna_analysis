import math, json
import numpy as np
import pdb; pdb.set_trace()

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


nodes = parse_nodes("source/tenD1/node.k")
part_nodes = map_node_to_parts("source/element.k")
# for nid, (x, y, z) in sorted(star_mid_coord.items()):
#     print(f"Node {nid}: 0, {y}, {z}")

with open("star_mid_coord.json") as f:
    star_mid_coord = json.load(f)

import math


def find_nodes_by_coord(nodes, target_coord, tol=1e-3):
    """
    nodes: dict {nid: (x, y, z)}
    target_coord: tuple (x, y, z)
    tol: tolerance for floating-point comparison
    """
    matches = []
    tx, ty, tz = target_coord
    for nid, (x, y, z) in nodes.items():
        if abs(x - tx) <= tol and abs(y - ty) <= tol and abs(z - tz) <= tol:
            matches.append(nid)
    return matches


def find_matching_pairs(star_mid_coord, nodes, part_nodes, target_part=10, yz_thresh=0.009):
    star_gap_match_coord = set()  # use a set for uniqueness
    star_gap_match_name = set()
    part10_nodes = {nid for nid, parts in part_nodes.items() if target_part in parts}

    for nid9, (x0, y0, z0) in star_mid_coord.items():
        for nid10 in part10_nodes:
            if nid10 not in nodes:
                continue
            x, y, z = nodes[nid10]

            dist_yz = math.sqrt((y - y0)**2 + (z - z0)**2)
            if dist_yz <= yz_thresh:
                # print(nid9, nid10, dist_yz)
                nid_star = find_nodes_by_coord(nodes, (x, y0, z0))
                star_gap_match_coord.add((nid_star[0], x, y0, z0))  # tuple is hashable
                star_gap_match_name.add((nid_star[0]))  
    return star_gap_match_coord, star_gap_match_name

coord_stars_near_gaps, stars_near_gaps = find_matching_pairs(star_mid_coord, nodes, part_nodes)

save_json(list(stars_near_gaps), "stars_near_gaps.json")
print("stars associated with gaps are saved in stars_near_gaps.json")
# for nid9, x9, y9, z9 in sorted(stars_near_gaps):
#     print(f"Part9 Node {nid9}: ({x9}, {y9}, {z9})")


# Example usage
# target = (5.01, -1.485, 1.231002)
# matched_nodes = find_nodes_by_coord(nodes, target)
# print("Matched node IDs:", matched_nodes)

