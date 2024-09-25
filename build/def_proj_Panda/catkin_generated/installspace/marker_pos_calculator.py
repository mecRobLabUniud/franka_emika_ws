#!/usr/bin/env python3
# coding=utf-8

import numpy as np
import math
from math import cos, sin, pi, atan2
from copy import deepcopy

def compute_end_effector(DH, q):
    T_k = np.identity(4)

    for j in range(7):        
        a = DH[j, 0]
        alpha = DH[j, 1]
        d = DH[j, 3]
        theta = q[j]+DH[j, 2]
              
        T = np.array([[cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha),  a*cos(theta)],
                      [sin(theta), cos(theta)*cos(alpha),  -cos(theta)*sin(alpha), a*sin(theta)],
                      [0,          sin(alpha),             cos(alpha),             d],
                      [0,          0,                      0,                      1]])
                
        T_k = deepcopy(np.dot(T_k, T))  
    
    R = T_k   

    return R


if __name__ == "__main__":
    q_multi = np.array([[-0.052503843748625836, 0.6897211279521458, -0.12053761146919999, -2.307009646732263, 0.17733034705225423, 2.7102391534766936, 0.8096250286073321],
                        [0.07552464062559527, 0.6803180845494856, 0.040927349743092076, -2.317529094500005, 0.1769062976451348, 2.710952746152878, 0.8096849585610131],
                        [0.1276289547345091, 0.6093907501823077, 0.07926810990997536, -2.7679113046585164, 0.17641428204144727, 3.189057566404342, 0.8056189289339967],
                        [-0.0072593103583883265, 0.6300199648770047, -0.1634515040541001, -2.753694295613193, 0.17566866370992143, 3.1896435261567433, 0.8056495370835893]])

    DH = np.array([[0,    -pi/2,  0, 0.333],
                   [0,    -pi/2, pi, 0],
                   [0.088, pi/2, pi, 0.316],
                   [0.088, pi/2, pi, 0],
                   [0,     pi/2, pi, 0.384],
                   [0.088, pi/2, 0,  0],
                   [0,     0,    0,  0.107]])

    p = []

    for i in range(len(q_multi)):
        q = deepcopy(q_multi[i])
        
        R = compute_end_effector(DH, q)

        A = np.array([[1, 0, 0, 0   ],
                      [0, 1, 0, 0   ],
                      [0, 0, 1, 0.05],
                      [0, 0, 0, 1   ]]) 

        E = np.dot(R, A)

        p.append([E[0][3], E[1][3], E[2][3]])

    A1 =[]
    A2 =[]
    A3 =[]
    A4 =[]

    for j in range(3):
        A1.append((p[0][j] + p[1][j])/2)
        A2.append((p[2][j] + p[3][j])/2)
        A3.append((p[0][j] + p[3][j])/2)
        A4.append((p[1][j] + p[2][j])/2)

    C1 = []
    C2 = []

    for j in range(3):
        C1.append((A1[j] + A2[j])/2)
        C2.append((A3[j] + A4[j])/2)

    C = []

    for j in range(3):
        C.append(-(C1[j] + C2[j])/2)   #inverto i segni per poter portare l'array come variabile marker_pos in base_rotation_matrix_subscriber.py 

    print(C)
       
    

