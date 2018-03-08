import numpy as np
import probInfo
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.patches as patches
import matplotlib.animation as animation
import matplotlib.patches as patches
import problemData as pdata
import os
from utils import *

# Axis:
# *X, *Y = E [ft], N [ft], theta [rad] (theta is w.r.t +E axis)


def nmpcPlotSol(u_new,path,mpciter,x0,obstacle,case):

    u_mpciter = u_new.flatten(1)
    x_mpciter = probInfo.computeOpenloopSolution(u_mpciter, pdata.N, pdata.T, pdata.t0, x0)
    East = x_mpciter[:,0]
    North = x_mpciter[:,1]

    V_terminal = x_mpciter[-1,2]

    # figure 1
    plt.figure(1,figsize=(5, 7), dpi=100)

    plt.ylabel('N [ft]')
    plt.xlabel('E [ft]')
    #plt.axis('equal')

    if mpciter == 0:

        # Detailed Path
        plt.plot(path.pathData.E, path.pathData.N, linestyle='--', color='c')

        # Laplacian Path
        #plt.plot(path.pathData.pathLaplacian[0,:], path.pathData.pathLaplacian[1,:], linestyle='--', color='k')

        #plt.plot(path.pathData.PathLeftBoundaryE, path.pathData.PathLeftBoundaryN, linestyle='-', color='k')
        #plt.plot(path.pathData.PathRightBoundaryE, path.pathData.PathRightBoundaryN, linestyle='-', color='k')

        plt.plot(path.pathData.PathStartPoint[0], path.pathData.PathStartPoint[1], marker='o', markersize=8, color='r')
        plt.plot(path.pathData.PathEndPoint[0], path.pathData.PathEndPoint[1], marker='o', markersize=8, color='g')

        if True:
            plt.plot(path.pathData.PathRightEndPointsE, path.pathData.PathRightEndPointsN,'m+')
            plt.plot(path.pathData.PathLeftEndPointsE, path.pathData.PathLeftEndPointsN,'m+')

            x1 = path.pathData.PathRightEndPointsE
            x2 = path.pathData.PathLeftEndPointsE
            y1 = path.pathData.PathRightEndPointsN
            y2 = path.pathData.PathLeftEndPointsN
            plt.plot(x1, y1, 'm', x2, y2, 'm')

            x1 = path.pathData.PathCenterEndPointsE - pdata.delta_yRoad*np.sin(path.pathData.Theta_endpoints)
            x2 = path.pathData.PathCenterEndPointsE + pdata.delta_yRoad*np.sin(path.pathData.Theta_endpoints)
            y1 = path.pathData.PathCenterEndPointsN + pdata.delta_yRoad*np.cos(path.pathData.Theta_endpoints)
            y2 = path.pathData.PathCenterEndPointsN - pdata.delta_yRoad*np.cos(path.pathData.Theta_endpoints)
            plt.plot(x1, y1, 'r', x2, y2, 'r')

            #for i in range(len(path.pathData.LaneRightEndPointsX)):
            #    x1 = path.pathData.LaneRightEndPointsX[i]
            #    y1 = path.pathData.LaneRightEndPointsY[i]
            #    x2 = path.pathData.LaneLeftEndPointsX[i]
            #    y2 = path.pathData.LaneLeftEndPointsY[i]
            #    plt.plot([x1, x2], [y1, y2], 'm')

        plt.grid(True)

        if True: # obstacle.Present == True:

            nObs = len(obstacle.E)
            if nObs > 0:
                for k in range(nObs):

                    Efc = obstacle.E[k] + pdata.pathWidth/2
                    Nfc = obstacle.N[k]
                    W = obstacle.w[k] - pdata.pathWidth
                    L = obstacle.l[k]
                    Theta = obstacle.Chi[k]
                    fc = "red"
                    polygon_obstacle = getPatch(Efc, Nfc, W, L, Theta, fc)


                    Efc = obstacle.E[k]
                    Nfc = obstacle.N[k]
                    W = obstacle.w[k]
                    L = obstacle.l[k]
                    Theta = obstacle.Chi[k]
                    fc = "green"
                    polygon_safezone = getPatch(Efc, Nfc, W, L, Theta, fc)

                    ax = plt.gca()
                    ax.add_patch(polygon_safezone)
                    ax.add_patch(polygon_obstacle)

    nEN = len(East)
    plt.plot(East[0:nEN], North[0:nEN], marker='x', markersize=4, color='b')
    plt.plot(East[0], North[0], marker='o', markersize=4, color='r')
    plt.xlim([0, 16])
    plt.ylim([0, 128])

    #plt.draw()
    plt.pause(0.01)
    #if mpciter == mpciterations-1:
        #   ax1 = f1.gca()
        #   del ax1.lines[7:12]
        #dummy = raw_input('Press Enter to continue: ')

    return V_terminal


