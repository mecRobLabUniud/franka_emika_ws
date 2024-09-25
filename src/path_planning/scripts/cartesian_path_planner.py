#!/usr/bin/env python
# coding=utf-8

import rospy
import moveit_commander
from moveit_msgs.msg import ExecuteTrajectoryActionGoal
from trajectory_msgs.msg import MultiDOFJointTrajectoryPoint
from geometry_msgs.msg import Transform, Twist, PoseStamped
from copy import deepcopy
import time
from tf.transformations import quaternion_from_euler
import math


def file_reader():
    t = []
    p = []
    p_p = []
    p_pp = []
    p_ppp = []
    
    # Read q matrix -------------------------------
    path_name = '/home/panda/Desktop/DATA'

    fl_t = open(path_name + '/t.txt','r')
    fl_p = open(path_name + '/p.txt','r')
    fl_p_p = open(path_name + '/p_p.txt','r')
    fl_p_pp = open(path_name + '/p_pp.txt','r')
    fl_p_ppp = open(path_name + '/p_ppp.txt','r')

    for line in fl_t:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        t.append(data)

    for line in fl_p:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        p.append(data)

    for line in fl_p_p:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        p_p.append(data)

    for line in fl_p_pp:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        p_pp.append(data)

    for line in fl_p_ppp:
        v_s = line.split('\t')
        data = []

        for s in v_s:
            data.append(float(s))

        p_ppp.append(data)

    fl_t.close()
    fl_p.close()
    fl_p_p.close()
    fl_p_pp.close() 
    fl_p_ppp.close()

    return t, p, p_p, p_pp, p_ppp



if __name__ == '__main__':

    rospy.init_node('execute_trajectory') 

    t, p, p_p, p_pp, p_ppp = file_reader()

    q = quaternion_from_euler(0, 0, math.pi/4)
    print(q)
    initial_pose = PoseStamped()

    initial_pose.header.stamp = rospy.Time(0)
    initial_pose.header.frame_id = 'panda_link0'

    initial_pose.pose.position.x = 0.30702#p[0][0]
    initial_pose.pose.position.y = 0#p[0][1]
    initial_pose.pose.position.z = 0.59027#p[0][2]
    initial_pose.pose.orientation.x = q[0]
    initial_pose.pose.orientation.y = q[1]
    initial_pose.pose.orientation.z = q[2]
    initial_pose.pose.orientation.w = q[3]
    
    # Initialization publication node
    control_publisher = rospy.Publisher('/execute_trajectory/goal', ExecuteTrajectoryActionGoal, queue_size=10)
    
    # Move to start configuration
    move_group = moveit_commander.MoveGroupCommander("panda_arm")
    move_group.set_pose_target(initial_pose)
    move_group.go(wait=True)
        
    # Creation of trajectory message --------------
    msg = ExecuteTrajectoryActionGoal()
    
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = ''
    msg.goal.trajectory.multi_dof_joint_trajectory.header.stamp = rospy.Time(0)
    msg.goal.trajectory.multi_dof_joint_trajectory.header.frame_id = 'panda_link0'
    msg.goal.trajectory.multi_dof_joint_trajectory.joint_names = ['panda_joint1','panda_joint2','panda_joint3','panda_joint4','panda_joint5','panda_joint6','panda_joint7']

    for i in range(0, len(t)):
        points = MultiDOFJointTrajectoryPoint()
        transforms = Transform()
        velocities = Twist()
        accelerations = Twist()
        
        transforms.translation.x = p[i][0]
        transforms.translation.y = p[i][1]
        transforms.translation.z = p[i][2]      
        transforms.rotation.x = q[0]
        transforms.rotation.y = q[1]
        transforms.rotation.z = q[2]
        transforms.rotation.w = q[3]
        
        points.transforms.append(deepcopy(transforms))
        
        velocities.linear.x = p_p[i][0]
        velocities.linear.y = p_p[i][1]
        velocities.linear.z = p_p[i][2]

        points.velocities.append(deepcopy(velocities))

        accelerations.linear.x = p_pp[i][0]
        accelerations.linear.y = p_pp[i][1]
        accelerations.linear.z = p_pp[i][2]

        points.accelerations.append(deepcopy(accelerations))
        
        points.time_from_start = rospy.Duration(t[i][0])
        
        msg.goal.trajectory.multi_dof_joint_trajectory.points.append(deepcopy(points))
        
    raw_input('\nPremere invio per avviare il task')

    # Move to configuration
    control_publisher.publish(msg)

    time.sleep(1)

    # ---------------------------------------------


    


