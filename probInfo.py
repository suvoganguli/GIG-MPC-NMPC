from problemData import *
from utils import *

def system(uk, xk, T):

    if ns == 2:
        # x0 = E, x1 = N
        # u0 = V, u1 = Chi

        xkp1 = [0, 0]
        xkp1[0] = xk[0] + T * uk[0] * np.sin(uk[1]) # Edot
        xkp1[1] = xk[1] + T * uk[0] * np.cos(uk[1]) # Ndot

    elif ns == 4:
        # x0 = E, x1 = N, x2 = V, x3 = Chi
        # u0 = Vdot, u1 = Chidot

        sys = 'nonlin'

        if sys == 'nonlin':

            xkp1 = [0, 0, 0, 0]
            xkp1[0] = xk[0] + T * xk[2] * np.sin(xk[3]) # Edot
            xkp1[1] = xk[1] + T * xk[2] * np.cos(xk[3]) # Ndot
            xkp1[2] = xk[2] + T * uk[0]                 # Vdot
            xkp1[3] = xk[3] + T * uk[1]                 # Chidot

        elif sys == 'lin':

            x0_k = [0, 0, 14.7, 0]

            del_u_k = uk
            del_x_k = xk

            E0_k = x0_k[0]
            N0_k = x0_k[1]
            V0_k = x0_k[2]
            Chi0_k = x0_k[3]

            del_E_k = del_x_k[0]
            del_N_k = del_x_k[1]
            del_V_k = del_x_k[2]
            del_Chi_k = del_x_k[3]

            del_u1_k = del_u_k[0]
            del_u2_k = del_u_k[1]

            del_E_kp1 = del_E_k + T * (np.sin(Chi0_k) * del_V_k + V0_k * np.cos(Chi0_k) * del_Chi_k)  # Edot
            del_N_kp1 = del_N_k + T * (np.cos(Chi0_k) * del_V_k - V0_k * np.sin(Chi0_k) * del_Chi_k)  # Edot
            del_V_kp1 = del_V_k + T * del_u1_k
            del_Chi_kp1 = del_Chi_k + T * del_u2_k

            x_del_kp1 = np.array([del_E_kp1, del_N_kp1, del_V_kp1, del_Chi_kp1])

            xkp1 = x_del_kp1


    elif ns == 6:
        # x0 = E, x1 = N, x2 = V, x3 = Chi, x5 = Vdot, x6 = Chidot
        # u0 = Vddot, u1 = Chiddot

        xkp1 = [0 ,0, 0, 0, 0, 0]
        xkp1[0] = xk[0] + T * xk[2] * np.sin(xk[3])     # Edot
        xkp1[1] = xk[1] + T * xk[2] * np.cos(xk[3])     # Ndot
        xkp1[2] = xk[2] + T * xk[4]                     # Vdot
        xkp1[3] = xk[3] + T * xk[5]                     # Chidot
        xkp1[4] = xk[4] + T * uk[0]                     # Vddot
        xkp1[5] = xk[5] + T * uk[1]                     # Chiddot

    else:
        xkp1 = []

    return xkp1


