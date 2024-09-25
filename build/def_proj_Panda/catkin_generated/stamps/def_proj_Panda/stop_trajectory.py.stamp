#!/usr/bin/env python
# coding=utf-8

"""
Funziona per il movimento di tutti i giunti su 2 punti utilizzando
'/position_joint_trajectory_controller/follow_joint_trajectory/goal' 
implementando una trajpoly5 in avanti e indietro con la possibilità di ricominciare.
Possibilità di utilizzare più eventi di stop consecutivi lungo la traiettoria originale.
Ogni traiettoria viene verificata.
La traiettoria di stop viene calcolata utilizzando il tempo ottimale
ed implementata come una trajpoly5 (con la posizione predetta, velocità
e accelerazioni pari a zero).
Il tempo ottimale viene calcolato con l'ottimizzatore a cicli for con tutti i vincoli
utilizzando  posizioni, velocità e accelerazioni predetti.
Serve una cartella 'stop_trajectory' con dentro il file 'traj.txt''
"""

import rospy
import moveit_commander
from copy import deepcopy
import numpy as np
import time
from control_msgs.msg import FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryActionResult
from sensor_msgs.msg import JointState
from def_proj.srv import *
import math
import os

# Settings
tester_name = 'unknown_tester'   # Insert tester name from terminal to create a directory
stamp = False   # True if you want to save datas into .txt files
reverse = False   # True if you want to have a reverse trajectory in your loop
n_loops = 1   # Number of loops to perform until ask for new start

# Parameters
traj_step = 0.01   # s
time_iter = 0.05   # s
toll_no_stop = 0.05   # rad
q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])    # rad/s
q_pp_lim = np.array([15, 7.5, 10, 12.5, 15, 20, 20])                            # rad/s^2

# Initialize empty lists
q_exp = []
q_p_exp = []
t_stop_exp = []
t_exp_q = []
t_exp_s = []

t_i = None
fl_q = None 
fl_q_p = None
fl_q_stop = None



def CallbackFollowJointTrajectoryResult(data, arg):

    arg.append(data.status.status)



def CallbackJointStates(data, arg):
    global fl_q, fl_q_p

    t = rospy.get_time()
    t_exp_q = t - t_i
 
    q_exp = data.position
    q_p_exp = data.velocity
        
    # ******************* FILES WRITING *******************

    if(stamp):
        # Write files
        fl_q.write('{0:14f} {1:14f} {2:14f} {3:14f} {4:14f} {5:14f} {6:14f} {7:14f}'.format(q_exp[0], q_exp[1], q_exp[2], q_exp[3], q_exp[4], q_exp[5], q_exp[6], t_exp_q) + '\n')
        fl_q_p.write('{0:14f} {1:14f} {2:14f} {3:14f} {4:14f} {5:14f} {6:14f} {7:14f}'.format(q_p_exp[0], q_p_exp[1], q_p_exp[2], q_p_exp[3], q_p_exp[4], q_p_exp[5], q_p_exp[6], t_exp_q) + '\n')
        
    # *****************************************************
 


def CalcValidTrajClient(q_s, q_e, traj_duration, traj_step):
    rospy.wait_for_service('calc_valid_traj')
    try:
        CalcValidTrajFunction = rospy.ServiceProxy('calc_valid_traj', CalcValidTraj)
        resp1 = CalcValidTrajFunction(q_s, q_e, traj_duration, traj_step)
        return resp1.flag_valid
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)



def CalcStopDurationClient(q_cur, q_p_cur, q_pp_cur):
    rospy.wait_for_service('calc_stop_duration')
    try:
        CalcStopDurationFunction = rospy.ServiceProxy('calc_stop_duration', CalcStopDuration)
        resp1 = CalcStopDurationFunction(q_cur, q_p_cur, q_pp_cur)
        return resp1.stop_duration
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)



def FlagStopClient(T_stop, q, q_p, q_pp):
    rospy.wait_for_service('flag_stop')
    try:
        FlagStopFunction = rospy.ServiceProxy('flag_stop', FlagStop)
        resp1 = FlagStopFunction(T_stop, q, q_p, q_pp)
        return resp1.flag_stop
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)



def ReadStopTrajectory(test_number, q_tar_or, traj_durations):

    file = open('/home/panda/Desktop/demo/stop_trajectory/traj_test_' + test_number + '.txt','r')

    for line in file:
        v_s = line.split('\t')
        data = []
        for s in v_s:
            data.append(float(s))
        q_tar_or.append(data[0:-1])
        traj_durations.append(data[-1])
    
    file.close()

    

