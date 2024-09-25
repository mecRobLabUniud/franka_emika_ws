#!/usr/bin/env python3
# coding=utf-8

from cmath import nan
from collections import namedtuple
import cv2
from time import time, sleep
import math
from math import cos, sin, pi, atan2
import numpy as np
from copy import deepcopy
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import rospy
from def_proj.srv import FlagStop, FlagStopResponse
import roboticstoolbox as rtb
import os
import pyrealsense2 as rs
import PoseModule as pm

"""
Documentazione: 
https://www.analyticsvidhya.com/blog/2021/05/pose-estimation-using-opencv/

Enumerazione giunti:
7 = orecchio sinistro
8 = orecchio destro
11 = spalla sinistra
12 = spalla destra
13 = gomito sinistro
14 = gomito destro
15 = polso sinistro
16 = polso destro
23 = anca sinistra
24 = anca destra
33 = testa (custom)
34 = collo (custom)
35 = centro anche (custom)

Richiede:
- PoseModule.py
"""


panda = rtb.models.DH.Panda()

stamp = 0
record = 1

joints_num = [11, 12, 13, 14, 15, 16, 33, 34, 35]
joints_segm = [[6, 7], [7, 8], [0, 2], [2, 4], [1, 3], [3, 5]]
    


def capsule_calculation(T_stop, q, q_p, q_pp):
    global rv, T_reaction, csi, max_human_speed, max_robot_speed 

    Sh = max_human_speed*(T_reaction + T_stop)

    n_samples = T_stop*1000/ 5 # sample ogni 5 ms
        
    # ricalcolo la traiettoria di stop con n_samples punti:
    num_points = int( T_stop*1000/ n_samples) + 1 

    qi = np.zeros((num_points, 7))
    qi_p = np.zeros((num_points, 7))
    qi_pp = np.zeros((num_points, 7))

    q = np.array([q[0], q[1], q[2], q[3], q[4], q[5], q[6]])
    q_p = np.array([q_p[0], q_p[1], q_p[2], q_p[3], q_p[4], q_p[5], q_p[6]])
    q_pp = np.array([q_pp[0], q_pp[1], q_pp[2], q_pp[3], q_pp[4], q_pp[5], q_pp[6]])

    for k in range(7):
        traj = TrajPoly5(q[k], q_p[k], q_pp[k], q[k], 0, 0, T_stop, n_samples)
       
        qi[:, k] = deepcopy(np.transpose(traj[0, :]))
        qi_p[:, k] = deepcopy(np.transpose(traj[1, :]))
        qi_pp[:, k] = deepcopy(np.transpose(traj[2, :]))
    
    vel_max_1 = []
    vel_max_2 = []
    vel_max_3 = []
    vel_max_4 = []
    
    for m in range(len(qi)):  # per ogni step della traiettoria di stop calcolo la velocita' massima dei punti estremi di ogni capsula
        q_stop = np.matrix([[qi[m, 0], qi[m, 1], qi[m, 2], qi[m, 3], qi[m, 4], qi[m, 5], qi[m, 6]]])

        qp_stop = np.matrix([[qi_p[m, 0], qi_p[m, 1], qi_p[m, 2], qi_p[m, 3], qi_p[m, 4], qi_p[m, 5], qi_p[m, 6]]])

        vel_max = compute_max_vel_capsule(q_stop, qp_stop, rv)
        vel_max_1.append(vel_max[0])
        vel_max_2.append(vel_max[1])
        vel_max_3.append(vel_max[2])
        vel_max_4.append(vel_max[3])
        
        dt_stop = np.linspace(0, T_stop, len(qi))

    Sr_1 = vel_max_1[0]*T_reaction
    Sr_2 = vel_max_2[0]*T_reaction
    Sr_3 = vel_max_3[0]*T_reaction
    Sr_4 = vel_max_4[0]*T_reaction

    # integro sulla traiettoria di stop
    Ss_1 = trapz(dt_stop, vel_max_1)
    Ss_2 = trapz(dt_stop, vel_max_2)
    Ss_3 = trapz(dt_stop, vel_max_3)
    Ss_4 = trapz(dt_stop, vel_max_4)
   
    # calcolo i raggi delle capsule r_sw
    r_sw_1 = rv + Sh + Sr_1 + Ss_1 + csi
    r_sw_2 = rv + Sh + Sr_2 + Ss_2 + csi
    r_sw_3 = rv + Sh + Sr_3 + Ss_3 + csi
    r_sw_4 = rv + Sh + Sr_4 + Ss_4 + csi
    
    r_sw = [r_sw_1, r_sw_2, r_sw_3, r_sw_4]  # raggi delle 4 capsule del robot 
    
    return r_sw



