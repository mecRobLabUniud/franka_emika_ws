#!/usr/bin/env python3
# coding=utf-8

import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import DHRobot, RevoluteMDH
from math import pi, sin, cos, sqrt
from copy import deepcopy



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


def compute_robot_capsules(q):
    panda = rtb.models.DH.Panda()
    fk = panda.fkine_all(q).stack()
               
    robot_capsules = np.array([[fk[0:3, 3, 1], fk[0:3, 3, 0]],
                               [fk[0:3, 3, 3], fk[0:3, 3, 2]],
                               [fk[0:3, 3, 5], fk[0:3, 3, 4]],
                               [fk[0:3, 3, 7], fk[0:3, 3, 6]]])

    return robot_capsules


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
    
    D1 = Q1-P1
    D2 = Q2-P2
    R = P1-P2
    a = np.inner(D1, D1)     
    b = np.inner(D1, D2) 
    c = np.inner(D1, R)
    e = np.inner(D2, D2)
    f = np.inner(D2, R)              
                
    d = a*e-b*b

    if  d == 0:
        s = 0.0
        
        t = (b*s+f)/e
    
        if t < 0.0:
            t = 0.0
            s = clamp(-c/a)
        
        elif t > 1.0:
            t = 1.0
            s = clamp((b-c)/a)
        
    else:
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
    distance = sqrt(np.inner(C_h-C_r, C_h-C_r))
        
    return [distance, C_h, C_r]


def clamp(n):
    if n < 0:
        out = 0
    
    elif n > 1:
        out = 1
    
    else:
        out = n

    return(out)


def validator(q):
    y = 0  

    coll_valid = True 
   
    while(coll_valid and y < len(q)):
        distance = []

        robot_capsules = compute_robot_capsules(q[y])
        
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

        y += 1

        if np.any(distance) < 2*0.125 :
            coll_valid = False 

    return coll_valid



if __name__ == "__main__":

    path_name = '/home/panda/Desktop/path_datas'

    t, q, q_p, q_pp, q_ppp = file_reader()
 
    t = np.array(t)  
    q = np.array(q)
    q_p = np.array(q_p)
    q_pp = np.array(q_pp)
    q_ppp = np.array(q_ppp)
    
    print(validator(q))   #verifica possibili collisioni tra segmenti del robot
   
     