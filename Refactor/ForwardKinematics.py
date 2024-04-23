# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 19:52:37 2024

@author: Joe
"""
import numpy as np
import src.Robots2 as R2
np.set_printoptions(suppress=True)
def forward_kinematics(ThetaList):
                                                

                            #a0 a1 a2   a3   a4 a5 aFT aProbe
    LinkLength =            [0, 0, 700, 900, 0, 0, 0,  31.4]
    
                            #α0  α1  α2 α3 α4   α5  αFT αProbe
    TwistAngle = np.deg2rad([0, 270, 0, 0, 270, 90, 0,  0])
    
                            #0s1 1s2 2s3  3s4 4s5    5s6      6sFT   FTSProbe
    JointOffset =           [0, 0,   0,   98, 145,   241.3,   -33.6, 30.3]
    
                            #0ϕ1-5θ6   6θFT FTθProbe
    JointAngle =            ThetaList+[0, 0]

    Tij = [0]*8
    for i in range(8):
        Tij[i] = R2.T_from_robot_param(LinkLength[i], #
                                       TwistAngle[i], #
                                       JointOffset[i],  #
                                       JointAngle[i]) #
    T0j = [0]*8
    T0j[0] = Tij[0]

    
    for j in range(1,8):
        T0j[j] = np.matmul(T0j[j-1], Tij[j])
    
    Slist = [0]*8
    SOLlist = [0]*8
    Plist = [0]*8
    for i in range(8):
        Slist[i] = R2.S_from_T(T0j[i])
        Plist[i] = R2.P_from_T(T0j[i])
        SOLlist[i] = R2.vcross(Plist[i], Slist[i])
    
   
    return T0j, Tij
    