def trapz(dt_stop, vel_max):
    Area = 0

    for i in range(1, len(dt_stop)):
        A = (dt_stop[i]-dt_stop[i-1])*(vel_max[i]+vel_max[i-1])/2
        
        Area = Area + A
        
    return Area



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
    
    t = np.linspace(0, traj_duration, int(traj_duration*1000 / time_step + 1))
    
    # Position profile
    q = coeff[0] + coeff[1] * t + coeff[2] * t**2 + coeff[3] * t**3 + coeff[4] * t**4 + coeff[5] * t**5
    
    # Velocity profile
    q_p = coeff[1] + 2 * coeff[2] * t + 3 * coeff[3] * t**2 + 4 * coeff[4] * t**3 + 5 * coeff[5] * t**4

    # Acceleration profile
    q_pp = 2 * coeff[2] + 6 * coeff[3] * t + 12 * coeff[4] * t**2 + 20 * coeff[5] * t**3

    traj = np.vstack((q, q_p, q_pp))
    
    return traj
    


def compute_max_vel_capsule(q, qp, rv):
    norm = np.linalg.norm

    fk = panda.fkine_all(q).stack()
        
    # 1-0
    A_1 = robot_capsules[0, 0]
    B_1 = np.zeros(3)
        
    #calculate Jacobian for capsule 1-0     
    J = Jacobian(q[0, 0], A_1, fk)
    Jp = J[0:3, :]
    A_1_p = np.dot(Jp, qp[0, 0])
    A_1_p = np.array([A_1_p[0, 0], A_1_p[1, 0], A_1_p[2, 0]])
                   
    Jo = J[3:6, :]
    omega_1 = np.dot(Jo, qp[0, 0])
    omega_1 = np.array([omega_1[0, 0], omega_1[1, 0], omega_1[2, 0]])
    
    A_e1_p = A_1_p + np.cross(omega_1, ((A_1-B_1)/(norm(A_1-B_1))*rv))
    B_e1_p = A_1_p + np.cross(omega_1, ((B_1-A_1)/(norm(B_1-A_1))*(norm(B_1-A_1) + rv)))
    vel_max_1 = max(norm(A_e1_p), norm(B_e1_p))
    
    # 3-2
    A_2 = robot_capsules[1, 0]
    B_2 = robot_capsules[1, 1] 

    #calculate Jacobian for capsule 3-2 
    J = Jacobian(q[0, :3], A_2, fk)
    Jp = J[0:3, :]
    
    A_2_p = np.dot(Jp, qp[0, 0:3].transpose())
    A_2_p = np.array([A_2_p[0, 0], A_2_p[1, 0], A_2_p[2, 0]])
    
    Jo = J[3:6, :]
    omega_2 = np.dot(Jo, qp[0, 0:3].transpose())
    omega_2 = np.array([omega_2[0, 0], omega_2[1, 0], omega_2[2, 0]])
       
    A_e2_p = A_2_p + np.cross(omega_2, ((A_2-B_2)/(norm(A_2-B_2))*rv))
    B_e2_p = A_2_p + np.cross(omega_2, ((B_2-A_2)/(norm(B_2-A_2))*(norm(B_2-A_2) + rv)))
    vel_max_2 = max(norm(A_e2_p), norm(B_e2_p))
        
    # 5-4
    A_3 = robot_capsules[2, 0]
    B_3 = robot_capsules[2, 1]
    
    #calculate Jacobian for capsule 5-4 
    J = Jacobian(q[0, 0:5], A_3, fk)
    Jp = J[0:3, :]
    A_3_p = np.dot(Jp, qp[0, 0:5].transpose())
    A_3_p = np.array([A_3_p[0, 0], A_3_p[1, 0], A_3_p[2, 0]])
    
    Jo = J[3:6, :]
    omega_3 = np.dot(Jo, qp[0, 0:5].transpose())
    omega_3 = np.array([omega_3[0, 0], omega_3[1, 0], omega_3[2, 0]])
    
    A_e3_p = A_3_p + np.cross(omega_3, ((A_3-B_3)/(norm(A_3-B_3))*rv))
    B_e3_p = A_3_p + np.cross(omega_3, ((B_3-A_3)/(norm(B_3-A_3))*(norm(B_3-A_3) + rv)))
    vel_max_3 = max(norm(A_e3_p), norm(B_e3_p))
    
    # 7-6
    A_4 = robot_capsules[3, 0]
    B_4 = robot_capsules[3, 1]

    #calculate Jacobian for capsule 7-6 
    J = Jacobian(q[0, 0:7], A_4, fk)
    Jp = J[0:3, :]
    A_4_p = np.dot(Jp, qp[0, 0:7].transpose())
    A_4_p = np.array([A_4_p[0, 0], A_4_p[1, 0], A_4_p[2, 0]])
    
    Jo = J[3:6, :]
    omega_4 = np.dot(Jo, qp[0, 0:7].transpose())
    omega_4 = np.array([omega_4[0, 0], omega_4[1, 0], omega_4[2, 0]])
    
    A_e4_p = A_4_p + np.cross(omega_4, ((A_4-B_4)/(norm(A_4-B_4))*rv))
    B_e4_p = A_4_p + np.cross(omega_4, ((B_4-A_4)/(norm(B_4-A_4))*(norm(B_4-A_4) + rv)))
    vel_max_4 = max(norm(A_e4_p), norm(B_e4_p))

    vel_max = []
    vel_max.append(vel_max_1)
    vel_max.append(vel_max_2)
    vel_max.append(vel_max_3)
    vel_max.append(vel_max_4)
    
    return vel_max
 


