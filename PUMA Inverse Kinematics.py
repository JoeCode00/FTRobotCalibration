# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 22:31:36 2023

@author: Joe
"""
#all units in mm or rad

import numpy as np
from numpy import array, cross, dot, sqrt, square, arctan2, arccos, rad2deg
import pandas as pd

def magnitude(vector):
    return sqrt(np.sum(square(vector)))

pi = np.pi
                                                                                                        #0   1   2   3   4   5   6
Frames = pd.DataFrame(data = {'LinkLength': [0,         17,     0.8,    0,      0,      0,      0],     #a12 a23 a34 a45 a56 a67 a71
                              'TwistAngle': [pi/2,      0,      3*pi/2, pi/2,   pi/2,   pi/2,   0],     #α12 α23 α34 α45 α56 α67 α71
                              'JointOffset':[0,         5.9,    0,      17,     0,      2,      0]})    #S1  S2  S3  S4  S5  S6  S7

#ϕ1  θ2  θ3  θ4  θ5  θ6  θ7
JointAngle = array(np.zeros((8,7))) #pose, joint                                  

v_6Ptool    = array([5,         3,         7])
v_FPtool    = array([25,        23,        24])
v_FS6       = array([0.177,    0.844,    -0.433])
v_Fa67      = array([-0.153,    0.459,    0.875])

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

#ϕ1
S4 = Frames.loc[3,'JointOffset']
S6 = Frames.loc[5,'JointOffset']
S7 = Frames.loc[6,'JointOffset']
a71 = Frames.loc[6,'LinkLength']
A = -S6*Y7 + S7*s71
B = -S6*X7 - a71
phi1arccosArg = -S4/sqrt(square(A)+square(B))
JointAngle[0:4,0] = arccos(phi1arccosArg) + arctan2(B,A) - gamma1
JointAngle[4:8,0] = -arccos(phi1arccosArg) + arctan2(B,A) - gamma1

JointAngleDeg = rad2deg(JointAngle)