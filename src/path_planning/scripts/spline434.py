#!/usr/bin/env python
# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import scipy.io


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

    def __init__(self):

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
       
    q = np.zeros((1+(N-1)*passo, giunti))
    q_p = np.zeros((1+(N-1)*passo, giunti))
    q_pp = np.zeros((1+(N-1)*passo, giunti))
    q_ppp = np.zeros((1+(N-1)*passo, giunti))
    
    for j in range(giunti):
        q[0, j] = B[0, 0, j]
        q_p[0, j] = B[1, 0, j]
        q_pp[0, j] = 2*B[2, 0, j]
        q_ppp[0, j] = 6*B[3, 0, j]
        
    t = [0] 
    
    for i in range(N-1):
        incr = T[0, i]/passo  

        for n in range(passo):  
            t.append(incr*(n+1))
    
    for j in range(giunti):
        for i in range(N-1):  
            for n in range(passo):
                inst = 1 + i*passo + n
                
                q[inst, j] = B[0, i, j] + B[1, i, j]*t[inst] + B[2, i, j]*t[inst]**2 + B[3, i, j]*t[inst]**3 + B[4, i, j]*t[inst]**4
                
                q_p[inst, j] = B[1, i, j] + 2*B[2, i, j]*t[inst] + 3*B[3, i, j]*t[inst]**2 + 4*B[4, i, j]*t[inst]**3

                q_pp[inst, j] = 2*B[2, i, j] + 6*B[3, i, j]*t[inst] + 12*B[4, i, j]*t[inst]**2

                q_ppp[inst, j]= 6*B[3, i, j] + 24*B[4, i, j]*t[inst]  

    return t, q, q_p, q_pp, q_ppp




if __name__ == '__main__':


    P = 10**-3*np.matrix([[0, 0, 10, 30, 175, 320, 340, 350, 350],
                 [0, 0, 12.9, 38.6, 225, 411.4, 437.1, 450, 450],
                 [0, 170, 190, 200, 200, 200, 190 , 170, 0]])
    
    P = P.transpose()
    
    IC = np.matrix([[0, 0, 0], [0, 0, 0]])
    FC = np.matrix([[0, 0, 0], [0, 0, 0]])
    
    T = np.matrix([.3, .1, .1, .15, .15, .1, .1, .3])

    passo = 100
    
    N, giunti = P.shape
 
    # Coeff. della Spline di 4° e 5° ordine tra i punti via  per ogni giunto%%
    V = kovacic_system_solver(P, T, IC, FC)

    spline = spline_solver()
    
    t, q, q_p, q_pp, q_ppp = trajectory_creator(spline.parameter_matrix)

    #ax = plt.axes(projection='3d')
#
    #ax.set_xlabel('x')
    #ax.set_ylabel('y')
    #ax.set_zlabel('z')
    #ax.set_xlim(-1, 1)
    #ax.set_ylim(-1, 1)
    #ax.set_zlim(-1, 1)
    #ax.view_init(10,-80)
#
    #for n in range(len(q)):
    #    ax.scatter3D(q[n, 0], q[n, 1], q[n, 2],'+r')
#
    #plt.show()

    mat = scipy.io.loadmat('data_spline.mat')
    
    q_mat = mat.get('q')
    q_p_mat = mat.get('vel')
    q_pp_mat = mat.get('acc')
    q_ppp_mat = mat.get('jerk')

    print(np.allclose(q, q_mat, rtol=1e-10, atol=1e-12, equal_nan=False))
    print(np.allclose(q_p, q_p_mat, rtol=1e-10, atol=1e-12, equal_nan=False))
    print(np.allclose(q_pp, q_pp_mat, rtol=1e-10, atol=1e-12, equal_nan=False))
    print(np.allclose(q_ppp, q_ppp_mat, rtol=1e-10, atol=1e-12, equal_nan=False))