def TrajPoly5(qi, qi_p, qi_pp, qf, qf_p, qf_pp, traj_duration, time_step):

    coeff = np.zeros(6)

    coeff[0] = qi
    coeff[1] = qi_p
    coeff[2] = qi_pp / 2

    known_terms = np.array([qf - qi - qi_p * traj_duration - 0.5 * qi_pp * traj_duration**2, qf_p - qi_p - qi_pp * traj_duration, qf_pp - qi_pp])

    # Vandermonde matrix
    V = np.array([[traj_duration**3, traj_duration**4, traj_duration**5], [3 * traj_duration**2, 4 * traj_duration**3, 5 * traj_duration**4], [6 * traj_duration, 12 * traj_duration**2, 20 * traj_duration**3]])

    coeff_1 = np.linalg.solve(V, known_terms)

    coeff[3] = coeff_1[0]
    coeff[4] = coeff_1[1]
    coeff[5] = coeff_1[2]
    
    t = np.linspace(0, traj_duration, int(traj_duration / time_step + 1))

    # Position profile
    q = coeff[0] + coeff[1] * t + coeff[2] * t**2 + coeff[3] * t**3 + coeff[4] * t**4 + coeff[5] * t**5

    # Velocity profile
    q_p = coeff[1] + 2 * coeff[2] * t + 3 * coeff[3] * t**2 + 4 * coeff[4] * t**3 + 5 * coeff[5] * t**4

    # Acceleration profile
    q_pp = 2 * coeff[2] + 6 * coeff[3] * t + 12 * coeff[4] * t**2 + 20 * coeff[5] * t**3

    traj = np.vstack((q, q_p, q_pp))
    
    return traj



