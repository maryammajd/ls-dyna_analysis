import pdb; pdb.set_trace()


def order_group(group, r_inner_values=(0.0062,0.0077), r_outer=0.0125, thresholds=(30,22.5), x_var=0.0299, tol=1e-3):
    """
    group: list of dicts like [{nid: (r,theta,x)}, ...]
    returns: dict {n1: nid, ..., n8: nid}
    """
    # flatten group into {nid: (r,theta,x)}
    coords = {}
    for entry in group:
        for nid, vals in entry.items():
            coords[int(nid)] = tuple(vals)

    # find base theta (a) and base x (b) from one inner node
    base_theta, base_x = None, None
    for r,theta,x in coords.values():
        if any(abs(r-ri)<tol for ri in r_inner_values):
            base_theta, base_x = theta, x
            break
    if base_theta is None:
        raise ValueError("No inner node found in group")

    ordered = {}

    def find_node(r_target, theta_target, x_target):
        for nid,(r,theta,x) in coords.items():
            if abs(r-r_target)<tol and abs(theta-theta_target)<tol and abs(x-x_target)<tol:
                return nid
        return None

    # try each threshold value
    for threshold in thresholds:
        tehta_added = (base_theta+threshold)%360
        print(tehta_added, base_theta, threshold)
        # nodes at x=b+Δ (shifted origin)
        ordered["n1"] = (find_node(r_inner_values[0], base_theta, base_x+x_var) or
                         find_node(r_inner_values[1], base_theta, base_x+x_var))
        ordered["n2"] = (find_node(r_inner_values[0], tehta_added, base_x+x_var) or
                         find_node(r_inner_values[1], tehta_added, base_x+x_var))
        ordered["n3"] = find_node(r_outer, tehta_added, base_x+x_var)
        ordered["n4"] = find_node(r_outer, base_theta, base_x+x_var)

        # nodes at x=b (base origin)
        ordered["n5"] = (find_node(r_inner_values[0], base_theta, base_x) or
                         find_node(r_inner_values[1], base_theta, base_x))
        ordered["n6"] = (find_node(r_inner_values[0], tehta_added, base_x) or
                         find_node(r_inner_values[1], tehta_added, base_x))
        ordered["n7"] = find_node(r_outer, tehta_added, base_x)
        ordered["n8"] = find_node(r_outer, base_theta, base_x)

        # if all slots filled, stop
        if all(ordered.values()):
            break

    return ordered


# Example usage
import json
with open("groups.json") as f:
    groups = json.load(f)

ordered_groups = [order_group(group) for group in groups]

def write_element_solid_file(elements, eid=0, pid=101010, filename="element_holetomt.k"):
    with open(filename, "w") as f:
        f.write("*ELEMENT_SOLID\n")
        for element in elements:
            eid += 1
            nids = [element.get(k) for k in ["n1","n2","n3","n4","n5","n6","n7","n8"]]
            if None in nids:
                print(f"Skipping element {eid}, missing nodes: {nids}")
                continue
            f.write(f"{eid:8.0f} {pid:7.0f} "
                    f"{nids[0]:7d} {nids[1]:7d} {nids[2]:7d} {nids[3]:7d} "
                    f"{nids[4]:7d} {nids[5]:7d} {nids[6]:7d} {nids[7]:7d}\n")


write_element_solid_file(ordered_groups, 317083, 1234)
