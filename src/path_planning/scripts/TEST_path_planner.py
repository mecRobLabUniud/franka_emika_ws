#!/usr/bin/env python
# coding=utf-8

import rospy
import moveit_commander
from moveit_msgs.msg import ExecuteTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from copy import deepcopy
import time
import os
import numpy as np
from write_read_plot import reader, writer
#from trajectory_validator import validator as trj_validator
#from self_collisions_validator import validator as scol_validator



matlab = 0


def CallbackJointStates(data):
    global fl_t, fl_q, fl_q_p, fl_tau, t_exp, q_exp, q_p_exp, tau_exp

    t = rospy.get_time()

    t_exp.append([t - t_i])  
    q_exp.append(data.position[0:7])
    q_p_exp.append(data.velocity)
    tau_exp.append(data.effort)



if __name__ == '__main__':

    rospy.init_node('execute_trajectory')

    if matlab:
        path_name = '/media/panda/KINGSTON/traj_matlab'
    else:
        path_name = '/home/panda/Desktop/DATA_OTTIMIZZATORE/OPT_T/P1_1E+04_P2_1'

    t, q, q_p, q_pp, q_ppp, tau, tau_p = reader(path_name, 'q', '')
    
    #print('Self collision check = ', scol_validator(q))     
    #print('Kinematics and dynamics limits check = ', trj_validator(t, q, q_p, q_pp, q_ppp))
    
    # Initialization publication node
    control_publisher = rospy.Publisher('/execute_trajectory/goal', ExecuteTrajectoryActionGoal, queue_size=10)
    
    # Move to start configuration
    move_group = moveit_commander.MoveGroupCommander("panda_arm")
    move_group.go(q[0], wait=True)
    
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
        point.effort = []
        point.time_from_start = rospy.Duration(t[i][0])
        msg.goal.trajectory.joint_trajectory.points.append(deepcopy(point))
    
    t_i = rospy.get_time()
    t_exp = []
    q_exp = []
    q_p_exp = []
    tau_exp = []

    # Initialization subscriber node for /joint_states
    sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)

    # Saving datas to files ------------------------
    path_name = '/home/panda/Desktop/DATA/traj_' + str(round(t[-1][0], 1)) + 's'
    if not os.path.exists(path_name):
        os.makedirs(path_name)
    
    raw_input('\nPremere invio per avviare il task')
    
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
    
    writer(path_name, t_exp, q_exp, q_p_exp, [], [], tau_exp, [], 'q', '_exp_mat')


    


