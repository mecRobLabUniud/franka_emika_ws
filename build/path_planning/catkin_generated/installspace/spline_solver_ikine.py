#!/usr/bin/env python3
# coding=utf-8

# Per conoscere i parametri da passare alla funzione ikine leggere il file python 
# nel percorso ~/robotics-toolbox-python/roboticstoolbox/robot/IK.py
# Informazioni sul toolbox sul sito: 
# https://github.com/petercorke/robotics-toolbox-python/wiki/Kinematics

import roboticstoolbox as rtb
import rospy
import numpy as np
from spatialmath import SE3
import math
import os
from trajectory_validator import validator as trj_validator
from self_collisions_validator import validator as scol_validator
from write_read_plot import writer, plotter



traj_file_name = 'pick_n_place'
t_traj = 15.6   #s
plot = 1

panda = rtb.models.DH.Panda()

def kovacic_system_solver(P, T, IC, FC):

    global N, giunti

    # Matrice H
    H = np.zeros((N-2, giunti))
    
    for j in range(giunti):
        H[0, j] = 6/(T[0, 0]**2)*(P[1, j]-P[0, j]) + 3/(T[0, 1]**2)*(P[2, j]-P[1, j])
        H[N-3, j] = 3/(T[0, N-3]**2)*(P[N-2, j]-P[N-3, j]) + 6/(T[0, N-2]**2)*(P[N-1, j]-P[N-2, j])

        for k in range(1, N-3):
            H[k, j] = 3/(T[0, k]*T[0, k+1])*((T[0, k]**2)*(P[k+2, j]-P[k+1, j]) + (T[0, k+1]**2)*(P[k+1, j]-P[k, j]))
    
    # Matrice M  
    M = np.zeros((N-2, N-2, giunti))

    for j in range(giunti):
        M[0, 0, j] = 3/T[0, 0] + 2/T[0, 1]
        M[0, 1, j] = 1/T[0, 1]
        
        M[N-3, (N-3)-1, j] = 1/T[0, N-3]
        M[N-3, N-3, j] = 2/T[0, N-3] + 3/T[0, N-2]
        
        for k in range(1, N-3):
            M[k, k-1, j] = T[0, k+1]
            M[k, k, j] = 2*(T[0, k] + T[0, k+1])
            M[k, k+1, j] = T[0, k]
            
    # Matrice D
    D = np.zeros((N-2, giunti))

    for j in range(giunti):  
        D[:, j] = np.linalg.solve(M[:, :, j], H[:, j])

    # Matrice V
    V = np.zeros((N, giunti))
    V[0, :] = IC[0, :]
    V[N-1, :] = FC[0, :]
    V[1:N-1, :] = D

    return V


class spline_solver():

    global N, giunti

    def __init__(self, P, V, T):

        B4iniz = self.fourth_degree_coeff_35(P, V, T)
        B3 = self.third_degree_coeff_23(P, V, T)
        B4fin = self.fourth_degree_coeff_41(P, V, T)

        B = np.zeros((5, N-1, giunti))

        B[:, 0, :] = B4iniz[:, 0, :]
        B[:, N-2, :] = B4fin[:, 0, :]
        
        for j in range(1, N-2):
            B[:, j, :] = B3[:, j-1, :] 

        self.parameter_matrix = B


    def fourth_degree_coeff_35(self, P, V, T):
        
        B4iniz = np.zeros((5, 1, giunti))

        for j in range(giunti):  

            vett = np.matrix([P[0, j], P[1, j], V[0, j], V[1, j]])
            vett = vett.transpose()
            
            B4iniz[0, 0, j] = np.dot(np.matrix([1, 0, 0, 0]), vett)
            B4iniz[1, 0, j] = np.dot(np.matrix([0, 0, 0, 0]), vett)
            B4iniz[2, 0, j] = np.dot(np.matrix([0, 0, 0, 0]), vett)
            B4iniz[3, 0, j] = np.dot(np.matrix([-4/T[0, 0]**3, 4/T[0, 0]**3, 0, -1/T[0, 0]**2]), vett)
            B4iniz[4, 0, j] = np.dot(np.matrix([3/T[0, 0]**4, -3/T[0, 0]**4, 0, 1/T[0, 0]**3]), vett)

        return B4iniz


    def third_degree_coeff_23(self, P, V, T):

        B3 = np.zeros((5, N-3, giunti))

        for j in range(giunti):  

            for k in range(N-3):  
                
                vett = np.matrix([P[k+1, j], P[k+2, j], V[k+1, j], V[k+2, j]])
                vett = vett.transpose()

                B3[0, k, j] = np.dot(np.matrix([1, 0, 0, 0]), vett)
                B3[1, k, j] = np.dot(np.matrix([0, 0, 1, 0]), vett)
                B3[2, k, j] = np.dot(np.matrix([-3/T[0, k+1]**2, 3/T[0, k+1]**2, -2/T[0, k+1], -1/T[0, k+1]]), vett)
                B3[3, k, j] = np.dot(np.matrix([2/T[0, k+1]**3, -2/T[0, k+1]**3, 1/T[0, k+1]**2, 1/T[0, k+1]**2]), vett)  

        B3[4, :, :] = 0 

        return B3  


    def fourth_degree_coeff_41(self, P, V, T):

        B4fin = np.zeros((5, 1, giunti))

        for j in range(giunti): 

            vett = np.matrix([P[N-2, j], P[N-1, j], V[N-2, j], V[N-1, j]])
            vett = vett.transpose()

            B4fin[0, 0, j] = np.dot(np.matrix([1, 0, 0, 0]), vett)
            B4fin[1, 0, j] = np.dot(np.matrix([0, 0, 1, 0]), vett)
            B4fin[2, 0, j] = np.dot(np.matrix([-6/T[0, N-2]**2, 6/T[0, N-2]**2, -3/T[0, N-2], 0]), vett)
            B4fin[3, 0, j] = np.dot(np.matrix([8/T[0, N-2]**3, -8/T[0, N-2]**3, 3/T[0, N-2]**2, 0]), vett)
            B4fin[4, 0, j] = np.dot(np.matrix([-3/T[0, N-2]**4, 3/T[0, N-2]**4, -1/T[0, N-2]**3, 0]), vett)

        return B4fin


