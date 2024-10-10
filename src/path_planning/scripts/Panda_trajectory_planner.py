#! /usr/bin/env python3

import sys
import rospy
from math import pi
from itertools import repeat
import numpy as np
import csv
import time 
from copy import deepcopy
import os

from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryActionGoal


def reader(path_name, name, arg):
    t = []
    q = []
    q_p = []
    q_pp = []
    q_ppp = []
    tau = []
    tau_p = []

    # Open files -------------------------------
    if os.path.exists(path_name + '/t' + arg + '.txt'):
        fl_t = open(path_name + '/t' + arg + '.txt', 'r')

        for line in fl_t:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            t.append(data)

        fl_t.close()

    if os.path.exists(path_name + '/' + name + arg + '.txt'):
        fl_q = open(path_name + '/' + name + arg + '.txt', 'r')

        for line in fl_q:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            q.append(data)

        fl_q.close()

    if os.path.exists(path_name + '/' + name + '_p' + arg + '.txt'):
        fl_q_p = open(path_name + '/' + name + '_p' + arg + '.txt', 'r')

        for line in fl_q_p:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            q_p.append(data)

        fl_q_p.close()

    if os.path.exists(path_name + '/' + name + '_pp' + arg + '.txt'):
        fl_q_pp = open(path_name + '/' + name + '_pp' + arg + '.txt', 'r')

        for line in fl_q_pp:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            q_pp.append(data)

        fl_q_pp.close()

    if os.path.exists(path_name + '/' + name + '_ppp' + arg + '.txt'):
        fl_q_ppp = open(path_name + '/' + name + '_ppp' + arg + '.txt', 'r')

        for line in fl_q_ppp:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            q_ppp.append(data)

        fl_q_ppp.close()

    if os.path.exists(path_name + '/tau' + arg + '.txt'):
        fl_tau = open(path_name + '/tau' + arg + '.txt', 'r')

        for line in fl_tau:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            tau.append(data)

        fl_tau.close()

    if os.path.exists(path_name + '/tau_p' + arg + '.txt'):
        fl_tau_p = open(path_name + '/tau_p' + arg + '.txt', 'r')

        for line in fl_tau:
            v_s = line.split('\t')
            data = []

            for s in v_s:
                data.append(float(s))

            tau_p.append(data)

        fl_tau_p.close()

    return t, q, q_p, q_pp, q_ppp, tau, tau_p


def writer(path_name, t, q, q_p, q_pp, q_ppp, tau, tau_p, name, arg):
    # Open files -------------------------------
    if not t == []:
        fl_t = open(path_name + '/t' + arg + '.txt', 'w')

        for line in t:
            fl_t.write(str(line[0]) + '\n')

        fl_t.close()

    if not q == []:
        fl_q = open(path_name + '/' + name + arg + '.txt', 'w')

        for line in q:
            for i in range(len(line)-1):
                fl_q.write(str(line[i]) + '\t')
            
            fl_q.write(str(line[len(line)-1]) + '\n')

        fl_q.close()

    if not q_p == []:
        fl_q_p = open(path_name + '/' + name + '_p' + arg + '.txt', 'w')

        for line in q_p:
            for i in range(len(line)-1):
                fl_q_p.write(str(line[i]) + '\t')
            
            fl_q_p.write(str(line[len(line)-1]) + '\n')

        fl_q_p.close()

    if not q_pp == []:
        fl_q_pp = open(path_name + '/' + name + '_pp' + arg + '.txt', 'w')

        for line in q_pp:
            for i in range(len(line)-1):
                fl_q_pp.write(str(line[i]) + '\t')
            
            fl_q_pp.write(str(line[len(line)-1]) + '\n')

        fl_q_pp.close()

    if not q_ppp == []:
        fl_q_ppp = open(path_name + '/' + name + '_ppp' + arg + '.txt', 'w')

        for line in q_ppp:
            for i in range(len(line)-1):
                fl_q_ppp.write(str(line[i]) + '\t')
            
            fl_q_ppp.write(str(line[len(line)-1]) + '\n')

        fl_q_ppp.close()

    if not tau == []:
        fl_tau = open(path_name + '/tau' + arg + '.txt', 'w')

        for line in tau:
            for i in range(len(line)-1):
                fl_tau.write(str(line[i]) + '\t')
            
            fl_tau.write(str(line[len(line)-1]) + '\n')

        fl_tau.close()

    if not tau_p == []:
        fl_tau_p = open(path_name + '/tau_p' + arg + '.txt', 'w')

        for line in tau_p:
            for i in range(len(line)-1):
                fl_tau_p.write(str(line[i]) + '\t')
            
            fl_tau_p.write(str(line[len(line)-1]) + '\n')

        fl_tau_p.close()


def execute_trajectory(control_publisher, times, positions, velocities, accelerations, efforts):
    joint_names = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint", "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]

    msg = FollowJointTrajectoryActionGoal()
     
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
    #(positions, velocities, accelerations, efforts, times) = define_trajectory()
    (t, q, q_p, q_pp, q_ppp, tau, tau_p) = reader()
    
    times = np.array(times)
    
    # execute trajectory
    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)

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
