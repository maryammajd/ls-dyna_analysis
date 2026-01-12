
import math, json
import numpy as np

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


nodes = parse_nodes("source/tenD1/node.k")

with open("stars_near_gaps.json") as f:
    stars_near_gaps = json.load(f)

def find_nodes_polar(target_nodes, nodes,
                           r_targets=[0.0062, 0.0077, 0.0125], tol=0.001, angle_step=30):
    """
    target_nodes: list of node IDs to use as centers
    nodes: dict {nid: (x, y, z)}
    r_targets: list of radii to check
    tol: tolerance for matching coordinates
    angle_step: step size in degrees for theta bins
    """
    results = {}

    for tid in target_nodes:
        results[tid] ={}
        # print(results)
        if tid not in nodes:
            print(tid)
            continue
        x0, y0, z0 = nodes[tid]
        if abs(y0 + 1.375) <= tol and abs(z0 - 1.231) <= tol:
            # print(tid, x0, y0, z0)
            angle_step = 22.5
        else:
            angle_step = 30
        for r_target in r_targets:
            for theta_bin in np.arange(-0, 370, angle_step):
                # Desired coordinate in yz-plane
                y_desired = y0 + r_target * math.cos(math.radians(theta_bin))
                z_desired = z0 + r_target * math.sin(math.radians(theta_bin))

                # Look for a node at (x0, y_desired, z_desired)
                for nid, (x, y, z) in nodes.items():
                    if (abs(x - x0) <= tol and abs(y - y_desired) <= tol and abs(z - z_desired) <= tol):
                        if theta_bin == 360: 
                            theta_bin =0
                        # print('found the node', tid, nid, 'r:', r_target, "theta:", theta_bin)
                        results[tid][nid] = {
                            "coord": [float(x), float(y), float(z)],  # list, not tuple
                            "r_target": float(r_target),
                            "theta_bin": float(theta_bin)
                        }
    return results



target_nodes = sorted(stars_near_gaps)

matches = find_nodes_polar(target_nodes, nodes)

save_json(matches, "matches.json")