def runningCosts(u, x, t0, path, obstacle, posIdx = None, V_cmd = None):

    if ns == 6:
        cost_v = W_V * (V_cmd - x[2]) ** 2
        cost_vddot = W_Vddot * u[0] ** 2
        cost_Chiddot = W_Chiddot * (u[1] * 180 / np.pi) ** 2
        cost_x = cost_v
        cost_u = cost_vddot + cost_Chiddot
        cost = cost_x + cost_u

        costbreakdown = np.zeros(3)
        costbreakdown[0] = cost_v
        costbreakdown[1] = cost_vddot
        costbreakdown[2] = cost_Chiddot

    elif ns == 4:
        cost_v = W_V * (V_cmd - x[2]) ** 2
        cost_vdot = W_Vdot * u[0] ** 2
        cost_Chidot = W_Chidot * (u[1] * 180 / np.pi) ** 2
        #cost_x = cost_v
        #cost_u = cost_vdot + cost_Chidot
        #cost = cost_x + cost_u

        costvec = np.zeros(3)
        costvec[0] = cost_v
        costvec[1] = cost_vdot
        costvec[2] = cost_Chidot

    else:
        costvec = 0.0

    return costvec

    # A = path.alongPathLines.A
    # B = path.alongPathLines.B
    # C = path.alongPathLines.C
    # AR = path.alongPathLines.AR
    # BR = path.alongPathLines.BR
    # CR = path.alongPathLines.CR
    # AL = path.alongPathLines.AL
    # BL = path.alongPathLines.BL
    # CL = path.alongPathLines.CL
    #
    # D1 = path.acrossPathLines.D1
    # E1 = path.acrossPathLines.E1
    # F1 = path.acrossPathLines.F1
    # D2 = path.acrossPathLines.D2
    # E2 = path.acrossPathLines.E2
    # F2 = path.acrossPathLines.F2
    #
    # nSections = len(D1)
    #
    # if posIdx == None:
    #     kvec = range(nSections)
    # else:
    #     kvec = np.arange(posIdx['number'], nSections, 1)
    #
    # for k in kvec:
    #
    #     cost = 0.0
    #
    #     inbox = insideBox(x[0], x[1], AR[k], BR[k], CR[k], AL[k], BL[k], CL[k],
    #                  D1[k], E1[k], F1[k], D2[k], E2[k], F2[k])
    #
    #     # inside road segment
    #     if inbox == True:
    #
    #         if obstacle.Present == False:
    #             a = A[k]
    #             b = B[k]
    #             c = C[k]
    #         else:
    #             print("TBD")
    #
    #         if ns == 6:
    #             cost_p = W_P * (a * x[0] + b * x[1] - c) ** 2 / (a ** 2 + b ** 2)
    #             cost_v = W_V * (V_cmd - x[2])**2
    #             cost_vddot = W_Vddot * u[0]**2
    #             cost_Chiddot = W_Chiddot * (u[1]*180/np.pi)**2
    #             cost_x = cost_p + cost_v
    #             cost_u = cost_vddot + cost_Chiddot
    #             cost = cost_x + cost_u
    #
    #         elif ns == 4:
    #             cost_p = W_P * (a * x[0] + b * x[1] - c) ** 2 / (a ** 2 + b ** 2)
    #             cost_v = W_V * (V_cmd - x[2])**2
    #             cost_vdot = W_Vdot * u[0]**2
    #             cost_Chidot = W_Chidot * (u[1]*180/np.pi)**2
    #             cost_x = cost_p + cost_v
    #             cost_u = cost_vdot + cost_Chidot
    #             cost = cost_x + cost_u
    #
    #         return cost
    #
    #     else:
    #         cost = 1e6
    #
    # return cost


def goalCost(x, t0):

    goalDist = np.sqrt((endPoint[0] - x[0]) ** 2 + (endPoint[1] - x[1]) ** 2)
    cost_goalDist = W_gDist * goalDist**2

    dE = (endPoint[1] - x[1])
    dN = (endPoint[0] - x[0])

    # converting heading to deg for proper scaling
    Chi_goal = np.arctan2(dN, dE) * 180 / np.pi   # w.r.t +ve N axis
    Chi = x[3] * 180/np.pi
    delChi = Chi_goal - Chi

    cost_goalDelChi = W_gChi * np.abs(delChi)**2

    return np.array([cost_goalDist]), np.array([cost_goalDelChi])


