import numpy as np
import pdb; pdb.set_trace()
import json

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

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
tol = 0.001
def categorise_nodes(data, r_inner_values, r_outer, threshold, q):
    groups = []
    
    for origin_key, inner_dict in data.items():
        
        ox, oy, oz = nodes[int(origin_key)]
        # print(origin_key, ox, oy, oz )
        # find paired origin2 by offset q in x
        origin2_cart = (ox + q, oy, oz)
        origin2_key = None
        for key, val in nodes.items():
            cx, cy, cz = val
            if (abs(cx - origin2_cart[0]) < tol and
                abs(cy - origin2_cart[1]) < tol and
                abs(cz - origin2_cart[2]) < tol):
                origin2_key = key
                break
        # break if origin2_key not in data
        if not origin2_key or str(origin2_key) not in data.keys():
            print(origin_key)
            continue
        
        
        # print(origin2_key, nodes[origin2_key] )
        def get_node(origin_dict, r_values, theta):
            for nid, info in origin_dict.items():
                pr, pt = info["r_target"], info["theta_bin"]
                if any(abs(pr - r) < 1e-3 for r in r_values) and abs(pt - theta) < 1:
                    return {nid: [pr, pt, info['coord'][0]]}
                else: print(nid, pr, pt)
            return None


        if abs(oy + 1.375) <= tol and abs(oz - 1.231) <= tol:
            threshold = 22.5  # tid removed, angle_step kept if needed
        else:
            threshold = 30
        # build group for each angle a found in origin1
        for nid, info in inner_dict.items():
            a = info["theta_bin"]
            tehta_added = (a + threshold) % 360

            nodes_group = []
            # from origin1
            nodes_group.append(get_node(inner_dict, r_inner_values, a))
            nodes_group.append(get_node(inner_dict, r_inner_values, tehta_added))
            nodes_group.append(get_node(inner_dict, [r_outer], a))
            nodes_group.append(get_node(inner_dict, [r_outer], tehta_added))
            # from origin2
            inner2_dict = data[str(origin2_key)]
            nodes_group.append(get_node(inner2_dict, r_inner_values, a))
            nodes_group.append(get_node(inner2_dict, r_inner_values, tehta_added))
            nodes_group.append(get_node(inner2_dict, [r_outer], a))
            nodes_group.append(get_node(inner2_dict, [r_outer], tehta_added))
            # print(nodes_group)
            if all(nodes_group):
                groups.append(nodes_group)
            # else:
                # print(nodes_group, origin_key, origin2_key)
    
    return groups

# Example usage:
with open("matches.json") as f:
    dict_of_gaps = json.load(f)

groups = categorise_nodes(
    dict_of_gaps,
    r_inner_values=[0.0062, 0.0077],  # now accepts multiple inner radii
    r_outer=0.012,
    threshold=30,
    q=0.0299
)
# print(groups)


save_json(groups, 'groups.json')


