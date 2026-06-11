#!/usr/bin/env python3
# coding=utf-8

# Per conoscere i parametri da passare alla funzione ikine leggere il file python 
# nel percorso ~/robotics-toolbox-python/roboticstoolbox/robot/IK.py
# Informazioni sul toolbox sul sito: 
# https://github.com/petercorke/robotics-toolbox-python/wiki/Kinematics

import roboticstoolbox as rtb
import numpy as np
from spatialmath import SE3
import math
import casadi as ca
from copy import deepcopy



traj_file_name = 'pick_n_place'
t_traj = 20   #s
plot = 1

panda = rtb.models.DH.Panda()

def kovacic_system_solver(P, T, IC, FC):

    global N, giunti

    # Matrice H
    H = ca.SX.zeros(N-2, giunti)

    for j in range(giunti):
        H[0, j] = 6/(T[0, 0]**2)*(P[1, j]-P[0, j]) + 3/(T[0, 1]**2)*(P[2, j]-P[1, j])
        H[N-3, j] = 3/(T[0, N-3]**2)*(P[N-2, j]-P[N-3, j]) + 6/(T[0, N-2]**2)*(P[N-1, j]-P[N-2, j])

        for k in range(1, N-3):
            H[k, j] = 3/(T[0, k]*T[0, k+1])*((T[0, k]**2)*(P[k+2, j]-P[k+1, j]) + (T[0, k+1]**2)*(P[k+1, j]-P[k, j]))
    
    # Matrice M  
    L = ca.SX.zeros(N-2, N-2)
    M = []

    for j in range(giunti):
        L[0, 0] = 3/T[0, 0] + 2/T[0, 1]
        L[0, 1] = 1/T[0, 1]
        
        L[N-3, (N-3)-1] = 1/T[0, N-3]
        L[N-3, N-3] = 2/T[0, N-3] + 3/T[0, N-2]
        
        for k in range(1, N-3):
            L[k, k-1] = T[0, k+1]
            L[k, k] = 2*(T[0, k] + T[0, k+1])
            L[k, k+1] = T[0, k]
        M.append(L)
    
    # Matrice D
    D = ca.SX.zeros(N-2, giunti)

    for j in range(giunti):  
        D[:, j] = ca.solve(M[j][:, :], H[:, j])
    
    # Matrice V
    V = ca.SX.zeros(N, giunti)
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
        
        B = []
        L = np.zeros((5, N-1))

        for j in range(giunti):

            L[:, 0] = B4iniz[j][:, 0]
            L[:, N-2] = B4fin[j][:, 0]
            
            for i in range(1, N-2):
                L[:, i] = B3[j][:, i-1] 

            B.append(deepcopy(L))

        self.parameter_matrix = B


    def fourth_degree_coeff_35(self, P, V, T):
        B4iniz = []
        L = ca.SX.zeros((5, 1))
        
        for j in range(giunti):
            vett = np.matrix([P[0, j], P[1, j], V[0, j], V[1, j]])
            #vett = vett.transpose()

            L[0, 0] = ca.dot(np.matrix([1, 0, 0, 0]), vett)
            L[1, 0] = ca.dot(np.matrix([0, 0, 0, 0]), vett)
            L[2, 0] = ca.dot(np.matrix([0, 0, 0, 0]), vett)
            L[3, 0] = ca.dot(np.matrix([-4/T[0, 0]**3, 4/T[0, 0]**3, 0, -1/T[0, 0]**2]), vett)
            L[4, 0] = ca.dot(np.matrix([3/T[0, 0]**4, -3/T[0, 0]**4, 0, 1/T[0, 0]**3]), vett)

            B4iniz.append(deepcopy(L))

        return B4iniz


    def third_degree_coeff_23(self, P, V, T):
        B3 = []
        L = ca.SX.zeros((5, N-3))

        for j in range(giunti): 
            for k in range(N-3):                 
                vett = np.matrix([P[k+1, j], P[k+2, j], V[k+1, j], V[k+2, j]])
                #vett = vett.transpose()

                L[0, k] = ca.dot(np.matrix([1, 0, 0, 0]), vett)
                L[1, k] = ca.dot(np.matrix([0, 0, 1, 0]), vett)
                L[2, k] = ca.dot(np.matrix([-3/T[0, k+1]**2, 3/T[0, k+1]**2, -2/T[0, k+1], -1/T[0, k+1]]), vett)
                L[3, k] = ca.dot(np.matrix([2/T[0, k+1]**3, -2/T[0, k+1]**3, 1/T[0, k+1]**2, 1/T[0, k+1]**2]), vett)  

            L[4, :] = 0
            B3.append(deepcopy(L))

        return B3  


    def fourth_degree_coeff_41(self, P, V, T):
        B4fin = []
        L = ca.SX.zeros((5, 1))

        for j in range(giunti): 
            vett = np.matrix([P[N-2, j], P[N-1, j], V[N-2, j], V[N-1, j]])
            #vett = vett.transpose()

            L[0, 0] = ca.dot(np.matrix([1, 0, 0, 0]), vett)
            L[1, 0] = ca.dot(np.matrix([0, 0, 1, 0]), vett)
            L[2, 0] = ca.dot(np.matrix([-6/T[0, N-2]**2, 6/T[0, N-2]**2, -3/T[0, N-2], 0]), vett)
            L[3, 0] = ca.dot(np.matrix([8/T[0, N-2]**3, -8/T[0, N-2]**3, 3/T[0, N-2]**2, 0]), vett)
            L[4, 0] = ca.dot(np.matrix([-3/T[0, N-2]**4, 3/T[0, N-2]**4, -1/T[0, N-2]**3, 0]), vett)

            B4fin.append(deepcopy(L))

        return B4fin