def runningCons(u, x, t0, path, obstacle, posIdx=None):

    return np.array([], dtype=float)

    # cons = [0,0] #[1,-1]  will lead to both constraints false in nlp.py
    # yDist = np.zeros(2) # with respect to road axis (x - along, y - across)
    # found_sol = False
    #
    # AR = path.alongPathLines.AR
    # BR = path.alongPathLines.BR
    # CR = path.alongPathLines.CR
    # AL = path.alongPathLines.AL
    # BL = path.alongPathLines.BL
    # CL = path.alongPathLines.CL
    #
    # D1 = path.acrossPathLines.D1
    # E1 = path.acrossPathLines.E1
    # F1 = path.acrossPathLines.F1
    # D2 = path.acrossPathLines.D2
    # E2 = path.acrossPathLines.E2
    # F2 = path.acrossPathLines.F2
    #
    # nSections = len(D1)
    # if posIdx == None:
    #     kvec = range(nSections)
    # else:
    #     kvec = np.arange(posIdx['number'], nSections, 1)
    #
    # for k in kvec:
    #
    #     inbox = insideBox(x[0], x[1], AR[k], BR[k], CR[k], AL[k], BL[k], CL[k],
    #                  D1[k], E1[k], F1[k], D2[k], E2[k], F2[k])
    #
    #     # inside road segment
    #     if inbox == True:
    #
    #         if obstacle.Present == False:     # stay one lane 1
    #             a1 = AR[k]
    #             b1 = BR[k]
    #             c1 = CR[k]
    #             a2 = AL[k]
    #             b2 = BL[k]
    #             c2 = CL[k]
    #             found_sol = True
    #
    #         else:
    #             print("TBD")
    #
    #         if found_sol == True:
    #             yDist[0] = (a1 * x[0] + b1 * x[1] - c1)/np.sqrt(a1**2 + b1**2)
    #             yDist[1] = (a2 * x[0] + b2 * x[1] - c2)/np.sqrt(a2**2 + b2**2)
    #             cons[0] = np.sign(yDist[0]) # not used
    #             cons[1] = np.sign(yDist[1]) # not used
    #             return yDist
    #         else:
    #             # calculate the yDist anyway
    #             yDist[0] = (a1 * x[0] + b1 * x[1] - c1) / np.sqrt(a1 ** 2 + b1 ** 2)
    #             yDist[1] = (a2 * x[0] + b2 * x[1] - c2) / np.sqrt(a2 ** 2 + b2 ** 2)
    #             continue
    #
    #     else:
    #         None
    #
    # if found_sol == False:
    #     # print('No solution found in runningCons function')
    #     # return ([np.NAN, np.NaN])
    #     # return the yDist anyway
    #     return yDist


def terminalCons(u, x, t0, path, obstacle, posIdx=None):

    empty = np.array([], dtype=float) # yDist
    VEnd = np.array([x[2]]) # VEnd

    dN = (endPoint[1] - x[1])
    dE = (endPoint[0] - x[0])

    ChiGoal = np.arctan2(dE, dN) # w.r.t. +ve N axis
    Chi = x[3]

    delChi = np.array([ChiGoal - Chi])

    return empty, VEnd, delChi

    # found_sol = False
    #
    # A = path.alongPathLines.A
    # B = path.alongPathLines.B
    # C = path.alongPathLines.C
    # AR = path.alongPathLines.AR
    # BR = path.alongPathLines.BR
    # CR = path.alongPathLines.CR
    # AL = path.alongPathLines.AL
    # BL = path.alongPathLines.BL
    # CL = path.alongPathLines.CL
    #
    # D1 = path.acrossPathLines.D1
    # E1 = path.acrossPathLines.E1
    # F1 = path.acrossPathLines.F1
    # D2 = path.acrossPathLines.D2
    # E2 = path.acrossPathLines.E2
    # F2 = path.acrossPathLines.F2
    #
    #
    # nSections = len(D1)
    #
    # if posIdx == None:
    #     kvec = range(nSections)
    # else:
    #     kvec = np.arange(posIdx['number'], nSections, 1)
    #
    # for k in kvec:
    #     inbox = insideBox(x[0], x[1], AR[k], BR[k], CR[k], AL[k], BL[k], CL[k],
    #                  D1[k], E1[k], F1[k], D2[k], E2[k], F2[k])
    #     if inbox == True:
    #         if obstacle.Present == False:     # stay one lane 1
    #             a = A[k]
    #             b = B[k]
    #             c = C[k]
    #             found_sol = True
    #         else:
    #             print("TBD")
    #
    #         if found_sol == True:
    #             yDist = (a * x[0] + b * x[1] - c) / np.sqrt(a**2 + b**2)
    #             VEnd = x[2]
    #             return np.array([yDist]), np.array([VEnd])
    #         else:
    #             continue
    #
    #     else:
    #         None
    #
    # if found_sol == False:
    #     return np.array([np.NaN]), np.array([np.NaN])


def computeOpenloopSolution(u, N, T, t0, x0):
    x = np.zeros([N, np.size(x0)])
    x[0] = x0

    for k in range(N - 1):
        u0 = u[k]
        u1 = u[k+N]
        uk = np.array([u0,u1])
        x[k+1] = system(uk, x[k], T)
    return x

