#!/usr/bin/env python3
# coding=utf-8

import cv2
import mediapipe as mp
import time
import numpy as np
from copy import deepcopy

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
"""

joints_num = [11, 12, 13, 14, 15, 16, 33, 34, 35]
joints_segm = [[6, 7], [7, 0], [7, 1], [7, 8], [0, 2], [2, 4], [1, 3], [3, 5]]

class PoseDetector:

    def __init__(self, mode = True, upBody = False, smooth = True, detectionCon = 0.1, trackCon = 1):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)


    def findPose(self, img, draw=True):

        imgRGB = img
        self.results = self.pose.process(imgRGB)
        
        return imgRGB


    def getPosition(self, img, depth_img, draw=True):
        
        skeleton_proj = []
        skeleton_real = []
                
        if self.results.pose_landmarks:
            
            h, w, c = img.shape
                        
            # Creazione giunto testa
            joints = self.results.pose_landmarks.landmark
            joints.append(joints[0])
            joints[-1].x = (joints[7].x + joints[8].x)/2
            joints[-1].y = (joints[7].y + joints[8].y)/2
            joints[-1].z = (joints[7].z + joints[8].z)/2

            # Creazione giunto collo
            joints.append(joints[0])
            joints[-1].x = (joints[11].x + joints[12].x)/2
            joints[-1].y = (joints[11].y + joints[12].y)/2
            joints[-1].z = (joints[11].z + joints[12].z)/2

            # Creazione giunto centro anche
            joints.append(joints[0])
            joints[-1].x = (joints[23].x + joints[24].x)/2
            joints[-1].y = (joints[23].y + joints[24].y)/2
            joints[-1].z = (joints[23].z + joints[24].z)/2
                    
            for id, lm in enumerate(joints):
                if id in joints_num:
                
                    if lm.visibility >= 0.25:                                
                        if lm.x >= 1.0:
                            lm.x = 0.999999999
                        elif lm.x <= 0.0:
                            lm.x = 0.000000001
                        
                        if lm.y >= 1.0:
                            lm.y = 0.999999999
                        elif lm.y <= 0.0:
                            lm.y = 0.000000001

                        cx = int(lm.x*w)
                        cy = int(lm.y*h)
                        if cx == w or cy == h:
                            cx = cx-1
                            cy = cy-1
                        
                        cz = depth_img[cy, cx]

                        # lunghezza focale = 1.93 mm
                        focal_length = 957.042
                        dim_eff = 0.311  #mm
                        au = focal_length
                        av = focal_length
                        u0 = w/2
                        v0 = h/2

                        A = np.matrix([[1/au, 0, 0, -u0/au], 
                                        [0, 1/av, 0, -v0/av], 
                                        [0, 0, 0, 1], 
                                        [0, 0, 1, 0]])

                        B = np.matrix([[cx],
                                        [cy],
                                        [1/cz],
                                        [1]])

                        M = np.dot(A, B)
                        M = M*cz
                        
                        skeleton_proj.append((cx, cy, cz))
                        skeleton_real.append([int(M[0]), -int(M[1]), int(M[2])])
                    else:
                        skeleton_proj.append(0)
                        skeleton_real.append([-999000.0, -999000.0, -999000.0])

            for s in joints_segm:
                if skeleton_proj[s[0]] and skeleton_proj[s[1]]:

                    cv2.line(img, (skeleton_proj[s[0]][0], skeleton_proj[s[0]][1]), (skeleton_proj[s[1]][0], skeleton_proj[s[1]][1]), (0, 255, 0), 2)

            for n in range(len(skeleton_proj)):
                if skeleton_proj[n]:                
                               
                    cv2.circle(img, (skeleton_proj[n][0],skeleton_proj[n][1]), 2, (0, 0, 255), -1)

            for j in range(len(skeleton_real)):
                skeleton_real[j] = deepcopy((skeleton_real[j][0]/1000, skeleton_real[j][2]/1000, skeleton_real[j][1]/1000))
        
        return img, skeleton_real