def ExecuteTrajectory(q_tar_or, traj_duration, control_publisher):
    global q_exp, q_p_exp, t_stop_exp, t_exp_q, t_exp_s, fl_t_stop

    # Usefull variables
    flag_continue = 1   # flag to indicate that the final position isn't reached
    i = 0               # index of trajectory to final position

    traj_duration_new = round(traj_duration / traj_step) * traj_step    # current trajectory duration [s]
    added_time = 0                                                      # added time to precedent trajectory duration [s]

    q_c = deepcopy(q_tar_or[0])     # start position of current trajectory
    q_end = deepcopy(q_tar_or[1])   # final position of current trajectory

    q_p_lim = np.array([ 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
    q_pp_lim = np.array([0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
  
    while(flag_continue):        
        # verify feasibility of original trajectory
        flag_valid_traj = CalcValidTrajClient(deepcopy(q_c), deepcopy(q_end), deepcopy(traj_duration_new), deepcopy(traj_step))

        if(not(flag_valid_traj)):
            sys.exit("\nTraiettoria non valida")
        else:
            print('\nTraiettoria valida')
        
        # Initialization q, q_p and q_pp
        num_points = int(traj_duration_new / traj_step) + 1

        q = np.zeros((num_points, 7))
        q_p = np.zeros((num_points, 7))
        q_pp = np.zeros((num_points, 7)) 
    
        # Calculate complete trajectory
        for joint_num in range(7):

            traj_comp = TrajPoly5(q_c[joint_num], 0, 0, q_end[joint_num], 0, 0, traj_duration_new, traj_step)
            
            q[:, joint_num] = deepcopy(np.transpose(traj_comp[0, :]))
            q_p[:, joint_num] = deepcopy(np.transpose(traj_comp[1, :]))
            q_pp[:, joint_num] = deepcopy(np.transpose(traj_comp[2, :]))

            # Find out speed and acceleration limits to calculate added_time
            if not max(abs(traj_comp[1, :])) == 0.0:
                q_p_lim[joint_num] = (max(abs(traj_comp[1, :])))  
            
            if not max(abs(traj_comp[2, :])) == 0.0:
                q_pp_lim[joint_num] = (max(abs(traj_comp[2, :]))) 
                    
        # Write header message
        msg = FollowJointTrajectoryActionGoal()

        msg.header.stamp = rospy.Duration(0)
        msg.header.frame_id = ''

        msg.goal.trajectory.header.stamp = rospy.Duration(0)
        msg.goal.trajectory.header.frame_id = ''
        msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']      
        
        # Write trajectory message
        point = JointTrajectoryPoint()
        point.positions = deepcopy(q_end)
        point.velocities = [0, 0, 0, 0, 0, 0, 0]
        point.accelerations = [0, 0, 0, 0, 0, 0, 0]
        point.effort = []
        point.time_from_start = rospy.Duration(traj_duration_new)
        msg.goal.trajectory.points.append(deepcopy(point))

        # Status of movement on the trajectory
        status = []

        # Initialization subscriber node for /position_joint_trajectory_controller/follow_joint_trajectory/result
        sub_follow_joint_trajectory_result = rospy.Subscriber('/position_joint_trajectory_controller/follow_joint_trajectory/result', FollowJointTrajectoryActionResult, CallbackFollowJointTrajectoryResult, (status))
       
        # Move to configuration
        control_publisher.publish(msg)
        pub_time = rospy.get_time()

        # Wait the end of the trajectory or an error or a stop event
        stop_flag = 0

        if(len(q_exp) > 0):
            no_stop = np.all(abs(q_end - q_exp[-1]) < toll_no_stop)
        else:
            no_stop = 0

        rate = rospy.Rate(1/time_iter)
            
        while(len(status) == 0 and (not(stop_flag) or no_stop)): 
            
            # Calculate optimal stop duration
            traj_duration_prec = rospy.get_time() - pub_time + time_iter
            traj_index = int(traj_duration_prec / traj_step)
            if(traj_index < len(q)):
                q_c = deepcopy(q[traj_index])
                q_p_c = deepcopy(q_p[traj_index])
                q_pp_c = deepcopy(q_pp[traj_index])
              
                stop_duration = CalcStopDurationClient(deepcopy(q_c), deepcopy(q_p_c), deepcopy(q_pp_c))               

                # ******************* FILES WRITING *******************

                t = rospy.get_time()
                t_exp_s = t - t_i

                if(stamp):                    
        
                    fl_t_stop.write('%.9f'%stop_duration + '\t' + '%.9f'%t_exp_s + '\n')

                # ***************************************************** 
            
            # Detect capsule collision
            if(FlagStopClient(stop_duration, q_c, q_p_c, q_pp_c)):
                stop_flag = 1
            
            if(len(q_exp) > 0):
                no_stop = np.all(abs(q_end - q_exp[-1]) < toll_no_stop)
            else:
                no_stop = 0
            
            #rate.sleep()

        # If there was a stop event
        if(len(q_exp) > 0):
            do_stop = np.any(abs(q_end - q_exp[-1]) > toll_no_stop)
        else:
            do_stop = 1

        if(stop_flag and do_stop):

            print('\nIngaggio traiettoria di stop')

            # Write header message
            msg = FollowJointTrajectoryActionGoal()

            msg.header.stamp = rospy.Duration(0)
            msg.header.frame_id = ''

            msg.goal.trajectory.header.stamp = rospy.Duration(0)
            msg.goal.trajectory.header.frame_id = ''
            msg.goal.trajectory.joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']

            # Write trajectory message
            point = JointTrajectoryPoint()
            point.positions = deepcopy(q_c)
            point.velocities = [0, 0, 0, 0, 0, 0, 0]
            point.accelerations = [0, 0, 0, 0, 0, 0, 0]
            point.effort = []
            point.time_from_start = rospy.Duration(stop_duration)
            msg.goal.trajectory.points.append(deepcopy(point))

            # Move to stop configuration
            control_publisher.publish(msg)

            # Wait the end of the trajectory or an error
            while(status == [] or status == [2]):                
                FlagStopClient(stop_duration, q_c, q_p_c, q_pp_c)

                continue

            if(status[-1] == 3):
                print('Fine del movimento alla configurazione di stop')
            else:
                sys.exit('Errore nel movimento di tipo ' + str(status[-1]))
        else:
            # The final position is reached
            flag_continue = 0

            if(status[-1] == 3):
                print('Fine del movimento alla configurazione finale')
            else:
                sys.exit('Errore nel movimento di tipo ' + str(status[-1]))
        
        # Close subscribers
        sub_follow_joint_trajectory_result.unregister()
        
        # Update i
        i += 1

        # Update added_time 
        vect_t_vel = np.zeros((1, 7))
        np.divide(15 * (q_end - q_c), 8 * q_p_lim, vect_t_vel)
        t_vel = np.amax(abs(vect_t_vel))
   
        vect_t_acc = np.zeros((1, 7))
        np.divide(10 * (q_end - q_c), math.sqrt(3) * q_pp_lim, vect_t_acc)
        t_acc = np.amax(np.sqrt(abs(vect_t_acc)))
  
        a_time = max(t_vel, t_acc)

        if(a_time < 0.5):
            a_time = 0.5
        added_time = a_time
      
        # Update traj_duration
        traj_duration_new = round((added_time) / traj_step) * traj_step



def ExecuteTask(q_tar_or, traj_durations):
    global fl_q, fl_q_p, fl_t_stop, t_i, n_loops, stamp, tester_name, q_exp, q_p_exp, t_stop_exp, t_exp_q, t_exp_s 

    # Initialization node
    rospy.init_node('execute_trajectory')

    # Initialization publisher node for /position_joint_trajectory_controller/follow_joint_trajectory/goal
    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)

    # Needed to wait for the end of the node publication (publication isn't snapshot)
    time.sleep(0.5)

    flag_cont = 1
    while(flag_cont):
        q_exp = []
        q_p_exp = []
        t_stop_exp = []
        t_exp_q = []
        t_exp_s = []

        # ******************* FILES WRITING *******************

        if(stamp):
            sub_path_name = '/home/panda/Desktop/' + tester_name + '/test_' + test_number + '/stop_trajectory_static'

            # Open files
            fl_q = open(sub_path_name + '/q.txt', 'w')
            fl_q_p = open(sub_path_name + '/q_p.txt', 'w')
            fl_t_stop = open(sub_path_name + '/t_stop.txt', 'w')
            fl_t_tot = open(sub_path_name + '/t_tot.txt', 'w')
        
        # ***************************************************** 

        # Initialization subscriber node for /joint_states
        sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates, (q_exp, q_p_exp, t_exp_q))

        # Needed to wait for tCallback start
        time.sleep(0.011)

        t_i = rospy.get_time()

        for e in range(n_loops):

            # Move in the forward direction
            for i in range(len(traj_durations) - 1):
                q_tar_or_pair = []
                q_tar_or_pair.append(deepcopy(q_tar_or[i]))
                q_tar_or_pair.append(deepcopy(q_tar_or[i + 1]))
                ExecuteTrajectory(deepcopy(q_tar_or_pair), traj_durations[i + 1], control_publisher)

            if reverse:

                # Create reverse trajectory
                q_tar_or_rev = []
                traj_durations_rev = []
                for i in range(1,len(traj_durations) + 1):
                    q_tar_or_rev.append(deepcopy(q_tar_or[-i]))
                    traj_durations_rev.append(deepcopy(traj_durations[-i]))

                # Move in the backward direction
                for i in range(len(traj_durations_rev) - 1):
                    q_tar_or_pair = []
                    q_tar_or_pair.append(deepcopy(q_tar_or_rev[i]))
                    q_tar_or_pair.append(deepcopy(q_tar_or_rev[i + 1]))
                    ExecuteTrajectory(deepcopy(q_tar_or_pair), traj_durations_rev[i], control_publisher)

        # ******************* FILES WRITING *******************

        t_f = rospy.get_time()
        t_tot_exp = t_f - t_i

        if(stamp):
            
            fl_t_tot.write('%.9f'%t_tot_exp + '\n')

            # Close files
            fl_q.close()
            fl_q_p.close()
            fl_t_stop.close()
            fl_t_tot.close()

        # *****************************************************    

        # Close subscribers
        sub_joint_states.unregister()

        if(raw_input("\nInserire 'y' se si vuole uscire, altrimenti un qualsiasi altro input:\n") == 'y'):
            flag_cont = 0
              


if __name__ == '__main__':

    file = open('/home/panda/Desktop/demo/test_data.txt', 'r')

    test_data = []

    for line in file:
        test_data.append(line.split('\n'))

    tester_name = test_data[0][0]
    test_number = test_data[1][0]
    print(tester_name)
    print(test_number)
    
    # Read stop trajectory from files
    q_tar_or = []
    traj_durations = []
    ReadStopTrajectory(test_number, q_tar_or, traj_durations)

    # Initialization moveit
    move_group = moveit_commander.MoveGroupCommander("panda_arm")

    print('\n**************************************************\n')

    # Print configuration
    print('I giunti sono nella configurazione:')
    print(move_group.get_current_joint_values())

    # Move to start configuration
    print('\nMovimento alla configurazione iniziale\n')
    move_group.go(q_tar_or[0], wait=True)
    
    # Print configuration
    print('I giunti sono nella configurazione:')
    print(move_group.get_current_joint_values())

    raw_input('\nPremere invio per avviare il task')

    ExecuteTask(deepcopy(np.array(q_tar_or)), deepcopy(np.array(traj_durations)))

    # Move to start configuration
    print('\nMovimento alla configurazione iniziale\n')
    move_group.go(q_tar_or[0], wait=True)
    
    # Print configuration
    print('I giunti sono nella configurazione:')
    print(move_group.get_current_joint_values())
    
    print('\n**************************************************\n')

