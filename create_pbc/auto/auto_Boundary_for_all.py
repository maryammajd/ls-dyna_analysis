import json
import os

def MT_NF_const(file):
    file.write('*BOUNDARY_SPC_SET_ID\n         0MTs constarint\n')
    file.write('        10         0         0         0         0         0         0         0\n')
    file.write('*BOUNDARY_SPC_SET_ID\n         0NFs constarint\n')
    file.write('        11         0         0         0         0         1         1         1\n')
    
def compressionD1(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_compD1.k')


    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        xdir = globals()['dimensions']['xdir']
        file.write(f'         1         0       1.0     {xdir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')
        center_front = globals()[
            'centers']['front']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1compressionD1\n')
        file.write(f'{center_front:10.0f}')
        file.write(
            '         1         2         1      -1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerFront_node fix\n')
        file.write(f'{center_front:10.0f}')
        file.write(
            '         0         0         1         1         0         0         0\n')
        FT_node = globals()[
            'centers']['FT']
        file.write('          1FT fix\n')
        file.write(f'{FT_node:10.0f}')
        file.write(
            '         0         0         1         0         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
    # =============================================================================
    #             file.write('*BOUNDARY_SPC_NODE_ID\n')
    # =============================================================================
        file.write('          2midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for compD1 saved')

def compressionD2(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_compD2.k')


    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        # print('adding load curve')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        ydir = globals()['dimensions']['ydir']
        file.write(f'         1         0       1.0     {ydir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')

        center_right = globals()[
            'centers']['right']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1compressionD2\n')
        file.write(f'{center_right:10.0f}')
        file.write(
            '         2         2         1      -1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerRight_node fix\n')
        file.write(f'{center_right:10.0f}')
        file.write(
            '         0         1         0         1         0         0         0\n')
        FT_node = globals()[
            'centers']['FT']
        file.write('          1FT fix\n')
        file.write(f'{FT_node:10.0f}')
        file.write(
            '         0         0         1         0         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
# =============================================================================
#             file.write('*BOUNDARY_SPC_NODE_ID\n')
# =============================================================================
        file.write('          2midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
                '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for compD2 saved')

def tensionD1(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_tenD1.k')

    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        # print('adding load curve')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        xdir = globals()['dimensions']['xdir']
        file.write(f'         1         0       1.0     {xdir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')

        center_front = globals()[
                'centers']['front']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1tensionD1\n')
        file.write(f'{center_front:10.0f}')
        file.write(
            '         1         2         1       1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerFront_node fix\n')
        file.write(f'{center_front:10.0f}')
        file.write(
            '         0         0         1         1         0         0         0\n')
        FT_node = globals()[
            'centers']['FT']
        file.write('          1FT fix\n')
        file.write(f'{FT_node:10.0f}')
        file.write(
            '         0         0         1         0         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
# =============================================================================
#             file.write('*BOUNDARY_SPC_NODE_ID\n')
# =============================================================================
        file.write('          2midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for tenD1 saved')

def tensionD2(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_tenD2.k')

    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        # print('adding load curve')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        ydir = globals()['dimensions']['ydir']
        file.write(f'         1         0       1.0     {ydir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')

        center_right = globals()[
            'centers']['right']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1tensionD2\n')
        file.write(f'{center_right:10.0f}')
        file.write(
            '         2         2         1       1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerRight_node fix\n')
        file.write(f'{center_right:10.0f}')
        file.write(
            '         0         1         0         1         0         0         0\n')
        FT_node = globals()[
            'centers']['FT']
        file.write('          1FT fix\n')
        file.write(f'{FT_node:10.0f}')
        file.write(
            '         0         0         1         0         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
# =============================================================================
#             file.write('*BOUNDARY_SPC_NODE_ID\n')
# =============================================================================
        file.write('          2midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
                '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for tenD2 saved')


def shearD1(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_shearD1.k')

    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        # print('adding load curve')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        zdir = globals()['dimensions']['zdir']
        file.write(f'         1         0       1.0     {zdir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')

        center_top = globals()[
            'centers']['top']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1shearD1\n')
        file.write(f'{center_top:10.0f}')
        file.write(
            '         2         2         1       1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerTop_node fix\n')
        file.write(f'{center_top:10.0f}')
        file.write(
            '         0         1         0         0         0         0         0\n')
        right_node = globals()[
            'centers']['right']
        file.write('          3right fix\n')
        file.write(f'{right_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
# =============================================================================
#             file.write('*BOUNDARY_SPC_NODE_ID\n')
# =============================================================================
        file.write('          2midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
                '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for shearD1 saved')


def shearD2(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_shearD2.k')

    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        # print('adding load curve')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        zdir = globals()['dimensions']['zdir']
        file.write(f'         1         0       1.0     {zdir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')

        center_top = globals()[
            'centers']['top']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1shearD2\n')
        file.write(
            f'{center_top:10.0f}         1         2         1       1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerTop_node fix\n')
        file.write(f'{center_top:10.0f}')
        file.write(
            '         0         0         1         0         0         0         0\n')
        front_node = globals()[
            'centers']['front']
        file.write('          2front fix\n')
        file.write(f'{front_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
# =============================================================================
#             file.write('*BOUNDARY_SPC_NODE_ID\n')
# =============================================================================
        file.write('          3midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for shearD2 saved')


def shearD3(dir, maxstrain, folder_to_save):
    files = ['centers', 'dimensions']
    for jsons in files:
        json_file = dir + '/' + jsons + '.json'
        with open(json_file, 'r') as file:
            globals()[jsons] = json.load(file)
    cmg_id = 0

    file_path = os.path.join(dir, f'{folder_to_save}/BC_shearD3.k')

    with open(file_path, 'w') as file:
        file.write('*TITLE\nLS-DYNA keyword for boundary conditions\n')
        # print('adding load curve')
        file.write('*DEFINE_CURVE_TITLE\n')
        file.write('DisplR(t)\n')
        xdir = globals()['dimensions']['xdir']
        file.write(f'         1         0       1.0     {xdir/2*maxstrain:5.3f}       0.0       0.0         0         0\n')
        file.write('$                  X                   Y\n')
        file.write('                 0.0                 0.0\n')
        file.write('              &TERMT                 1.0\n')
        file.write('                   5                 1.0\n')

        center_front = globals()[
            'centers']['front']
        file.write('*BOUNDARY_PRESCRIBED_MOTION_NODE_ID\n')
        file.write('         1shearD3\n')
        file.write(f'{center_front:10.0f}')
        file.write(
            '         3         2         1       1.0         01.00000E28       0.0\n')
        file.write('*BOUNDARY_SPC_NODE_ID\n')
        file.write('          1centerFront_node fix\n')
        file.write(f'{center_front:10.0f}')
        file.write(
            '         0         0         1         0         0         0         0\n')
        top_node = globals()[
            'centers']['top']
        file.write('          1top fix\n')
        file.write(f'{top_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        midpoint_node = globals()[
            'centers']['midpoint']
# =============================================================================
#             file.write('*BOUNDARY_SPC_NODE_ID\n')
# =============================================================================
        file.write('          2midpoint fix\n')
        file.write(f'{midpoint_node:10.0f}')
        file.write(
            '         0         1         1         1         0         0         0\n')
        MT_NF_const(file)
        file.write('*END\n')
    print(f'Boundary card for shearD3 saved')


if __name__ == "__main__":
    pass