def Jacobian(q, A_k, fk):
    z0 = np.matrix([[0, 0, 1]])
    z0 = z0.transpose()
    
    p0 = np.matrix([[0, 0, 0, 1]])
    
    p0 = p0.transpose()
    
    J = np.zeros((6, q.size))
    
    R_k = np.identity(3)         
    T_k = np.identity(4)

    if q.size == 1:        
        zj = z0.transpose()
        zj = zj[0][0,0:3]
        pj = p0.transpose()
        pj = pj[0][0,0:3]
        p = A_k
        
        J_k = np.cross(zj, p - pj) 
              
        J[0:3, 0] = np.array([J_k[0, 0], J_k[0, 1], J_k[0, 2]])
        J[3:6, 0] = np.array([zj[0, 0], zj[0, 1], zj[0, 2]])

    else:
        zj = z0.transpose()
        zj = zj[0]
        pj = p0[0:3].transpose()
        pj = pj[0]
        p = A_k
        
        J_k = np.cross(zj, p - pj)
        J[0:3, 0] = np.array([J_k[0, 0], J_k[0, 1], J_k[0, 2]])
        J[3:6, 0] = np.array([zj[0, 0], zj[0, 1], zj[0, 2]])
        
        for i in range(len(q) - 1):               
            R = np.array(fk[0:3, 0:3, i])
            
            T = np.array(fk[0:4, 0:4, i])
            
            R_k = deepcopy(np.dot(R_k, R))
            T_k = deepcopy(np.dot(T_k, T)) 
                
            zj = np.dot(R_k, z0) 
            zj = np.array([zj[0, 0], zj[1, 0], zj[2, 0]])
            pj = np.dot(T_k, p0)
            pj = np.array([pj[0, 0], pj[1, 0], pj[2, 0]])
            p = A_k
            
            J_k = np.cross(zj, p - pj)            
            J[0:3, i + 1] = np.array([J_k[0, 0], J_k[0, 1], J_k[0, 2]])
            J[3:6, i + 1] = np.array([zj[0, 0], zj[0, 1], zj[0, 2]])
    
    return J   



def compute_robot_capsules(q):
    fk = panda.fkine_all(q).stack()
                   
    robot_capsules = np.array([[fk[0:3, 3, 1], fk[0:3, 3, 0]],
                               [fk[0:3, 3, 3], fk[0:3, 3, 2]],
                               [fk[0:3, 3, 5], fk[0:3, 3, 4]],
                               [fk[0:3, 3, 7], fk[0:3, 3, 6]]])

    return robot_capsules



