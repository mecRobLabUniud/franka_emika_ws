#!/usr/bin/env python3
# coding=utf-8

import rospy
from control_msgs.msg import FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from copy import deepcopy
import time
import numpy as np
from write_read_plot import reader, writer
import socket

#/home/panda/Documents/Data_Optimizer/Trajectories


if __name__ == "__main__":
    HOST = "172.16.1.1"  # Standard loopback interface address (localhost)
    PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

    #TCP input
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen() 

        try:
            while True:  
                         
                conn, addr = s.accept()
                print("ciclando")
                with conn:
                    data = conn.recv(1024)
                    
                    file = open(f"/home/panda/Desktop/{data.decode()}_TCP.txt", "wb")
                    
                    while data:
                        if data == b"END":
                            break                   
                        
                        data = conn.recv(1024)
                        file.write(data)
                        print(data)
                        
                    print("fine ricezione")    
                    s.close()
                    print("socket chiuso")

                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((HOST, PORT))
                    s.listen() 
                    print("socket aperto")
        except:
            s.close()
        
        s.close()
            


