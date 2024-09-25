#!/usr/bin/env python
# coding=utf-8

import matplotlib.pyplot as plt
import os
import time


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


def plotter(path_name, t, q, q_p, q_pp, q_ppp, tau, tau_p):
    N, giunti = q.shape

    # Creating plots --------------------------------
    jnt = []
    for j in range(giunti):
        jnt.append('g' + str(j))

    if not q == []:
        for i in range(giunti):
            plt.plot(t, q[:, i], label=jnt[i])

        plt.xlabel("t [s]")
        plt.ylabel("q [rad]")
        plt.title("Positione")
        plt.legend()
        plt.savefig(path_name + '/Positions.png', format='png')
        time.sleep(0.05)
        plt.clf()  
    
    if not q_p == []:
        for i in range(giunti):
            plt.plot(t, q_p[:, i], label=jnt[i])

        plt.xlabel("t [s]")
        plt.ylabel("q_p [rad/s]")
        plt.title("Velocita\'")
        plt.legend()
        plt.savefig(path_name + '/Velocities.png', format='png')
        time.sleep(0.05)
        plt.clf()

    if not q_pp == []:
        for i in range(giunti):
            plt.plot(t, q_pp[:, i], label=jnt[i])

        plt.xlabel("t [s]")
        plt.ylabel("q_pp [rad/s^2]")
        plt.title("Accelerazione")
        plt.legend()
        plt.savefig(path_name + '/Accelerations.png', format='png')
        time.sleep(0.05)
        plt.clf()

    if not q_ppp == []:
        for i in range(giunti):
            plt.plot(t, q_ppp[:, i], label=jnt[i])

        plt.xlabel("t [s]")
        plt.ylabel("q_ppp [rad/s^3]")
        plt.title("Jerk")
        plt.legend()
        plt.savefig(path_name + '/Jerk.png', format='png')
        time.sleep(0.05)
        plt.clf()

    if not tau == []:
        for i in range(giunti):
            plt.plot(t, tau[:, i], label=jnt[i])

        plt.xlabel("t [s]")
        plt.ylabel("tau [Nm]")
        plt.title("Coppia")
        plt.legend()
        plt.savefig(path_name + '/Effort.png', format='png')
        time.sleep(0.05)
        plt.clf() 

    if not tau_p == []:
        for i in range(giunti):
            plt.plot(t, tau_p[:, i], label=jnt[i])

        plt.xlabel("t [s]")
        plt.ylabel("tau_p [Nm/s]")
        plt.title("Derivata della coppia")
        plt.legend()
        plt.savefig(path_name + '/Effort derivative.png', format='png')
        time.sleep(0.05)
        plt.clf() 