def distance_to_skeleton(point_3D, P2, Q2, r_sw_h):

    global joints_segm

    segment = []

    for s in joints_segm:
        if not (point_3D[s[0]] == [-999, -999, -999] or point_3D[s[1]] == [-999, -999, -999]): 
            row1 = point_3D[s[0]]
            row2 = point_3D[s[1]]

            P1 = [row1[0], row1[1], row1[2]]
            Q1 = [row2[0], row2[1], row2[2]]

            P1_o = np.array([[P1[0]],
                            [P1[1]],
                            [P1[2]],
                            [1    ]])

            P1 = np.dot(R_00, P1_o)
            P1 = np.array([P1[0][0], P1[1][0], P1[2][0]])
            
            Q1_o = np.array([[Q1[0]],
                            [Q1[1]],
                            [Q1[2]],
                            [1    ]])

            Q1 = np.dot(R_00, Q1_o)
            Q1 = np.array([Q1[0][0], Q1[1][0], Q1[2][0]])
                                                
            segm = [P1, Q1]  

            segment.append(segm)

        else:

            segment.append([])
    
    # Segment length check   
    norm = np.linalg.norm 

    body_length_values = [0.21, 0.535, 0.355, 0.305, 0.355, 0.305]
    
    if not np.all(segment) == []:
        for j in range(len(segment)):
        
            s = segment[j][1] - segment[j][0]

            if norm(s) > body_length_values[j]:
                
                segment[j] = []  
    
    count = 0

    for b in segment:
        if not b == []:

            count += 1

    if count >= 2:
        min_distance = []

        do_once = 1
    
        for i in range(len(segment)):
            sgmt = segment[i]
                        
            if not sgmt == []:            
                P1 = sgmt[0]
                Q1 = sgmt[1]
  
                dist = distance_to_segment(P1, Q1, P2, Q2)

                distance = dist[0] - r_sw_h[i]
                C_h = dist[1]
                C_r = dist[2]
                    
                if do_once:
                    min_distance.append(deepcopy(distance))
                    min_distance.append(deepcopy(C_h))
                    min_distance.append(deepcopy(C_r))
                
                    do_once = 0

                else:  
                    if not min_distance == []:              
                        if distance < min_distance[0]:
                            min_distance[0] = deepcopy(distance)
                            min_distance[1] = deepcopy(C_h)
                            min_distance[2] = deepcopy(C_r)

    else:

        min_distance = None
                   
    return min_distance



def self_collision_avoidance(robot_capsules):
    distance = []

    for i in (0, 1):
        if i == 0:
            for j in (2, 3):
                P1 = robot_capsules[i][0]
                Q1 = robot_capsules[i][1]
                P2 = robot_capsules[j][0]
                Q2 = robot_capsules[j][1]

                dist = distance_to_segment(P1, Q1, P2, Q2)
                
                distance.append(dist[0])

        if i == 1:
            j = 3

            P1 = robot_capsules[i][0]
            Q1 = robot_capsules[i][1]
            P2 = robot_capsules[j][0]
            Q2 = robot_capsules[j][1]

            dist = distance_to_segment(P1, Q1, P2, Q2)
            
            distance.append(dist[0])

    return distance



def distance_to_segment(P1, Q1, P2, Q2):    
    D1 = Q1-P1
    D2 = Q2-P2
    R = P1-P2
    a = np.inner(D1, D1)     
    b = np.inner(D1, D2) 
    c = np.inner(D1, R)
    e = np.inner(D2, D2)
    f = np.inner(D2, R)
    
    d = a*e-b*b

    s = (b*f-c*e)/d
    s = clamp((b*f-c*e)/d)
    
    t = (b*s+f)/e

    if t < 0.0:
        t = 0.0
        s = clamp(-c/a)
    
    elif t > 1.0:
        t = 1.0
        s = clamp((b-c)/a)
        
    C_h = P1+D1*s
    C_r = P2+D2*t            
    distance = math.sqrt(np.inner(C_h-C_r, C_h-C_r))
        
    return [distance, C_h, C_r]



def clamp(n):
    if n < 0:
        out = 0
    
    elif n > 1:
        out = 1
    
    else:
        out = n

    return out