def trajectory_creator(B):

    global passo, giunti

    t = np.zeros((1+(N-1)*passo, 1))   
    q = np.zeros((1+(N-1)*passo, giunti))
    q_p = np.zeros((1+(N-1)*passo, giunti))
    q_pp = np.zeros((1+(N-1)*passo, giunti))
    q_ppp = np.zeros((1+(N-1)*passo, giunti))
    
    for j in range(giunti):
        q[0, j] = B[0, 0, j]
        q_p[0, j] = B[1, 0, j]
        q_pp[0, j] = 2*B[2, 0, j]
        q_ppp[0, j] = 6*B[3, 0, j]
        
    t_n = [0] 

    for i in range(N-1):
        incr = T[0, i]/passo  

        for n in range(passo):  
            t_n.append(incr*(n+1))
    
    for j in range(giunti):
        for i in range(N-1):  
            for n in range(passo):
                inst = 1 + i*passo + n
                
                q[inst, j] = B[0, i, j] + B[1, i, j]*t_n[inst] + B[2, i, j]*t_n[inst]**2 + B[3, i, j]*t_n[inst]**3 + B[4, i, j]*t_n[inst]**4
                
                q_p[inst, j] = B[1, i, j] + 2*B[2, i, j]*t_n[inst] + 3*B[3, i, j]*t_n[inst]**2 + 4*B[4, i, j]*t_n[inst]**3

                q_pp[inst, j] = 2*B[2, i, j] + 6*B[3, i, j]*t_n[inst] + 12*B[4, i, j]*t_n[inst]**2

                q_ppp[inst, j]= 6*B[3, i, j] + 24*B[4, i, j]*t_n[inst]  

    t_prev = [0]
    
    for i in range(N-1):
        incr = T[0, i]/passo  

        for n in range(passo):
            t[10*i + (n+1)] = incr*(n+1) + t_prev[0]  ############## sbagliato
            
        t_prev[0] = t[10*i + (n+1)]
 
    return t, q, q_p, q_pp, q_ppp


def centr_distribution(P, N, giunti):

    T0 = np.zeros((N-1, 1))

    d = np.zeros((1, giunti))
    
    for i in range(giunti):
        for k in range(N-1):
            dk = (abs(P[k+1, i] - P[k, i]))**0.5
            d[0, i] = d[0, i] + dk
 
    for k in range(N-1):
        t = 0
        for i in range(giunti):
            dk = (abs(P[k+1, i] - P[k, i]))**0.5
            tk = dk/d[0, i]
            if tk > t:
                t = tk
                        
        T0[k] = t

    return T0


def inverse_kinematics_solver(n):
    
    N = np.zeros((len(n), 7))
    q0 = [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]

    for i in range(len(n)):
        
        p = SE3(n[i])*SE3.RPY([0.0, 0.0, math.pi], order='xyz')
        print('loading... ', i,'/',len(n)-1)
        
        print(p)  
             
        sol = panda.ikine_LM(p, q0=q0)                    
        N[i, :] = np.matrix(sol.q) 

        q0 = sol.q   
    
    return N



if __name__ == '__main__':
    rospy.init_node('spline_solver')

        # Write p matrix -----------------------------
    P = []

    # Read via points -----------------------------
    file = open(f'/home/panda/Desktop/demo/path_trajectory/{traj_file_name}.txt','r')

    for line in file:
        data = line.split('\t')
        
        S = []
        for p in data[0:-1]:
            S.append(float(p))
        
        P.append(S)
    
    file.close()
    
    # ---------------------------------------------
    print(P)
    P = inverse_kinematics_solver(P)
    N, giunti = P.shape
    print(P)
    IC = np.matrix([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    FC = np.matrix([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])

    passo = 10
    
    T0 = centr_distribution(P, N, giunti)  
    print('T0 = ',T0)
    x0 = 0
    for i in range(len(T0)):
        x0 = x0 + T0[i, 0] 
    
    T = np.dot(T0, (t_traj/x0))

    T = np.matrix(T)
    T = T.transpose()

    V = kovacic_system_solver(P, T, IC, FC)

    # Creation of spline_solver class object
    spline = spline_solver(P, V, T)
    
    t, q, q_p, q_pp, q_ppp = trajectory_creator(spline.parameter_matrix)
    print(t)
    print(q)
    print('Self collision check = ', scol_validator(q))     
    print('Kinematics and dynamics limits check = ', trj_validator(t, q, q_p, q_pp, q_ppp))
    
    # Saving datas to files ------------------------
    path_name = f'/home/panda/Desktop/DATA/traj_{round(float(t[-1][0]), 1)}s'
    if not os.path.exists(path_name):
        os.makedirs(path_name)
    writer(path_name, t, q, q_p, q_pp, q_ppp, [], [], 'q', '')
    
    if plot:
        plotter(path_name, t, q, q_p, q_pp, q_ppp, [], [])



    
