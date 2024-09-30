#!/usr/bin/env python3
# coding=utf-8

import rospy
from control_msgs.msg import FollowJointTrajectoryActionGoal
from moveit_msgs.msg import ExecuteTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from copy import deepcopy
import time
import numpy as np
from write_read_plot import reader, writer
import socket
#from trajectory_validator import validator as trj_validator
#from self_collisions_validator import validator as scol_validator


# per bloccare processo:
# kill -9 $(lsof -ti tcp:139)

q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])    # rad/s


def CallbackJointStates(data):
    global fl_t, fl_q, fl_q_p, fl_tau, t_exp, q_exp, q_p_exp, tau_exp

    t = rospy.get_time()

    t_exp.append([t - t_i])  
    q_exp.append(data.position[0:7])
    q_p_exp.append(data.velocity)
    tau_exp.append(data.effort)



if __name__ == '__main__':
    rospy.init_node('TCP_executor')


    HOST = "172.16.1.1"  # Standard loopback interface address (localhost)
    PORT = 139  # Port to listen on (non-privileged ports are > 1023)

    #TCP input
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        print('Connessione...')
        
        try:
            while True:            
                conn, addr = s.accept()
                
                with conn:
                    print(f"Connesso con {addr}")

                    data = conn.recv(1024)
                    if data == b'Stop':
                        conn.close()
                        print('Disconnesso')
                        s.close()

                        time.sleep(1)
                        
                        print('Fine esecuzione test')
                        break

                    print('Movimento alla configurazione iniziale')

                    # Reading data to files ------------------------
                    #path_name = f'/home/panda/Desktop/DATA_OTTIMIZZATORE/{data.decode()}'
                    path_name = f'/home/panda/Desktop/{data.decode()}'

                    t, q, q_p, q_pp, q_ppp, tau, tau_p = reader(path_name, 'q', '_test')

                    #print('Self collision check = ', scol_validator(q))     
                    #print('Kinematics and dynamics limits check = ', trj_validator(t, q, q_p, q_pp, q_ppp))
                    
                    t_i = rospy.get_time()
                    t_exp = []
                    q_exp = []
                    q_p_exp = []
                    tau_exp = []

                    # Initialization subscriber node for /joint_states
                    sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)
                    
                    # Initialization publisher node for /position_joint_trajectory_controller/follow_joint_trajectory/goal
                    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)
                    
                    # Move to start configuration
                    msg = FollowJointTrajectoryActionGoal()

                    msg.header.stamp = rospy.Duration(0)
                    msg.header.frame_id = ''
                    msg.goal.trajectory.header.stamp = rospy.Duration(0)
                    msg.goal.trajectory.header.frame_id = ''
                    msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']      

                    t_start = []     

                    time.sleep(0.4)

                    for i in range(len(q[0])):
                        d = abs(q_exp[-1][i]-q[0][i])
                        t_start.append(d/(0.15*q_p_lim[i])+1)

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
                    print(msg)
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
                        conn.send(b'1')
                        conn.close()

                        time.sleep(0.2)

                        print('Esecuzione traiettoria...')
                        
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
            s.close()
            


