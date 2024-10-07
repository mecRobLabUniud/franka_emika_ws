#! /usr/bin/env python3

import sys
import rospy
from math import pi
from itertools import repeat
import numpy as np
import csv
import time 
from copy import deepcopy
import rtde_receive

from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryActionGoal


def define_trajectory():

    # load times
    csv_time = open('traj_data/time.csv')
    csv_reader = csv.reader(csv_time)
    times = []
    for row in csv_reader:
        time = float(row[0])
        times.append(time)

    # load positions
    csv_pos = open('traj_data/pos.csv')
    csv_reader = csv.reader(csv_pos)
    positions = []
    for row in csv_reader:
        positions_float = [float(item) for item in row]
        positions.append(positions_float)   

    # load velocites
    csv_vel = open('traj_data/vel.csv')
    csv_reader = csv.reader(csv_vel)
    velocities = []
    for row in csv_reader:
        velocities_float = [float(item) for item in row]
        velocities.append(velocities_float)

    # load accelerations
    csv_acc = open('traj_data/acc.csv')
    csv_reader = csv.reader(csv_acc)
    accelerations = []
    for row in csv_reader:
        accelerations_float = [float(item) for item in row]
        accelerations.append(accelerations_float)

    # torques are undefined
    efforts = list(repeat([],len(positions)))

    return positions, velocities, accelerations, efforts, times


def execute_trajectory(control_publisher, times, positions, velocities, accelerations, efforts):
    joint_names = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]

    msg = ExecuteTrajectoryActionGoal()
     
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = ''
    msg.goal.trajectory.header.stamp = rospy.Time(0)
    msg.goal.trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_names = joint_names

    for i in range(len(times)):
        point = JointTrajectoryPoint()
        point.positions = positions[i]
        point.velocities = velocities[i]
        point.accelerations = accelerations[i]
        #point.effort = efforts[i]
        point.time_from_start = rospy.Duration(times[i])
        msg.goal.trajectory.points.append(deepcopy(point))

    control_publisher.publish(msg)


if __name__ == '__main__':
    rospy.init_node('ur5', anonymous=True)

    # move to default home
    folded_home = [0.18016493320465088, -1.6301008663573207, -1.7113336324691772, -1.173974559908249, 1.2832341194152832, -1.969231430684225]
    
    # define trajectory
    (positions, velocities, accelerations, efforts, times) = define_trajectory()
    
    times = np.array(times)
    
    # execute trajectory
    control_publisher = rospy.Publisher('/scaled_pos_joint_traj_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size=10)

    rtde_r = rtde_receive.RTDEReceiveInterface("172.16.0.2")

    q_r = rtde_r.getTargetQ()

    input('\nPremere invio per avviare il task')
    execute_trajectory(control_publisher, [0, 3], [q_r, positions[0]], [np.array([0, 0, 0, 0, 0, 0]),np.array([0, 0, 0, 0, 0, 0])], [np.array([0, 0, 0, 0, 0, 0]),np.array([0, 0, 0, 0, 0, 0])], [])
    time.sleep(3)

    time.sleep(0.4)
    input('\nPremere invio per avviare il task')
    execute_trajectory(control_publisher, times, positions, velocities, accelerations, efforts)

    out = open('/home/panda/Desktop/joint_states.txt', 'w')
    
    t0 = time.time()
    t_final = times[-1]

    while time.time()-t0 < t_final:
        # time
        t = rtde_r.getTimestamp()
        times = [0]
        times[0] = t
        # target data
        joint_target_position = rtde_r.getTargetQ()
        joint_target_velocity = rtde_r.getTargetQd()
        joint_target_acceleration = rtde_r.getTargetQdd()
        joint_target_current = rtde_r.getTargetCurrent()
        joint_target_moment = rtde_r.getTargetMoment()
        # joint data
        joint_position = rtde_r.getActualQ()
        joint_velocity = rtde_r.getActualQd()
        joint_current = rtde_r.getActualCurrent()
        joint_voltage = rtde_r.getActualJointVoltage()
        joint_control_current = rtde_r.getJointControlOutput()
        joint_temperature = rtde_r.getJointTemperatures()
        # tool center point (TCP) data
        tcp_position = rtde_r.getActualTCPPose()
        tcp_speed = rtde_r.getActualTCPSpeed()
        tcp_acceleration = rtde_r.getActualToolAccelerometer()
        tcp_force = rtde_r.getActualTCPForce()

        data_list = (times + joint_position + joint_velocity + joint_current + joint_voltage + joint_control_current + joint_temperature + tcp_position + tcp_speed
            + tcp_acceleration + tcp_force + joint_target_position + joint_target_velocity + joint_target_acceleration + joint_target_current + joint_target_moment)

        for item in data_list:
            out.write("%s " % item)
        out.write('\n')
        time.sleep(1/500)

    #time.sleep(times[-1])

    # move to starting point again, then home
    #group = move_to_position(positions[0])
    #group = move_to_position(folded_home)
