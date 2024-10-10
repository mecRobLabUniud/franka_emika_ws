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
import os

# per bloccare processo: kill -9 $(lsof -ti tcp:8080)

HOST = "172.16.1.1"  # Standard loopback interface address (localhost)
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

path = "/home/panda/Documents/Data_Optimizer/"
nm = ["t", "q", "q_p", "q_pp"]
folder = None
q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])    # rad/s
t_i = None
t_exp = []
q_exp = []
q_p_exp = []
tau_exp = []


def CallbackJointStates(data):
    global t_i, t_exp, q_exp, q_p_exp, tau_exp

    t = rospy.get_time()

    t_exp.append([t - t_i])  
    q_exp.append(data.position[0:7])
    q_p_exp.append(data.velocity)
    tau_exp.append(data.effort)



def data_receiver():
    global folder 

    fileI = open(f"{path}Input.txt", "w")

    while True: 
        #TCP input
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen() 

            try:                            
                conn, addr = s.accept()
                
                with conn:
                    data = conn.recv(10)
                    
                    if data == b"END":
                        break
                    else:
                        if not folder == data.decode():
                            print(f"Acquiring {data.decode()}")
                            fileI.write(f"{data.decode()}\n")
                            
                        folder = data.decode()

                    data = conn.recv(10)
                    
                    if not os.path.exists(f"{path}Trajectories/{folder}"):
                        os.mkdir(f"{path}Trajectories/{folder}")
                    file = open(f"{path}Trajectories/{folder}/{data.decode()}.txt", "wb")
                    
                    while data:
                        data = conn.recv(1024)
                        file.write(data)
                    file.close()

            except:
                print("Connection error")
                quit()
            
            s.close()

    fileI.close()




def test_manager():
    global t_i, t_exp, q_exp, q_p_exp, tau_exp

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        try:
            while True:            
                conn, addr = s.accept()
                
                with conn:
                    data = conn.recv(1024)
                    print("-------- DATA = ", data)
                    if data == b'STOP':
                        conn.close()
                        print('Disconnected')
                        s.close()

                        time.sleep(1)
                        
                        print('Test execution finished')
                        break

                    print(f"Connected with {addr}")
                    print('Moving to the starting configuration')
                    
                    # Reading data to files ------------------------
                    path_name = f'/home/panda/Documents/{data.decode()}'

                    
                    t, q, q_p, q_pp, q_ppp, tau, tau_p = reader(path_name, 'q', '')
                    
                    t_i = rospy.get_time()
                    
                    
                    # Initialization subscriber node for /joint_states
                    sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)
                    
                    # Initialization publisher node for /position_joint_trajectory_controller/follow_joint_trajectory/goal
                    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)
                    
                    t_start = [] 
                    t_exp = []
                    q_exp = []
                    q_p_exp = []
                    tau_exp = []    

                    time.sleep(0.4)

                    for i in range(len(q[0])):
                        d = abs(q_exp[-1][i]-q[0][i])
                        t_start.append(d/(0.15*q_p_lim[i])+1)

                    # Move to start configuration
                    msg = FollowJointTrajectoryActionGoal()

                    msg.header.stamp = rospy.Duration(0)
                    msg.header.frame_id = ''
                    msg.goal.trajectory.header.stamp = rospy.Duration(0)
                    msg.goal.trajectory.header.frame_id = ''
                    msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']

                    # Write trajectory message
                    point = JointTrajectoryPoint()
                    point.positions = q[0]
                    point.velocities = [0, 0, 0, 0, 0, 0, 0]
                    point.accelerations = [0, 0, 0, 0, 0, 0, 0]
                    point.effort = []
                    point.time_from_start = rospy.Duration(max(t_start))
                    msg.goal.trajectory.points.append(deepcopy(point))

                    time.sleep(0.4)
                    
                    # Move to start configuration
                    control_publisher.publish(msg)

                    # Wait the end of the trajectory
                    time.sleep(max(t_start))

                    # Creation of trajectory message --------------
                    msg = FollowJointTrajectoryActionGoal()

                    msg.header.stamp = rospy.Duration(0)
                    msg.header.frame_id = ''
                    msg.goal.trajectory.header.stamp = rospy.Duration(0)
                    msg.goal.trajectory.header.frame_id = ''
                    msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']      

                    # Write trajectory message
                    for i in range(len(t)):
                        point = JointTrajectoryPoint()
                        point.positions = q[i]
                        point.velocities = q_p[i]
                        point. accelerations = q_pp[i]
                        point.effort = []
                        point.time_from_start = rospy.Duration(t[i][0])
                        msg.goal.trajectory.points.append(deepcopy(point))

                    if data:
                        conn.send(b'START')
                        conn.close()

                        time.sleep(0.2)

                        print('Trajectory execution')
                        
                        # Move to configuration
                        control_publisher.publish(msg)
                        
                        t_i = rospy.get_time()
                        t_exp = []
                        q_exp = []
                        q_p_exp = []
                        tau_exp = []

                        time.sleep(t[-1][0])
                        
                        sub_joint_states.unregister()
                    
                        t_exp = np.array(t_exp)
                        q_exp = np.array(q_exp)
                        q_p_exp = np.array(q_p_exp)
                        tau_exp = np.array(tau_exp)
                        
                        writer(path_name, t_exp, q_exp, q_p_exp, [], [], tau_exp, [], 'q', '_exp')

            s.close()
        except:
            print("Connection error")
            quit()



def data_sender():
    file = open(f"{path}Input.txt", "r")
    data = file.read()
    for row in data.split("\n"):
        if row == "":
            continue
        print(f"Sending {row}")

        for i in range(len(nm)):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                time.sleep(0.1)         
                s.connect((HOST, PORT))

                file = open(f"{path}Trajectories/{row}/{nm[i]}.txt", "rb")
                s.send(row.encode())
                time.sleep(0.01) 
                s.send(nm[i].encode())
                time.sleep(0.01) 

                data = file.read(1024)
                while data:
                    s.send(data)
                    data = file.read(1024)

                file.close()
                s.close

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        time.sleep(0.1)         
        s.connect((HOST, PORT))
        data = b"END"
        s.send(data)



if __name__ == '__main__':
    rospy.init_node('trajectory_executor')

    time.sleep(1)
    print('\n\nWaiting for files with trajectory data')
    print('\nConnection...\n')
    #data_receiver()

    time.sleep(1)
    print('\n\nWaiting for external input from LabView to start the tests')
    print('\nConnection...\n')
    #test_manager()

    time.sleep(1)
    input("Press enter when the receiver on the other PC is ready")
    data_sender()



    
            


