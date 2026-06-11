#!/usr/bin/env python3
# coding=utf-8

import rospy
from control_msgs.msg import FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from copy import deepcopy
import time
import numpy as np
import csv


element_delimiter = ','
# path to setpoint csv file (input)
csv_file_path_in = '/home/panda/Documents/trajFranka/setpoints_task4_fixPath[spline]_cheb[8].csv'
# path to measurement csv file (output)
csv_file_path_out = '/home/panda/Documents/trajFranka/meas_task4_fixPath[spline]_cheb[8].csv'



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
    #path_name = f'/home/panda/Documents/trajFranka'
    #path_name = f'/home/panda/Desktop/DATA_OTTIMIZZATORE/DATA_OTTIMIZZATORE-Histogram/SQUARE_TRAJ/'

    data = []

    with open(csv_file_path_in, "r") as csv_file:
        # create csv reader object
        csv_reader = csv.reader(csv_file, delimiter=element_delimiter)

        # skip the first row with headers
        # next(csv_reader)

        # loop through each row in the csv file
        for i, row in enumerate(csv_reader):
            # convert each element to a float and add the row to the list
            if i == 0: continue     # skip the header row
            data.append([float(i) for i in row])
    ### END READ DATA ###
    
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
    
    # Write trajectory message
    point = JointTrajectoryPoint()
    point.positions = data[0][1:7+1]
    point.velocities = [0, 0, 0, 0, 0, 0, 0]
    point.accelerations = [0, 0, 0, 0, 0, 0, 0]
    point.effort = []
    point.time_from_start = rospy.Duration(5)
    msg.goal.trajectory.points.append(deepcopy(point))

    time.sleep(0.4)
    
    # Move to start configuration
    control_publisher.publish(msg)

    # Wait the end of the trajectory
    time.sleep(2)

    # Creation of trajectory message --------------
    msg = FollowJointTrajectoryActionGoal()
    
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = ''
    msg.goal.trajectory.header.stamp = rospy.Time(0)
    msg.goal.trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_names = ['panda_joint1','panda_joint2','panda_joint3','panda_joint4','panda_joint5','panda_joint6','panda_joint7']
    
    # Write trajectory message
    for row in data:
        point = JointTrajectoryPoint()
        point.positions = row[1:7+1]
        point.velocities = row[8:14+1]
        point.accelerations = row[15:21+1]
        point.time_from_start = rospy.Duration(row[0])
        msg.goal.trajectory.points.append(deepcopy(point))

    input('Press to execute trajectory')

    time.sleep(0.4)

    # Execute trajectory
    control_publisher.publish(msg)

    # print("Total time = ", data[-1][0])
    # time.sleep(data[-1][0])

    ### MEASURE DATA ###
    # Create an empty array to store the measurements
    measurements = []

    # Read first message
    state = rospy.wait_for_message('/franka_state_controller/joint_states', JointState)

    # Notify that first message has arrived
    print('Measurement started.')

    # Initialize time
    time0 = state.header.stamp.to_sec()
    currTime = 0

    # Initialize positions
    currPos = list(state.position)
    targPos = data[-1][1:7+1]

    # Execute loop if target position is not reached
    #while max([abs(currPos[i]-targPos[i]) for i in range(len(currPos))]) > 0.001:
    while currTime < data[-1][0]:
    #while currTime < 10:

        # Save state data to a list
        currTime = state.header.stamp.to_sec()-time0
        currPos = list(state.position)
        currVel = list(state.velocity)
        currTau = list(state.effort)

        # Save state data to a list
        currMeas = [currTime]
        currMeas.extend(currPos)
        currMeas.extend(currVel)
        currMeas.extend(currTau)

        # Append list (row) to measurements
        measurements.append(currMeas)

        # wait for next ros message and update state
        state = rospy.wait_for_message('/franka_state_controller/joint_states', JointState)
        
    print('Measurement stopped.')
    ### END MEASURE DATA ###

    ### WRITE TO CSV ###
    # Create headers for CSV
    headers =['time [s]']
    for i in range(1,7+1):
        pos_string = 'position J' + str(i) + ' [rad]'
        headers.append(pos_string)
    for i in range(1,7+1):
        vel_string = 'velocity J' + str(i) + ' [rad/s]'
        headers.append(vel_string)
    for i in range(1,7+1):
        tau_string = 'torque J' + str(i) + ' [Nm]'
        headers.append(tau_string)

    # Open the file in write mode and create a CSV writer object
    with open(csv_file_path_out, mode='w') as file:
        writer = csv.writer(file)

        # Write the header row to the CSV file
        writer.writerow(headers)

        # Loop through each row of the list and write it to the CSV file
        for row in measurements:
            writer.writerow(row)
    ### END WRITE TO CSV ###
            


