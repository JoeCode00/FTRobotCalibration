# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 22:31:36 2023

@author: Joe
"""
#all units in mm or rad

import numpy as np
from numpy import array, cross, dot, sqrt, square, arctan2, arccos, rad2deg, cos, sin
import pandas as pd

def magnitude(vector):
    return sqrt(np.sum(square(vector)))

def normalizejointangles(array):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            while array[i][j] >= pi:
                array[i][j] = array[i][j] - 2*pi
            while array[i][j] <= -pi:
                array[i][j] = array[i][j] + 2*pi
    return array

def phi1(Choice, JointAngle, Frames, X7, Y7, s71, gamma1):
    S4 = Frames.loc[3,'JointOffset']
    S6 = Frames.loc[5,'JointOffset']
    S7 = Frames.loc[6,'JointOffset']
    a71 = Frames.loc[6,'LinkLength']
    A = -S6*Y7 + S7*s71
    B = -S6*X7 - a71
    phi1arccosArg = -S4/sqrt(square(A)+square(B))
    if Choice < 4:
        JointAngle[Choice,0] = arccos(phi1arccosArg) + arctan2(B,A) - gamma1
    else:
        JointAngle[Choice,0] = -arccos(phi1arccosArg) + arctan2(B,A) - gamma1
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def XYZ17(Choice, JointAngle, X7, Y7, Z7, c12, s12, c67, s67, c71, s71, gamma1):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    theta7 = JointAngle[Choice][6]
    c7 = cos(theta7)
    s7 = sin(theta7)
    
    BarX1 = s12*s1
    BarY1 = -(s71*c12 + c71*s12*c1)
    BarZ1 = c71*c12 - s71*s12*c1

    X17 = BarX1*c7 - BarY1*s7
    Y17 = c67*(BarX1*s7 + BarY1*c7) - s67*BarZ1
    Z17 = s67*(BarX1*s7 + BarY1*c7) - c67*BarZ1
    return X17, Y17, Z17        

def theta5(Choice, JointAngle, Z17):
    if Choice % 4 == 2 or Choice % 4 == 3:
        JointAngle[Choice, 4] = -arccos(Z17)
    else:
        JointAngle[Choice, 4] = arccos(Z17)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta6(Choice, JointAngle, X17, Y17):
    theta5 = JointAngle[Choice, 4]
    c6 = -X17/sin(theta5)
    s6 = Y17/sin(theta5)
    JointAngle[Choice, 5] = arctan2(s6, c6)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def XYZ671(Choice, JointAngle, c56, s56, c67, s67, c71, s71, c12, s12, gamma1):
    
    theta6 = JointAngle[Choice][5]
    c6 = cos(theta6)
    s6 = sin(theta6)
    
    X6 = s56*s6
    Y6 = -(s67*c56 + c67*s56*c6)
    Z6 = c67*c56 - s67*s56*c6
    
    theta7 = JointAngle[Choice][6]
    c7 = cos(theta7)
    s7 = sin(theta7)
    
    X67 = X6*c7 - Y6*s7
    Y67 = c71*(X6*s7 + Y6*c7) - s71*Z6
    Z67 = s71*(X6*s7 + Y6*s7) + c71*Z6
    
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    X671 = X67*c1 - Y67*s1
    Y671 = c12*(X67*s1 + Y67*c1) - s12*Z67  
    Z671 = s12*(X67*s1 + Y67*c1) - c12*Z67
    return X671, Y671, Z671

def XY71(Choice, JointAngle, gamma1, X7, Y7, Z7, c12, s12):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    X71 = X7*c1 - Y7*s1
    Y71 = c12*(X7*s1 + Y7*c1) - s12*Z7    
    return X71, Y71

def XYZ1(Choice, JointAngle, c12, s12, c71, s71, gamma1):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    X1 = s71*s1
    Y1 = -(s12*c71 + c12*s71*c1)
    Z1 = c12*c71 - s12*s71*c1
    return X1, Y1, Z1

def K(Choice, JointAngle, Frames, gamma1, X1, Y1, X71, Y71, X671, Y671):
    S1  = Frames.loc[0,'JointOffset']
    S5  = Frames.loc[4,'JointOffset']
    S6  = Frames.loc[5,'JointOffset']
    S7  = Frames.loc[6,'JointOffset']
    a71 = Frames.loc[6,'LinkLength']
    
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    
    K1 = -S5*X671 - S6*X71 - S7*X1 - a71*c1
    K2 = -S1 - S5*Y671 - S6*Y71 - S7*Y1
    return K1, K2

def theta3(Choice, JointAngle, Frames, K1, K2):
    a23 = Frames.loc[1,'LinkLength']
    a34 = Frames.loc[2,'LinkLength']
    
    A = (square(K1) + square(K2) - square(a23) - square(a34))/(2*a23*a34)
    
    if Choice % 2 == 0:
        JointAngle[Choice, 2] = arccos(A)
    else:
        JointAngle[Choice, 2] = -arccos(A)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta2(Choice, JointAngle, Frames, K1, K2):
    a23 = Frames.loc[1,'LinkLength']
    a34 = Frames.loc[2,'LinkLength']
    
    theta3 = JointAngle[Choice][2]
    c3 = cos(theta3)
    s3 = sin(theta3)
    
    A = K1/sqrt(square(a23 + a34*c3)+square(-a34*s3))
    B1 = (-a34*s3)
    B2 = (a23 + a34*c3)
    C = K2/sqrt(square(-a34*s3)+square(-a23 - a34*c3))
    D1 = (-a23 - a34*c3)
    D2 = (-a34)*s3
    
    theta2a =  arccos(A) + arctan2(B1, B2)
    theta2b = -arccos(A) + arctan2(B1, B2)
    theta2c =  arccos(C) + arctan2(D1, D2)
    theta2d = -arccos(C) + arctan2(D1, D2)
    
    if np.round(theta2a, 5) == np.round(theta2c, 5) or np.round(theta2a, 5) == np.round(theta2d, 5):
        JointAngle[Choice, 1] = theta2a
    elif np.round(theta2b, 5) == np.round(theta2c, 5) or np.round(theta2b, 5) == np.round(theta2d, 5):
        JointAngle[Choice, 1] = theta2b
    else:
        JointAngle[Choice, 1] = np.nan
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta4(Choice, JointAngle, X671, Y671, Z671):
    theta2 = JointAngle[Choice][1]
    c2 = cos(theta2)
    s2 = sin(theta2)
    
    c23 = 1
    s23 = 0
    
    X6712 = X671*c2-Y671*s2
    Y6712 = c23*(X671*s2 + Y671*c2) - s23*Z671
    Z6712 = s23*(X671*s2 + Y671*c2) - c23*Z671
    
    theta3 = JointAngle[Choice][2]
    c3 = cos(theta3)
    s3 = sin(theta3)
    
    c34 = 1
    s34 = 0
    
    X67123 = X6712*c3 - Y6712*s3
    Y67123 = c34*(X6712*s3 + Y6712*c3) - s34*Z6712
    
    JointAngle[Choice, 3] = arctan2(-X67123, -Y67123)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

pi = np.pi
                                                                                                        #0   1   2   3   4   5   6
Frames = pd.DataFrame(data = {'LinkLength': [0,         700,    900,    0,      0,      0,      0],     #a12 a23 a34 a45 a56 a67 a71
                              'TwistAngle': [3*pi/2,    0,      0,      3*pi/2, pi/2,   pi/2,   0],     #α12 α23 α34 α45 α56 α67 α71
                              'JointOffset':[0,         0,      0,      98,     145,    152.4,  0]})    #S1  S2  S3  S4  S5  S6  S7

#ϕ1  θ2  θ3  θ4  θ5  θ6  θ7
JointAngle = array(np.zeros((8,7))) #pose, joint                                  

v_6Ptool    = array([20,         30,         50])
v_FPtool    = array([800,        800,        180])
v_FS6       = array([-0.5774,    0.5774,    0.5774])
v_Fa67      = array([ 0.4082,    0.8165,    -0.4082])

v_FS1       = array([0, 0, 1])
v_i         = array([1, 0, 0])
v_j         = array([0, 1, 0])
v_k         = array([0, 0, 1])

v_FS7   = cross(v_Fa67, v_FS6)
v_Fa71  = cross(v_FS7, v_FS1)/magnitude(cross(v_FS7, v_FS1))

#α71
c71 = dot(v_FS7, v_FS1)
s71 = dot(cross(v_FS7, v_FS1), v_Fa71)
Frames.loc[6,'TwistAngle'] = arctan2(s71, c71)

#θ7
c7 = dot(v_Fa67, v_Fa71)
s7 = dot(cross(v_Fa67, v_Fa71), v_FS7)
JointAngle[:,6] = arctan2(s7, c7)

#γ1
cgamma1 = dot(v_Fa71, v_i)
sgamma1 = dot(cross(v_Fa71, v_i), v_FS1)
gamma1 = arctan2(sgamma1, cgamma1)

#S7, a71, S1
v_FP6orig = v_FPtool - dot(v_6Ptool, v_i)*v_Fa67 - cross(dot(v_6Ptool, v_j)*v_FS6, v_Fa67) - dot(v_6Ptool,v_k)*v_FS6
    #S7
Frames.loc[6,'JointOffset'] = dot(cross(v_FS1, v_FP6orig), v_Fa71)/s71
    #a71
Frames.loc[6,'LinkLength']  = dot(cross(v_FP6orig, v_FS1), v_FS7) /s71
    #S1
Frames.loc[0,'JointOffset'] = dot(cross(v_FP6orig, v_FS7), v_Fa71)/s71

#X7, Y7, Z7
c67 = dot(v_FS6, v_FS7)
s67 = dot(cross(v_FS6, v_FS7), v_Fa67)
X7 = s67*s7
Y7 = -(s71*c67 + c71*s67*c7)
Z7 = c71*c67 - s71*s67*c7

for Choice in range(8):
    #ϕ1
    JointAngle = phi1(Choice, JointAngle, Frames, X7, Y7, s71, gamma1)
    
    c12 = 0
    s12 = -1
    X17, Y17, Z17 = XYZ17(Choice, JointAngle, X7, Y7, Z7, c12, s12, c67, s67, c71, s71, gamma1)
    
    #θ5
    JointAngle = theta5(Choice, JointAngle, Z17)
    
    #θ6
    JointAngle = theta6(Choice, JointAngle, X17, Y17)    
    
    c56 = 0
    s56 = 1
    X671, Y671, Z671 = XYZ671(Choice, JointAngle, c56, s56, c67, s67, c71, s71, c12, s12, gamma1)
    X71, Y71 = XY71(Choice, JointAngle, gamma1, X7, Y7, Z7, c12, s12)
    X1, Y1, Z1 = XYZ1(Choice, JointAngle, c12, s12, c71, s71, gamma1)
    K1, K2 = K(Choice, JointAngle, Frames, gamma1, X1, Y1, X71, Y71, X671, Y671)
    
    #θ3
    JointAngle = theta3(Choice, JointAngle, Frames, K1, K2)
    
    #θ2
    JointAngle = theta2(Choice, JointAngle, Frames, K1, K2)

    #θ4
    JointAngle = theta4(Choice, JointAngle, X671, Y671, Z671)
    
JointAngleDeg = rad2deg(JointAngle[:,0:6])