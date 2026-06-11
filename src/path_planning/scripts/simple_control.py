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
from data_IO import reader, writer
import socket
#from trajectory_validator import validator as trj_validator
#from self_collisions_validator import validator as scol_validator


# per bloccare processo:
# kill -9 $(lsof -ti tcp:139)

q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])    # rad/s


def CallbackJointStates(data):
    global t_exp, q_exp, q_p_exp, tau_exp

    t = rospy.get_time()

    t_exp.append([t - t_i])  
    q_exp.append(data.position[0:7])
    q_p_exp.append(data.velocity)
    tau_exp.append(data.effort)

def CallbackDesiredJointStates(data):
    global t_des, q_des, q_p_des, tau_des

    t = rospy.get_time()

    t_des.append([t - t_i])  
    q_des.append(data.position[0:7])
    q_p_des.append(data.velocity)
    tau_des.append(data.effort)



if __name__ == '__main__':

    rospy.init_node('TCP_execute_trajectory')

    print('Movimento alla configurazione iniziale')

    # Reading data to files ------------------------
    path_name = f'/home/panda/Documents/temp'
    #path_name = f'/home/panda/Desktop/DATA_OTTIMIZZATORE/DATA_OTTIMIZZATORE-Histogram/SQUARE_TRAJ/'

    t, q, q_p, q_pp, q_ppp, tau, tau_p = reader(path_name, 'q', '')
    
    #print('Self collision check = ', scol_validator(q))     
    #print('Kinematics and dynamics limits check = ', trj_validator(t, q, q_p, q_pp, q_ppp))

    t_i = rospy.get_time()
    t_exp = []
    q_exp = []
    q_p_exp = []
    tau_exp = []
    t_des = []
    q_des = []
    q_p_des = []
    tau_des = []

    # Initialization subscriber node for /joint_states
    sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)
    sub_desired_joint_states = rospy.Subscriber('/joint_states_desired', JointState, CallbackDesiredJointStates)
    
    # Initialization publisher node for /position_joint_trajectory_controller/follow_joint_trajectory/goal
    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)
    
    # Move to start configuration
    msg = FollowJointTrajectoryActionGoal()

    msg.header.stamp = rospy.Duration(0)
    msg.header.frame_id = ''

    msg.goal.trajectory.header.stamp = rospy.Duration(0)
    msg.goal.trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']      

    time.sleep(0.1)

    t_start = []
    
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

    time.sleep(0.2)
    
    # Move to start configuration
    control_publisher.publish(msg)

    # Wait the end of the trajectory
    time.sleep(max(t_start))
        
    # Initialization publication node
    control_publisher = rospy.Publisher('/execute_trajectory/goal', ExecuteTrajectoryActionGoal, queue_size=10)

    # Creation of trajectory message --------------
    msg = ExecuteTrajectoryActionGoal()
    
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = ''
    msg.goal.trajectory.joint_trajectory.header.stamp = rospy.Time(0)
    msg.goal.trajectory.joint_trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_trajectory.joint_names =    ['panda_joint1','panda_joint2','panda_joint3','panda_joint4','panda_joint5','panda_joint6','panda_joint7']
    
    # Write trajectory message
    for i in range(len(t)):
        point = JointTrajectoryPoint()
        point.positions = q[i]
        point.velocities = q_p[i]
        point.accelerations = q_pp[i]
        point.effort = []#tau[i]
        point.time_from_start = rospy.Duration(t[i][0])
        msg.goal.trajectory.joint_trajectory.points.append(deepcopy(point))

    input('Press to execute trajectory')

    # Move to configuration
    control_publisher.publish(msg)
    
    t_i = rospy.get_time()
    t_exp = []
    q_exp = []
    q_p_exp = []
    tau_exp = []
    t_des = []
    q_des = []
    q_p_des = []
    tau_des = []

    time.sleep(t[-1][0])

    sub_joint_states.unregister()
    sub_desired_joint_states.unregister()

    t_exp = np.array(t_exp)
    q_exp = np.array(q_exp)
    q_p_exp = np.array(q_p_exp)
    tau_exp = np.array(tau_exp)
    t_des = np.array(t_des)
    q_des = np.array(q_des)
    q_p_des = np.array(q_p_des)
    tau_des = np.array(tau_des)
    
    writer('/home/panda/Documents/temp/', t_exp, q_exp, q_p_exp, [], [], tau_exp, [], 'q', '_BASE_exp')
    writer('/home/panda/Documents/temp/', t_des, q_des, q_p_des, [], [], tau_des, [], 'q', '_BASE_des')


            


