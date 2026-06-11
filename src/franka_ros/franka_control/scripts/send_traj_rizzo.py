#!/usr/bin/env python
# coding=utf-8

import rospy
#import moveit_commander
from copy import deepcopy
import numpy as np
import time
from control_msgs.msg import FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from franka_msgs.msg import FrankaState
#from franka_gripper.msg import MoveActionGoal
import math
import csv
import re

### INSTRUCTIONS ###
# 1) Remove gripper if torque measurements must correspond with matlab model.
#
# 2) Make sure to set publish rate and cutoff frequency to 1000Hz in folder:
# ~/catkin_panda/src/franka_ros/franka_control/config
# (These values can be checked in the logs of roslaunch franka_control)
#
# 2) Open terminal and source the bash file of the franka_ros workspace with:
# source ~/catkin_panda/devel/setup.bash
#
# 3) Start the franka_control package with:
# roslaunch franka_control franka_control.launch robot_ip:=172.16.0.2 load_gripper:=false
#
# 4) Open second terminal and start movit planner with:
# roslaunch panda_moveit_config panda_moveit.launch controller:=position load_gripper:=false
#
# 5) Open terminal in folder of this file and source the bash file of the franka_ros workspace with:
# source ~/catkin_panda/devel/setup.bash
#
# 6) Change input .csv file at line 49 to the desired 'setpoints_<profilename>.csv'
#
# 7) Run python program with command:
# python franka_moveCSV_measureTorque.py
#
# 8) After execution the results cn be found in 'measurements_<profilename>.csv'


def ExecuteTask():

    ### DEFINE CSV PATHS ###
    # path to setpoint csv file (input)
    traj_n = '10'
    csv_file_path_in = '/media/panda/6EF5-26AF/Traiettorie/traj' + traj_n + '/traj' + traj_n + '.csv'
    # path to measurement csv file (output)
    csv_file_path_out = '/media/panda/6EF5-26AF/Traiettorie/traj' + traj_n + '/measurements_traj' + traj_n + '.csv'
    
    ### END DEFINE CSV PATHS ###

    #### READ DATA ###
    # create an empty list to store the rows
    data = []

    # open the csv file
    with open(csv_file_path_in, "r") as csv_file:
        # create csv reader object
        csv_reader = csv.reader(csv_file, delimiter=',')

        # skip the first row with headers
        # next(csv_reader)

        # loop through each row in the csv file
        for row in csv_reader:
            # convert each element to a float and add the row to the list
            data.append([float(i) for i in row])
    ### END READ DATA ###

    ### INIT ROS ###
    # Initialization node
    rospy.init_node('execute_trajectory')

    # Initialization publisher node for /position_joint_trajectory_controller/follow_joint_trajectory/goal
    publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 0)

    # Needed to wait for the end of the node publication (publication isn't snapshot)
    time.sleep(0.5)
    ### END INIT ROS ###

    ### MOVE TO START ###
    # Write header message
    msg = FollowJointTrajectoryActionGoal()

    msg.header.stamp = rospy.Duration(0)
    msg.header.frame_id = ''

    msg.goal.trajectory.header.stamp = rospy.Duration(0)
    msg.goal.trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']      
    
    # Write trajectory message to start point
    point = JointTrajectoryPoint()
    point.positions = data[0][1:7+1]
    point.velocities = [0, 0, 0, 0, 0, 0, 0]
    point.accelerations = [0, 0, 0, 0, 0, 0, 0]
    point.effort = []
    point.time_from_start = rospy.Duration(5.0)
    msg.goal.trajectory.points.append(deepcopy(point))

    # wait for message to be constructed
    time.sleep(0.5)

    # ask for confirmation with enter
    raw_input('\nPress "Enter" to go to start position')
    
    # move to configuration
    publisher.publish(msg)

    # wait for motion to execute
    time.sleep(5)
    ### END MOVE TO START ###

    ### EXECUTE MOTION ###
    # Write header message
    msg = FollowJointTrajectoryActionGoal()

    msg.header.stamp = rospy.Duration(0)
    msg.header.frame_id = ''

    msg.goal.trajectory.header.stamp = rospy.Duration(0)
    msg.goal.trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']      
    
    for row in data:
        # Write trajectory message
        point = JointTrajectoryPoint()
        point.positions = row[1:7+1]
        point.velocities = row[8:14+1]
        point.accelerations = row[15:21+1]
        point.effort = []
        point.time_from_start = rospy.Duration(row[0])
        msg.goal.trajectory.points.append(deepcopy(point))

    # wait for message to be constructed
    time.sleep(0.5)

    # ask for confirmation with enter
    raw_input('\nPress "Enter" to execute motion')
    
    # move to configuration
    publisher.publish(msg)
    ### END EXECUTE MOTION ###

    ### MEASURE DATA ###
    # Create an empty array to store the measurements
    measurements = []

    # Read first message
    #state = rospy.wait_for_message('/joint_states', JointState)
    state = rospy.wait_for_message('/franka_state_controller/joint_states', JointState)
    #state = rospy.wait_for_message('/franka_state_controller/franka_states', FrankaState)

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


if __name__ == '__main__':

    ExecuteTask()
   