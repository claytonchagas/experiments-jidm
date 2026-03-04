import sys
import math
import numpy as np
import os

from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

RAD = math.pi / 180
FILENAME_R = "R.dat"
FILENAME_E0 = "E0.dat"
FILENAME_PLOT = "plot.png"

def initialize_environment(argv):
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    program_name = argv[0]
    input_data_file = argv[2]
    input_model = argv[1]
    if len(argv) < 4:
        output_dir = os.path.join("output", "modular", str(time))
    else:
        output_dir = argv[3]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return time, program_name, input_data_file, input_model, output_dir

def load_parameters(input_data_file):
    params = open(input_data_file, 'r')
    param_list = []
    for line in params:
        if not line.startswith("#"):
            param_list.append(int(line))
    freq, corr, delstd, ipol, pstart, pstop, delp, tstart, tstop, delt = param_list
    params.close()
    return freq, corr, delstd, ipol, pstart, pstop, delp, tstart, tstop, delt

def calculate_constants(freq, ipol):
    c = 3e8
    waveL = c / freq
    if ipol == 0:
        et = 1 + 0j
        ep = 0 + 0j
    elif ipol == 1:
        et = 0 + 0j
        ep = 1 + 0j
    return waveL, et, ep

def load_geometry(input_model):
    fname = input_model + "/coordinates.m"
    coordinates = np.loadtxt(fname)
    xpts = coordinates[:, 0]
    ypts = coordinates[:, 1]
    zpts = coordinates[:, 2]
    nverts = len(xpts)

    fname2 = input_model + "/facets.m"
    facets = np.loadtxt(fname2)

    node1 = facets[:, 1]
    node2 = facets[:, 2]
    node3 = facets[:, 3]

    x = xpts
    y = ypts
    z = zpts
    r = [[x[i], y[i], z[i]]
         for i in range(nverts)]

    ntria = len(node3)
    vind = [[node1[i], node2[i], node3[i]]
            for i in range(ntria)]
    return r, vind, ntria

def plot_model(r, vind, ntria, input_model, output_dir):
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    fig1 = plt.figure()
    ax = Axes3D(fig1)
    for i in range(ntria):
        Xa = [int(r[int(vind[i][0])-1][0]), int(r[int(vind[i][1])-1][0]), int(r[int(vind[i][2])-1][0]), int(r[int(vind[i][0])-1][0])]
        Ya = [int(r[int(vind[i][0])-1][1]), int(r[int(vind[i][1])-1][1]), int(r[int(vind[i][2])-1][1]), int(r[int(vind[i][0])-1][1])]
        Za = [int(r[int(vind[i][0])-1][2]), int(r[int(vind[i][1])-1][2]), int(r[int(vind[i][2])-1][2]), int(r[int(vind[i][0])-1][2])]
        ax.plot3D(Xa, Ya, Za)
        ax.set_xlabel("X Axis")
    ax.set_title("3D Model: " + input_model)
    plt.savefig(os.path.join(output_dir, FILENAME_PLOT))
    plt.close()
    return now

def calculate_grid(pstart, pstop, delp, tstart, tstop, delt):
    if delp == 0:
        delp = 1
    if pstart == pstop:
        phr0 = pstart*RAD

    if delt == 0:
        delt = 1
    if tstart == tstop:
        thr0 = tstart*RAD

    it = math.floor((tstop-tstart)/delt)+1
    ip = math.floor((pstop-pstart)/delp)+1
    return delp, delt, it, ip

def execute_simulation(output_dir, r_data, ip, it, pstart, delp, tstart, delt, et, ep):
    header = '\n'.join(map(str, r_data)) + '\n'
    fileR = open(os.path.join(output_dir, FILENAME_R), 'w')
    fileE0 = open(os.path.join(output_dir, FILENAME_E0), 'w')

    fileR.write(header)
    fileE0.write(header)

    phi = []
    theta = []
    R = []
    e0 = []
    for i1 in range(0, int(ip)):
        for i2 in range(0, int(it)):
            phi.append(pstart + i1 * delp)
            phr = phi[i2] * RAD
            theta.append(tstart + i2 * delt)
            thr = theta[i2] * RAD
            st = math.sin(thr)
            ct = math.cos(thr)
            cp = math.cos(phr)
            sp = math.sin(phr)
            D0 = [st*cp, st*sp, ct]
            E = [ct*cp, ct*sp, -st, sp, cp]
            u, v, w = D0
            fileR.write(str(i2))
            fileR.write(" ")
            fileR.write(str([u, v, w]))
            fileR.write("\n")
            uu, vv, ww, sp, cp = E
            fileE0.write(str(i2))
            fileE0.write(" ")
            fileE0.write(str([(uu * et - sp * ep), (vv * et + cp * ep), (ww * et)]))
            fileE0.write("\n")
    fileR.close()
    fileE0.close()

if __name__ == "__main__":
    time, program_name, input_data_file, input_model, output_dir = initialize_environment(sys.argv)
    
    freq, corr, delstd, ipol, pstart, pstop, delp, tstart, tstop, delt = load_parameters(input_data_file)
    
    waveL, et, ep = calculate_constants(freq, ipol)
    
    r, vind, ntria = load_geometry(input_model)
    
    now = plot_model(r, vind, ntria, input_model, output_dir)
    
    delp, delt, it, ip = calculate_grid(pstart, pstop, delp, tstart, tstop, delt)
    
    r_data = [
        now, program_name, input_data_file, input_model,
        freq, corr, delstd, ipol, pstart, pstop,
        delp, tstart, tstop, delt
    ]
    
    execute_simulation(output_dir, r_data, ip, it, pstart, delp, tstart, delt, et, ep)