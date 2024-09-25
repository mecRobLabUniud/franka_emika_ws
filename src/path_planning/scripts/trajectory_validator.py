#!/usr/bin/env python3
# coding=utf-8

import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import DHRobot, RevoluteMDH
from math import pi
from copy import deepcopy



q_min_lim = np.array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])   # rad
q_max_lim = np.array([2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973])         # rad
q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])            # rad/s
q_pp_lim = np.array([15, 7.5, 10, 12.5, 15, 20, 20])                                    # rad/s^2
q_ppp_lim = np.array([7500, 3750, 5000, 6250, 7500, 10000, 10000])                      # rad/s^3
tau_lim = np.array([87, 87, 87, 87, 12, 12, 12])                                        # Nm
tau_p_lim = np.array([1000, 1000, 1000, 1000, 1000, 1000, 1000])                        # Nm/s
toll = 0.9


class Panda(DHRobot):

    def __init__(self):

        L = [
            # Link 1
            RevoluteMDH(
                a = 0.0,
                d = 0.333,
                alpha = 0.0,
                I = [0.7034, 0.7066, 0.0091, -1.3900e-4, 0.0192, 0.0068],
                # Inertia tensor of link with rispect to center of mass
                # I = [L_xx, L_yy, L_zz, L_xy, L_yz, L_xz]
                r = [0.0039, 0.0021, -0.1750],
                # Center of mass [x,y,z]
                m = 4.9707,
                # Mass of link
                qlim = np.array([-2.8973, 2.8973])
            ),

            # Link 2
            RevoluteMDH(
                a = 0.0,
                d = 0.0,
                alpha = -np.pi/2,
                I =[0.0080, 0.0281, 0.0260, -0.0039, 7.0400e-4, 0.0103],
                r = [-0.0031, -0.0287, 0.0035],
                m = 0.6469,
                qlim = np.array([-1.7628, 1.7628])
            ),

            # Link 3
            RevoluteMDH(
                a = 0.0,
                d = 0.316,
                alpha = np.pi/2,
                I = [0.0372, 0.0362, 0.0108, -0.0048, -0.0128, -0.0114],
                r = [0.0275, 0.0393, -0.0665],
                m = 3.2286,
                qlim = np.array([-2.8973, 2.8973])
            ),

            # Link 4
            RevoluteMDH(
                a = 0.0825,
                d = 0.0,
                alpha = np.pi/2,
                I = [0.0259, 0.0196, 0.0283, 0.0078, 0.0086, -0.0013],
                r = [-0.0532, 0.1044, 0.0275],
                m = 3.5879,
                qlim = np.array([-3.0718, -0.0698])
            ),

            # Link 5
            RevoluteMDH(
                a = -0.0825,
                d = 0.384,
                alpha = -np.pi/2,
                I = [0.0355, 0.0295, 0.0086, -0.0021, 2.2900e-4, -0.0040],
                r = [-0.0120, 0.0411, -0.0384],
                m = 1.2259,
                qlim = np.array([-2.8973, 2.8973])
            ),

            # Link 6
            RevoluteMDH(
                a = 0.0,
                d = 0.0,
                alpha = np.pi/2,
                I = [0.0020, 0.0044, 0.0054, 1.0900e-4, 3.4100e-4, -0.0012],
                r = [0.0601, -0.0141, -0.0105],
                m = 1.6666,
                qlim = np.array([-0.0175, 3.7525])
            ),

            # Link 7
            RevoluteMDH(
                a = 0.088,
                d = 0.0,
                alpha = np.pi/2,
                I = [0.0125, 0.0100, 0.0048, -4.2800e-4, -7.4100e-4, -0.0012],
                r = [0.0105, -0.0043, 0.0616],
                m = 0.0,
                qlim = np.array([-2.8973, 2.8973])
            )
        ]

        super().__init__(
            L,
            name = 'Panda',
            manufacturer = 'Franka Emika',
            meshdir = 'meshes/FRANKA-EMIKA/Panda'
            )


def file_reader():
    t = []
    q = []
    q_p = []
    q_pp = []
    q_ppp = []
    
    # Read q matrix -------------------------------
    fl_t = open(path_name + '/t.txt','r')
    fl_q = open(path_name + '/q.txt','r')
    fl_q_p = open(path_name + '/q_p.txt','r')
    fl_q_pp = open(path_name + '/q_pp.txt','r')
    fl_q_ppp = open(path_name + '/q_ppp.txt','r')

    for line in fl_t:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        t.append(data)

    for line in fl_q:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        q.append(data)

    for line in fl_q_p:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        q_p.append(data)

    for line in fl_q_pp:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        q_pp.append(data)

    for line in fl_q_ppp:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        q_ppp.append(data)

    fl_t.close()
    fl_q.close()
    fl_q_p.close()
    fl_q_pp.close() 
    fl_q_ppp.close()

    return t, q, q_p, q_pp, q_ppp


def validator(t, q, q_p, q_pp, q_ppp):
    panda = Panda()
    
    y = 0

    traj_valid = True
    t_prev = 0.000001
    tau_prev = panda.rne(q[0], q_p[0], q_pp[0])
    
   
    while(traj_valid and y < len(q)):
        # Calculate torques of all joints
        tau = panda.rne(q[y], q_p[y], q_pp[y])
        
        # Calculate torques derivatives of all joints
        tau_p = (tau-tau_prev) / (t[y][0]-t_prev)
        
        # Verify limits
        q_lim_valid = not(np.any(q[y] < toll * q_min_lim)) and not(np.any(q[y] > toll * q_max_lim))
        q_p_lim_valid = not(np.any(abs(q_p[y]) > toll * q_p_lim))
        q_pp_lim_valid = not(np.any(abs(q_pp[y]) > toll * q_pp_lim))
        q_ppp_lim_valid = not(np.any(abs(q_ppp) > toll * q_ppp_lim))
        tau_lim_valid = not(np.any(abs(tau) > toll * tau_lim))
        tau_p_lim_valid = not(np.any(abs(tau_p) > toll * tau_p_lim))

        if(not(q_lim_valid) or not(q_p_lim_valid) or not(q_pp_lim_valid) or not(q_ppp_lim_valid) or not(tau_lim_valid) or not(tau_p_lim_valid)):
            traj_valid = False

            if(not(q_lim_valid)):
                print('\nLimiti di posizione non rispettati')
            if(not(q_p_lim_valid)):
                print('\nLimiti di velocità superati')
            if(not(q_pp_lim_valid)):
                print('\nLimiti di accelerazione superati')
            if(not(q_ppp_lim_valid)):
                print('\nLimiti di jerk superati')
            if(not(tau_lim_valid)):
                print('\nLimiti di coppia superati')
            if(not(tau_p_lim_valid)):
                print('\nLimiti della derivata della coppia superati')

        tau_prev = deepcopy(tau)
        t_prev = deepcopy(t[y])
        y += 1

    return traj_valid


if __name__ == "__main__":

    path_name = '/home/panda/Desktop/DATA'

    t, q, q_p, q_pp, q_ppp = file_reader()
 
    t = np.array(t)  
    q = np.array(q)
    q_p = np.array(q_p)
    q_pp = np.array(q_pp)
    q_ppp = np.array(q_ppp)
    
    print(validator(t, q, q_p, q_pp, q_ppp))