def nmpcPlot(t,x,u,path,obstacle,tElapsed,V_terminal,latAccel,dyError,settingsFile):

    f_pData = file(settingsFile, 'r')
    cols, indexToName = getColumns(f_pData, delim=" ", header=False)
    #N = np.array(cols[0]).astype(np.int)
    #T = np.array(cols[1]).astype(np.int)
    ns = np.array(cols[2]).astype(np.int)
    #no = np.array(cols[3]).astype(np.int)

    figno = np.zeros(8)
    figno[0] = 1

    # ncons_option is now hard-coded here since we want to create plot from
    # plotSavedData.py also.
    ncons_option = 2

    # useLatAccelCons is now hard-coded here since we want to create plot from
    # plotSavedData.py also.
    useLatAccelCons = 1

    if ns == 4:
        lb_VdotVal = np.array(cols[4]).astype(np.float)
        ub_VdotVal = np.array(cols[5]).astype(np.float)
        lb_ChidotVal = np.array(cols[6]).astype(np.float)
        ub_ChidotVal = np.array(cols[7]).astype(np.float)
        delta_yRoad = np.array(cols[8]).astype(np.float)
        lataccel_maxVal = np.array(cols[9]).astype(np.float)
        lb_V = np.array(cols[10]).astype(np.float)
        ub_V = np.array(cols[11]).astype(np.float)


    elif ns == 6:
        lb_VddotVal = np.array(cols[4]).astype(np.float)
        ub_VddotVal = np.array(cols[5]).astype(np.float)
        lb_ChiddotVal = np.array(cols[6]).astype(np.float)
        ub_ChiddotVal = np.array(cols[7]).astype(np.float)
        delta_yRoad = np.array(cols[8]).astype(np.float)
        lataccel_maxVal = np.array(cols[9]).astype(np.float)
        lb_V = np.array(cols[10]).astype(np.float)
        ub_V = np.array(cols[11]).astype(np.float)

    if ns == 4:

        # figure 2
        plt.figure(2)
        figno[1] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, x[:, [0]])  # E
        plt.ylabel('E [ft]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, x[:, [1]])  # N
        plt.ylabel('N [ft]')
        plt.xlabel('t [sec]')
        plt.grid(True)


        # figure 3
        plt.figure(3)
        figno[2] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, x[:, [2]])  # V
        plt.grid(True)

        #plt.plot(t, lb_V*np.ones(t.shape),linestyle='--', color='g')
        #plt.plot(t, ub_V*np.ones(t.shape), linestyle='--', color='g')

        plt.ylabel('V [fps]')

        plt.subplot(212)
        plt.plot(t, u[:, [0]])  # Vdot
        plt.plot(t, lb_VdotVal*np.ones(t.shape),linestyle='--', color='r')
        plt.plot(t, ub_VdotVal*np.ones(t.shape), linestyle='--', color='r')
        plt.grid(True)

        plt.ylabel('Vdot [fps2]')
        plt.xlabel('t [sec]')
        plt.grid(True)

        # figure 4
        plt.figure(4)
        figno[3] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, x[:, [3]]*180/np.pi)
        plt.ylabel('Chi [deg]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, u[:, [1]]*180/np.pi)
        plt.plot(t, lb_ChidotVal*np.ones(t.shape)*180/np.pi,linestyle='--', color='r')
        plt.plot(t, ub_ChidotVal*np.ones(t.shape)*180/np.pi, linestyle='--', color='r')

        plt.ylabel('Chidot [deg/s]')
        plt.xlabel('t [sec]')
        plt.grid(True)


        # figure 5
        plt.figure(6)
        figno[4] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, latAccel)
        if useLatAccelCons == 1:
            plt.plot(t, lataccel_maxVal*np.ones(t.shape)/32.2, linestyle='--', color='r')
            plt.plot(t, -lataccel_maxVal*np.ones(t.shape)/32.2, linestyle='--', color='r')

        plt.ylabel('Lat Accel [g]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, dyError)
        plt.plot(t, delta_yRoad * np.ones(t.shape), linestyle='--', color='r')
        plt.plot(t, -delta_yRoad * np.ones(t.shape), linestyle='--', color='r')
        plt.ylabel('dy Error [m]')
        plt.xlabel('t [sec]')
        plt.grid(True)


    elif ns == 6:

        # figure 2
        plt.figure(2)
        figno[1] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, x[:,[0]])  # E
        plt.ylabel('E [ft]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, x[:,[1]])  # N
        plt.ylabel('N [ft]')
        plt.xlabel('t [sec]')
        plt.grid(True)


        # figure 3
        plt.figure(3)
        figno[2] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, x[:,[2]])  # V
        plt.ylabel('V [fps]')

        #plt.plot(t, lb_V*np.ones(t.shape),linestyle='--', color='g')
        #plt.plot(t, ub_V*np.ones(t.shape), linestyle='--', color='g')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, x[:,[4]])  # Vdot

        plt.ylabel('Vdot [fps2]')
        plt.xlabel('t [sec]')
        plt.grid(True)


        # figure 4
        plt.figure(4)
        figno[3] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, x[:,[3]]*180/np.pi)
        plt.ylabel('Chi [deg]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, x[:,[5]]*180/np.pi)

        plt.ylabel('Chidot [deg/s]')
        plt.xlabel('t [sec]')
        plt.grid(True)

        # figure 5
        plt.figure(5)
        figno[4] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, u[:,0])
        plt.plot(t, lb_VddotVal*np.ones(t.shape),linestyle='--', color='r')
        plt.plot(t, ub_VddotVal*np.ones(t.shape), linestyle='--', color='r')
        plt.ylabel('Vddot [fps3]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, u[:,1]*180/np.pi)
        plt.plot(t, lb_ChiddotVal*np.ones(t.shape)*180/np.pi,linestyle='--', color='r')
        plt.plot(t, ub_ChiddotVal*np.ones(t.shape)*180/np.pi, linestyle='--', color='r')
        plt.ylabel('Chiddot [deg/s2]')
        plt.xlabel('t [sec]')
        plt.grid(True)

        # figure 6
        plt.figure(6)
        figno[5] = plt.gcf().number

        plt.subplot(211)
        plt.plot(t, latAccel)
        if useLatAccelCons == 1:
            plt.plot(t, lataccel_maxVal*np.ones(t.shape)/32.2, linestyle='--', color='r')
            plt.plot(t, -lataccel_maxVal*np.ones(t.shape)/32.2, linestyle='--', color='r')

        plt.ylabel('Lat Accel [g]')
        plt.grid(True)

        plt.subplot(212)
        plt.plot(t, dyError)
        plt.plot(t, delta_yRoad * np.ones(t.shape), linestyle='--', color='r')
        plt.plot(t, -delta_yRoad * np.ones(t.shape), linestyle='--', color='r')
        plt.ylabel('dy Error [m]')
        plt.xlabel('t [sec]')
        plt.grid(True)


    # figure 7
    iterations = np.arange(len(tElapsed))
    plt.figure(7)
    figno[6] = plt.gcf().number

    plt.plot(iterations, tElapsed)
    plt.ylabel('CPU Time [sec]')
    plt.xlabel('Iteration')
    plt.grid(True)


    # figure 8
    plt.figure(8)
    figno[7] = plt.gcf().number
    plt.plot(t, V_terminal)
    if ncons_option != 3:
        plt.plot(t, lb_V * np.ones(t.shape), linestyle='--', color='r')
        plt.plot(t, ub_V * np.ones(t.shape), linestyle='--', color='r')
    plt.ylabel('V-terminal [fps]')
    plt.xlabel('time [sec]')
    plt.grid(True)

    plt.pause(0.1)
    #plt.show()

    return figno

def nmpcPrint(mpciter, info, N, x, u_new, writeToFile, f, cpuTime, VTerminal):

    status = info['status']
    cost = info['obj_val']
    g = info['g']
    idx_lataccel = 2*N
    if pdata.ns == 6:
        #idx_trackingerror = 2*N + 2 # (nlp.py, option 1)
        idx_trackingerror = 2*N + 1 # (nlp.py, option 2,3)
    elif pdata.ns == 4:
        idx_trackingerror = 2*N + 1
    g1 = g[idx_lataccel]/32.2 # g
    g2 = g[idx_trackingerror] # ft
    text_g1 = "ay [g]"
    text_g2 = "dy [ft]"

    status_msg = info['status_msg']
    u = info['x']
    u0 = u[0]  # Vddot
    u1 = u[N] #Chiddot

    if pdata.ns == 6:
        text_u0 = "Vddot"
        text_u1 = "Chiddot"
    elif pdata.ns == 4:
        text_u0 = "Vdot"
        text_u1 = "Chidot"

    # 0       solved
    # 1       solved to acceptable level
    # 2       infeasible problem detected
    # 3       search direction becomes too small
    # 4       diverging iterates
    # 5       user requested stop
    # -1      maximum number of iterations exceeded
    # -2      restoration phase failed
    # -3      error in step computation
    # -10     not enough degrees of freedom
    # -11     invalid problem definition
    # -12     invalid option
    # -13     invalid number detected
    # -100    unrecoverable exception
    # -101    non-IPOPT exception thrown
    # -102    insufficient memo
    # -199    internal error

    if status == 0:
        status_msg_short = "Solved"
    elif status == 1:
        status_msg_short = "Acceptable"
    elif status == 2:
        status_msg_short = "Infeasible"
    elif status == -1:
        status_msg_short = "Max-Iter"
    elif status == 5:
        status_msg_short = "User-Stop"
    elif status == -13:
        status_msg_short = "Algorithm-Received"
    else:
        status_msg_short = status_msg[0:19]

    if writeToFile == True:
        # if mpciter == 0:
        #     f.write("%*s %*s %*s %*s %*s %*s %*s %*s %*s %*s\n" % (10, "mpciter", 10, "cost",
        #                                        7, text_u0, 7, text_u1,
        #                                        7, "V", 7, "Chi",
        #                                        7, text_g1, 7, text_g2, 15, "status_msg",
        #                                        10, "cpuTime") )

        # f.write("%*d %*.1f %*.1f %*.1f %*.1f %*.1f %*.2f %*.2f %*s %*.1f\n" % (10, mpciter, 10, cost,
        #                                          7, u0, 7, u1,
        #                                          7, x[2], 7, x[3]*180/np.pi,
        #                                          7, g1, 7, g2, 15, status_msg_short,
        #                                          10, cpuTime))

        if pdata.ns == 4:
            f.write("%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %s\n" % (
                x[0], x[1], x[2], x[3],
                u0, u1,
                g1, g2,
                VTerminal, cost, cpuTime, status_msg_short ))

        elif pdata.ns == 6:
            f.write("%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %s\n" % (
                x[0], x[1], x[2], x[3], x[4], x[5],
                u0, u1,
                g1, g2,
                VTerminal, cost, cpuTime, status_msg_short ))


    if mpciter == 0:
        print("%*s %*s %*s %*s %*s %*s %*s %*s %*s %*s %*s\n" % (10, "mpciter", 10, "cost",
                                               7, text_u0, 7, text_u1,
                                               7, "V", 7, "Chi", 7, "V-Terminal",
                                               7, text_g1, 7, text_g2, 15, "status_msg",
                                              10, "cpuTime") )

    print("%*d %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f %*.2f %*.2f %*s %*.1f\n" % (10, mpciter, 10, cost,
                                                 7, u0, 7, u1*180/np.pi,
                                                 7, x[2], 7, x[3]*180/np.pi, 7, VTerminal,
                                                 7, g1, 7, g2, 15, status_msg_short,
                                                10, cpuTime))

    return g1, g2

def savePlots(dirname,figno):
    try:
        os.makedirs(dirname)
    except OSError:
        pass
    # let exception propagate if we just can't
    # cd into the specified directory

    oldpwd = os.getcwd()
    os.chdir(dirname)

    for k in range(len(figno)):
        plt.savefig(figno[k])

    os.chdir(oldpwd)


def plotSavedData(inFile, delim, header=False):

    f = file(inFile, 'r')
    T = np.array(inFile[13]).astype(np.int)
    ns = np.array(inFile[17]).astype(np.int)
    cols, indexToName = getColumns(f, delim=delim, header=header)

    if ns == 4:
        nt = len(cols[0])
        t = T * np.arange(0, nt)

        x = np.zeros((4, nt))
        x[0] = np.array(cols[0]).astype(np.float)
        x[1] = np.array(cols[1]).astype(np.float)
        x[2] = np.array(cols[2]).astype(np.float)
        x[3] = np.array(cols[3]).astype(np.float)

        u = np.zeros((2, nt))
        u[0] = np.array(cols[4]).astype(np.float)
        u[1] = np.array(cols[5]).astype(np.float)

        path = None
        obstacle = None

        latAccel = np.array(cols[6]).astype(np.float)
        dyError = np.array(cols[7]).astype(np.float)
        VTerminal = np.array(cols[8]).astype(np.float)

        cpuTime = np.array(cols[10]).astype(np.float)


    elif ns == 6:
        nt = len(cols[0])

        t = T * np.arange(0, nt)

        x = np.zeros((6, nt))
        x[0] = np.array(cols[0]).astype(np.float)
        x[1] = np.array(cols[1]).astype(np.float)
        x[2] = np.array(cols[2]).astype(np.float)
        x[3] = np.array(cols[3]).astype(np.float)
        x[4] = np.array(cols[4]).astype(np.float)
        x[5] = np.array(cols[5]).astype(np.float)

        u = np.zeros((2, nt))
        u[0] = np.array(cols[6]).astype(np.float)
        u[1] = np.array(cols[7]).astype(np.float)

        path = None
        obstacle = None

        latAccel = np.array(cols[8]).astype(np.float)
        dyError = np.array(cols[9]).astype(np.float)
        VTerminal = np.array(cols[10]).astype(np.float)

        cpuTime = np.array(cols[12]).astype(np.float)


    suffix = inFile[7:]
    settingsFile = 'settings' + suffix
    nmpcPlot(t, x.T, u.T, path, obstacle, cpuTime, VTerminal, latAccel, dyError, settingsFile)

    f.close()

    plt.pause(0.1)

    return np.mean(cpuTime)