def trajectory_creator(B):

    global passo, giunti

    t = ca.SX.zeros((1+(N-1)*passo, 1))   
    q = ca.SX.zeros((1+(N-1)*passo, giunti))
    q_p = ca.SX.zeros((1+(N-1)*passo, giunti))
    q_pp = ca.SX.zeros((1+(N-1)*passo, giunti))
    q_ppp = ca.SX.zeros((1+(N-1)*passo, giunti))
    
    for j in range(giunti):
        q[0, j] = B[j][0, 0]
        q_p[0, j] = B[j][1, 0]
        q_pp[0, j] = 2*B[j][2, 0]
        q_ppp[0, j] = 6*B[j][3, 0]
        
    t_n = [0] 

    for i in range(N-1):
        incr = T[0, i]/passo  

        for n in range(passo):  
            t_n.append(incr*(n+1))
    
    for j in range(giunti):
        for i in range(N-1):
            for n in range(passo):
                inst = 1 + i*passo + n
                
                q[inst, j] = B[j][0, i] + B[j][1, i]*t_n[inst] + B[j][2, i]*t_n[inst]**2 + B[j][3, i]*t_n[inst]**3 + B[j][4, i]*t_n[inst]**4
                
                q_p[inst, j] = B[j][1, i] + 2*B[j][2, i]*t_n[inst] + 3*B[j][3, i]*t_n[inst]**2 + 4*B[j][4, i]*t_n[inst]**3

                q_pp[inst, j] = 2*B[j][2, i] + 6*B[j][3, i]*t_n[inst] + 12*B[j][4, i]*t_n[inst]**2

                q_ppp[inst, j]= 6*B[j][3, i] + 24*B[j][4, i]*t_n[inst]  

    t_prev = [0]
    
    if not passo == 1:
        for i in range(N-1):
            incr = T[0, i]/passo  

            for n in range(passo):
                t[10*i + (n+1)] = incr*(n+1) + t_prev[0]
                
            t_prev[0] = t[10*i + (n+1)]

    else:
        for i in range(N-1):
            incr = T[0, i] 
            t[i+1] = incr + t_prev[0]
                
            t_prev[0] = t[i+1]
    
    return t, q, q_p, q_pp, q_ppp


def inverse_kinematics_solver(n):
    
    N = ca.SX.zeros((len(n), 7))
    q0 = [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]

    for i in range(len(n)):
        
        p = SE3(n[i])*SE3.RPY([0.0, 0.0, math.pi], order='xyz')
        print('loading... ', i,'/',len(n)-1)
        
        #print(p)  
             
        sol = panda.ikine_LMS(p, q0=q0)                    
        N[i, :] = np.matrix(sol.q) 

        q0 = sol.q   
    
    return N



if __name__ == '__main__':
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
    
    P = np.matrix(P)
    N, giunti = P.shape

    IC = np.matrix([[0, 0, 0], [0, 0, 0]])
    FC = np.matrix([[0, 0, 0], [0, 0, 0]])

    passo = 10
    
    T = ca.SX.sym('T', 1, N-1)
                
    V = kovacic_system_solver(P, T, IC, FC)
    
    # Creation of spline_solver class object
    spline = spline_solver(P, V, T)
    
    t, q, q_p, q_pp, q_ppp = trajectory_creator(spline.parameter_matrix)
    
    P = inverse_kinematics_solver(q)
    
    N, giunti = P.shape

    IC = np.matrix([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    FC = np.matrix([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])

    t_i = []
    for i in range(N-1):
        t_i.append(t_traj/(N-1))

    T_new = []
    for i in range(T.shape[1]):
        for j in range(passo):
            T_new.append(T[0, i]/passo)
    
    T = np.matrix(T_new)
        
    V = kovacic_system_solver(P, T, IC, FC)
    
    # Creation of spline_solver class object
    spline = spline_solver(P, V, T)
    passo = 1
    
    t, q, q_p, q_pp, q_ppp = trajectory_creator(spline.parameter_matrix)
    print(t)

    
