#!/usr/bin/env python3
# coding=utf-8

import rospy
from def_proj.srv import CalcValidTraj, CalcValidTrajResponse
import numpy as np
from roboticstoolbox import DHRobot, RevoluteMDH
from math import pi
from copy import deepcopy

"""
Validatore traiettoria con TrajPoly5 e tutti i vincoli
"""

# Settings
q_min_lim = np.array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])   # rad
q_max_lim = np.array([2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973])         # rad
q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])            # rad/s
q_pp_lim = np.array([15, 7.5, 10, 12.5, 15, 20, 20])                                    # rad/s^2
q_ppp_lim = np.array([7500, 3750, 5000, 6250, 7500, 10000, 10000])                      # rad/s^3
tau_lim = np.array([87, 87, 87, 87, 12, 12, 12])                                        # Nm
tau_p_lim = np.array([1000, 1000, 1000, 1000, 1000, 1000, 1000])                        # Nm/s
toll = 0.9

class Panda(DHRobot):

    """
    A class representing the Panda robot arm.

    ``Panda()`` is a class which models a Franka-Emika Panda robot and
    describes its kinematic and dynamics characteristics using modified DH
    conventions.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.DH.Panda()
        >>> print(robot)

    .. note::
        - SI units of metres are used.
        - The model includes a tool offset.

    :references:
        - https://frankaemika.github.io/docs/control_parameters.html
        - articolo ???


    .. codeauthor:: Samuel Drew
    .. codeauthor:: Peter Corke
    """

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

def TrajPoly5(qi, qi_p, qi_pp, qf, qf_p, qf_pp, traj_duration, time_step):

    coeff = np.zeros(6)

    coeff[0] = qi
    coeff[1] = qi_p
    coeff[2] = qi_pp / 2

    known_terms = np.array([qf - qi - qi_p * traj_duration - 0.5 * qi_pp * traj_duration**2, qf_p - qi_p - qi_pp * traj_duration, qf_pp - qi_pp])

    # Vandermonde matrix
    V = np.array([[traj_duration**3, traj_duration**4, traj_duration**5], [3 * traj_duration**2, 4 * traj_duration**3, 5 * traj_duration**4], [6 * traj_duration, 12 * traj_duration**2, 20 * traj_duration**3]])

    coeff_1 = np.linalg.solve(V, known_terms)

    coeff[3] = coeff_1[0]
    coeff[4] = coeff_1[1]
    coeff[5] = coeff_1[2]
    
    t = np.linspace(0, traj_duration, int(traj_duration / time_step + 1))

    # Position profile
    q = coeff[0] + coeff[1] * t + coeff[2] * t**2 + coeff[3] * t**3 + coeff[4] * t**4 + coeff[5] * t**5

    # Velocity profile
    q_p = coeff[1] + 2 * coeff[2] * t + 3 * coeff[3] * t**2 + 4 * coeff[4] * t**3 + 5 * coeff[5] * t**4

    # Acceleration profile
    q_pp = 2 * coeff[2] + 6 * coeff[3] * t + 12 * coeff[4] * t**2 + 20 * coeff[5] * t**3

    traj = np.vstack((q, q_p, q_pp))
    
    return traj

def CalcValidTrajServer(q_start, q_end, traj_duration, traj_step):

    panda = Panda()

    # Initialization q, q_p and q_pp
    num_points = int(traj_duration / traj_step) + 1

    q = np.zeros((num_points, 7))
    q_p = np.zeros((num_points, 7))
    q_pp = np.zeros((num_points, 7))
    q_ppp = np.zeros((num_points, 7))

    # Calculate complete trajectory
    for joint_num in range(7):

        traj = TrajPoly5(q_start[joint_num], 0, 0, q_end[joint_num], 0, 0, traj_duration, traj_step)
        
        q[:, joint_num] = deepcopy(np.transpose(traj[0, :]))
        q_p[:, joint_num] = deepcopy(np.transpose(traj[1, :]))
        q_pp[:, joint_num] = deepcopy(np.transpose(traj[2, :]))

    # Usefull variables
    y = 0

    traj_valid = 1

    q_pp_prec = np.zeros(7)
    tau_prec = panda.rne(q_start, q_p[0], q_pp[0])
   
    while(traj_valid and y < len(q)):

        # Calculate jerks
        q_ppp = (q_pp[y] - q_pp_prec) / traj_step

        # Calculate torques of all joints
        tau = panda.rne(q[y], q_p[y], q_pp[y])

        # Calculate torques derivatives of all joints
        tau_p = (tau - tau_prec) / traj_step

        # Verify limits
        q_lim_valid = not(np.any(q[y] < toll * q_min_lim)) and not(np.any(q[y] > toll * q_max_lim))
        q_p_lim_valid = not(np.any(abs(q_p[y]) > toll * q_p_lim))
        q_pp_lim_valid = not(np.any(abs(q_pp[y]) > toll * q_pp_lim))
        q_ppp_lim_valid = not(np.any(abs(q_ppp) > toll * q_ppp_lim))
        tau_lim_valid = not(np.any(abs(tau) > toll * tau_lim))
        tau_p_lim_valid = not(np.any(abs(tau_p) > toll * tau_p_lim))

        if(not(q_lim_valid) or not(q_p_lim_valid) or not(q_pp_lim_valid) or not(q_ppp_lim_valid) or not(tau_lim_valid) or not(tau_p_lim_valid)):
            traj_valid = 0

            # if(not(q_lim_valid)):
            #     print('\nLimiti di posizione non rispettati')
            # if(not(q_p_lim_valid)):
            #     print('\nLimiti di velocità superati')
            # if(not(q_pp_lim_valid)):
            #     print('\nLimiti di accelerazione superati')
            # if(not(q_ppp_lim_valid)):
            #     print('\nLimiti di jerk superati')
            # if(not(tau_lim_valid)):
            #     print('\nLimiti di coppia superati')
            # if(not(tau_p_lim_valid)):
            #     print('\nLimiti della derivata della coppia superati')

        q_pp_prec = deepcopy(q_pp[y])
        tau_prec = deepcopy(tau)
        y += 1

    return(traj_valid)

def HandleValidTraj(req):

    flag_valid = CalcValidTrajServer(np.array(req.q_s), np.array(req.q_e), req.traj_duration, req.traj_step)

    return CalcValidTrajResponse(flag_valid)

def CalcValidTrajServer1():

    rospy.init_node('calc_valid_traj_server')
    s = rospy.Service('calc_valid_traj', CalcValidTraj, HandleValidTraj)
    print("Ready.")
    rospy.spin()

if __name__ == "__main__":

    CalcValidTrajServer1()