def FlagStopServer(T_stop, q, q_p, q_pp): 

    flag_stop = False
    flag_human = False
    
    global do_once, t_i, rv, robot_capsules, depth, depth_intrinsic, detector
    
    img = []
    skeleton_real = []
    skeleton_proj = []

    if do_once == True:
        t_i = rospy.get_time()

        do_once = False

    # Skeleton Tracking             
    unaligned_frames = pipeline.wait_for_frames()
    frames = align.process(unaligned_frames)
    depth = frames.get_depth_frame()
    color = frames.get_color_frame()
    
    depth_image = np.asanyarray(depth.get_data())
    color_image = np.asanyarray(color.get_data())
    
    img = detector.findPose(color_image)
    
    img, skeleton_real = detector.getPosition(img, depth_image)
    
    # ****************** VIDEO RECORDING ******************

    if record:
        out.write(img)   #save a photogram

    # *****************************************************

    point_3D = skeleton_real 
    
    robot_capsules = compute_robot_capsules(q)   #rappresenta i giunti del robot
            
    r_sw_r = capsule_calculation(T_stop, q, q_p, q_pp)
    r_sw_h = [0.16, 0.05, 0.06, 0.05, 0.06, 0.15]
    #print(T_stop)
    print('raggi =', r_sw_r)
    self_collision_check = self_collision_avoidance(robot_capsules)   #verifica possibili collisioni tra segmenti del robot
   
    if np.any(self_collision_check) < 2*rv:
        flag_stop = True 
        #quit()
        
    if point_3D == []:
        flag_stop = False
    
    else:
        #for j in range(point_3D_multi[-1]): 
        for j in range(1):
            
            P2 = deepcopy(robot_capsules[0][0])
            Q2 = deepcopy(robot_capsules[0][1])
            
            #dist_check = distance_to_skeleton(point_3D, P2, Q2, r_sw_h)   #verifica uomo nello spazio operativo
            
            #if not dist_check == []:
            #    if dist_check[0] < 0.855:
            #        flag_human = True   # indica che l'uomo si trova dentro lo spazio operativo del robot

            min_distance = []
            do_once = 1
            
            for i in range(len(robot_capsules)):
                P2 = deepcopy(robot_capsules[i][0])
                Q2 = deepcopy(robot_capsules[i][1])
                
                dist = distance_to_skeleton(point_3D, P2, Q2, r_sw_h)
                #print(dist[0])
                if not dist == None:                   
                    dist[0] = dist[0] - r_sw_r[i]

                    if do_once:
                        min_distance.append(deepcopy(dist[0]))
                        do_once = 0
                                   
                    else:
                        if dist[0] < min_distance[0]:
                            min_distance[0] = deepcopy(dist[0])
                    
            if not min_distance == []:
                
                if min_distance[0] < 0.0:
                    flag_stop = True  
                              
                else:
                    flag_stop = False

            ## ******************* FILES WRITING *******************
#
            #t_f = rospy.get_time()
            #t_exp = t_f - t_i
#
            #if(stamp):
            #    
            #    # Write r_sw
            #    for i in range(len(r_sw_r)):
            #        fl_r_sw_r.write(f'{r_sw_r[i]} \t')
            #    
            #    fl_r_sw_r.write(f'{t_exp} \n')
#
            #    # Write point_3D
            #    for i in range(len(point_3D)):
            #        fl_point_3D.write(f'{point_3D[i]} \t')
            #    
            #    fl_point_3D.write(f'{t_exp} \n')
#
            #    # Write flag_stop
            #    fl_flag_stop.write(f'{int(flag_stop)} \t')
            #    fl_flag_stop.write(f'{t_exp} \n')
#
            #    # Write flag_human
            #    fl_flag_human.write(f'{int(flag_human)} \t')
            #    fl_flag_human.write(f'{t_exp} \n')
#
            #    if not dist == []:
            #        # Write distance
            #        fl_distance.write(f'{min_distance[0]} \t')
            #        fl_distance.write(f'{t_exp} \n')
#
            #        # Write C_h
            #        fl_C_h.write(f'{dist[1][0]} \t {dist[1][1]} \t {dist[1][2]} \t')
            #        fl_C_h.write(f'{t_exp} \n')
#
            #        # Write C_r
            #        fl_C_r.write(f'{dist[2][0]} \t {dist[2][1]} \t {dist[2][2]} \t')
            #        fl_C_r.write(f'{t_exp} \n')
            #    
            ## *****************************************************
    
    return(flag_stop)
              


