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

panda = rtb.models.DH.Panda()

def inverse_kinematics_solver(n):
    
    q0 = [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]

    p = SE3(n)*SE3.RPY([0.0, 0.0, math.pi], order='xyz') 
            
    sol = panda.ikine_LM(p, q0=q0)                    
    Q = sol.q
    
    return Q



if __name__ == '__main__':
        # Write p matrix -----------------------------
    P = [0.3, 0.1, 0.2]

    Q = inverse_kinematics_solver(P)

    print(Q)


    