def HandleFlagStop(req):    
    flag_stop = FlagStopServer(req.T_stop, req.q, req.q_p, req.q_pp)
        
    return FlagStopResponse(flag_stop)



def FlagStopServer1():
    rospy.init_node('flag_stop_server')

    global tester_name, test_number, out, fl_r_sw_r, fl_point_3D, fl_flag_stop, fl_flag_human, fl_distance, fl_C_h, fl_C_r

    file = open('/home/panda/Desktop/demo/test_data.txt', 'r')

    test_data = []

    for line in file:
        test_data.append(line.split('\n'))

    tester_name = test_data[0][0]
    test_number = test_data[1][0]

    ## ******************* FILES WRITING *******************
#
    ## Principal folder creation
    #path_name = f'/home/panda/Desktop/{tester_name}'
    #if not os.path.exists(path_name):
    #    os.makedirs(path_name)
#
    ## Secondary folder creation
    #path_name = f'/home/panda/Desktop/{tester_name}/test_{test_number}'
    #if not os.path.exists(path_name):
    #    os.makedirs(path_name)
#
    ## Third folder creation
    #sub_path_name = f'{path_name}/stop_trajectory_static'
    #if not os.path.exists(sub_path_name):
    #    os.makedirs(sub_path_name)        
    #
    ## Open files
    #fl_r_sw_r = open(sub_path_name + '/r_sw_r.txt', 'w')
    #fl_point_3D = open(sub_path_name + '/point_3D.txt', 'w')
    #fl_flag_stop = open(sub_path_name + '/flag_stop.txt', 'w')
    #fl_flag_human = open(sub_path_name + '/flag_human.txt', 'w')
    #fl_distance = open(sub_path_name + '/distance.txt', 'w')
    #fl_C_h = open(sub_path_name + '/C_h.txt', 'w')
    #fl_C_r = open(sub_path_name + '/C_r.txt', 'w')
    
    s = rospy.Service('flag_stop', FlagStop, HandleFlagStop)
    rospy.Rate(1/0.04)
    rospy.spin()



if __name__ == "__main__": 
    robot_capsules = []   
    rv = 0.125  # rv robot shell
    T_reaction = 0.05  # reaction time, con safety controller a 200 Hz
    csi = 0  # Zd+Zr; costante
    max_human_speed = 1.6
    max_robot_speed = 2

    color_image = None
    tester_name = None
    test_number = None
    out = None
    fl_r_sw_r = None 
    fl_point_3D = None
    fl_flag_stop = None
    fl_flag_human = None
    fl_distance = None
    fl_C_h = None
    fl_C_r = None
    t_i = None
     
    W = 1280
    H = 720      
    
    pipeline = rs.pipeline()
    config = rs.config() 

    ctx = rs.context()
    d = ctx.query_devices()[0]
    config.enable_device(d.get_info(rs.camera_info.serial_number))
    
    config.enable_stream(rs.stream.depth, W, H, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, W, H, rs.format.bgr8, 30)    
    config.enable_all_streams()
    
    pipeline.start(config)
    
    align = rs.align(rs.stream.color)
    
    unaligned_frames = pipeline.wait_for_frames()
    frames = align.process(unaligned_frames)
    depth = frames.get_depth_frame()
    depth_intrinsic = depth.profile.as_video_stream_profile().intrinsics

    detector = pm.PoseDetector()

    # ****************** VIDEO RECORDING ******************

    if record:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        path = '/home/panda/Desktop/mediapipe_output.avi'
        out = cv2.VideoWriter(path, fourcc, 17, (640, 480))

    # *****************************************************
        
    file = open('/home/panda/Desktop/demo/rotation_matrix.txt', 'r')

    do_once = True
    
    for line in file:
        array = line.split('\t')
        a = []            

        for i in range(4):
            a.append(float(array[i]))
        P = np.array([a])

        if do_once == True:
            R_0 = P

            do_once = False
        
        else:
            R_0 = np.concatenate((R_0, P), axis = 0)

    R_00 = np.linalg.inv(R_0)

    do_once = True

    print('Ready.')
        
    FlagStopServer1()

    pipeline.stop()
    cv2.destroyAllWindows()
    out.release()


