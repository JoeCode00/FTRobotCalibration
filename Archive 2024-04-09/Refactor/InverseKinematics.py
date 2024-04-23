import numpy as np
from pandas import DataFrame
import dearpygui.dearpygui as dpg
def magnitude(vector):
    return np.sqrt(np.sum(np.square(vector)))

def unit_vector(vector):
  # Calculate the length of the vector.
  length = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
  # Divide each component of the vector by the length.
  unit_vector = [vector[0] / length, vector[1] / length, vector[2] / length]
  return unit_vector

def normalizejointangles(array):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            while array[i][j] >= np.pi:
                array[i][j] = array[i][j] - 2*np.pi
            while array[i][j] <= -np.pi:
                array[i][j] = array[i][j] + 2*np.pi
    return array

def phi1(Choice, JointAngle, Frames, X7, Y7, s71, gamma1):
    S4 = Frames.loc[3,'JointOffset']
    S6 = Frames.loc[5,'JointOffset']
    S7 = Frames.loc[6,'JointOffset']
    a71 = Frames.loc[6,'LinkLength']
    A = -S6*Y7 + S7*s71
    B = -S6*X7 - a71
    phi1cosArg = -S4/np.sqrt(np.square(A)+np.square(B))
    if Choice < 4:
        JointAngle[Choice,0] = np.arccos(phi1cosArg) + np.arctan2(B,A) - gamma1
    else:
        JointAngle[Choice,0] = -np.arccos(phi1cosArg) + np.arctan2(B,A) - gamma1
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def XYZ17(Choice, JointAngle, X7, Y7, Z7, c12, s12, c67, s67, c71, s71, gamma1):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = np.cos(theta1)
    s1 = np.sin(theta1)
    
    theta7 = JointAngle[Choice][6]
    c7 = np.cos(theta7)
    s7 = np.sin(theta7)
    
    BarX1 = s12*s1
    BarY1 = -(s71*c12 + c71*s12*c1)
    BarZ1 = c71*c12 - s71*s12*c1

    X17 = BarX1*c7 - BarY1*s7
    Y17 = c67*(BarX1*s7 + BarY1*c7) - s67*BarZ1
    Z17 = s67*(BarX1*s7 + BarY1*c7) - c67*BarZ1
    return X17, Y17, Z17        

def theta5(Choice, JointAngle, Z17):
    if Choice % 4 == 2 or Choice % 4 == 3:
        JointAngle[Choice, 4] = -np.arccos(Z17)
    else:
        JointAngle[Choice, 4] = np.arccos(Z17)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta6(Choice, JointAngle, X17, Y17):
    theta5 = JointAngle[Choice, 4]
    c6 = -X17/np.sin(theta5)
    s6 = Y17/np.sin(theta5)
    JointAngle[Choice, 5] = np.arctan2(s6, c6)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def XYZ671(Choice, JointAngle, c56, s56, c67, s67, c71, s71, c12, s12, gamma1):
    
    theta6 = JointAngle[Choice][5]
    c6 = np.cos(theta6)
    s6 = np.sin(theta6)
    
    X6 = s56*s6
    Y6 = -(s67*c56 + c67*s56*c6)
    Z6 = c67*c56 - s67*s56*c6
    
    theta7 = JointAngle[Choice][6]
    c7 = np.cos(theta7)
    s7 = np.sin(theta7)
    
    X67 = X6*c7 - Y6*s7
    Y67 = c71*(X6*s7 + Y6*c7) - s71*Z6
    Z67 = s71*(X6*s7 + Y6*s7) + c71*Z6
    
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = np.cos(theta1)
    s1 = np.sin(theta1)
    
    X671 = X67*c1 - Y67*s1
    Y671 = c12*(X67*s1 + Y67*c1) - s12*Z67  
    Z671 = s12*(X67*s1 + Y67*c1) - c12*Z67
    return X671, Y671, Z671

def XY71(Choice, JointAngle, gamma1, X7, Y7, Z7, c12, s12):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = np.cos(theta1)
    s1 = np.sin(theta1)
    
    X71 = X7*c1 - Y7*s1
    Y71 = c12*(X7*s1 + Y7*c1) - s12*Z7    
    return X71, Y71

def XYZ1(Choice, JointAngle, c12, s12, c71, s71, gamma1):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = np.cos(theta1)
    s1 = np.sin(theta1)
    
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
    c1 = np.cos(theta1)
    
    K1 = -S5*X671 - S6*X71 - S7*X1 - a71*c1
    K2 = -S1 - S5*Y671 - S6*Y71 - S7*Y1
    return K1, K2

def theta3(Choice, JointAngle, Frames, K1, K2):
    a23 = Frames.loc[1,'LinkLength']
    a34 = Frames.loc[2,'LinkLength']
    
    A = (np.square(K1) + np.square(K2) - np.square(a23) - np.square(a34))/(2*a23*a34)
    
    if Choice % 2 == 0:
        JointAngle[Choice, 2] = np.arccos(A)
    else:
        JointAngle[Choice, 2] = -np.arccos(A)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta2(Choice, JointAngle, Frames, K1, K2):
    a23 = Frames.loc[1,'LinkLength']
    a34 = Frames.loc[2,'LinkLength']
    
    theta3 = JointAngle[Choice][2]
    c3 = np.cos(theta3)
    s3 = np.sin(theta3)
    
    A = K1/np.sqrt(np.square(a23 + a34*c3)+np.square(-a34*s3))
    B1 = (-a34*s3)
    B2 = (a23 + a34*c3)
    C = K2/np.sqrt(np.square(-a34*s3)+np.square(-a23 - a34*c3))
    D1 = (-a23 - a34*c3)
    D2 = (-a34)*s3
    
    theta2a =  np.arccos(A) + np.arctan2(B1, B2)
    theta2b = -np.arccos(A) + np.arctan2(B1, B2)
    theta2c =  np.arccos(C) + np.arctan2(D1, D2)
    theta2d = -np.arccos(C) + np.arctan2(D1, D2)
    
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
    c2 = np.cos(theta2)
    s2 = np.sin(theta2)
    
    c23 = 1
    s23 = 0
    
    X6712 = X671*c2-Y671*s2
    Y6712 = c23*(X671*s2 + Y671*c2) - s23*Z671
    Z6712 = s23*(X671*s2 + Y671*c2) - c23*Z671
    
    theta3 = JointAngle[Choice][2]
    c3 = np.cos(theta3)
    s3 = np.sin(theta3)
    
    c34 = 1
    s34 = 0
    
    X67123 = X6712*c3 - Y6712*s3
    Y67123 = c34*(X6712*s3 + Y6712*c3) - s34*Z6712
    
    JointAngle[Choice, 3] = np.arctan2(-X67123, -Y67123)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def inverse_kinematics(v_FPtool, v_FS6, v_Fa67):
    
                                            #   a12         a23     a34     a45             a56             a67         a71
    Frames = DataFrame(data = {'LinkLength': [  0,          700,    900,    0,              0,              0,          0],
                               
                                               #α12         α23     α34     α45             α56             α67         α71
                               'TwistAngle': [  3*np.pi/2,  0,      0,      3*np.pi/2,      np.pi/2,        np.pi/2,    0],
                               
                                              # S1          S2      S3      S4              S5              S6          S7
                               'JointOffset':[  0,          0,      0,      98,             145,            241.3,        0]}, dtype=object)    
    
    #ϕ1  θ2  θ3  θ4  θ5  θ6  θ7
    JointAngle = np.array(np.zeros((8,7))) #pose, joint                                  
    
    # v_6Ptool    = np.array([20,         30,         50])
    v_6Ptool    = np.array([0,         0,         0])
    # v_FPtool    = np.array([800,        800,        180])
    # v_FS6       = np.array([-0.5774,    0.5774,    0.5774])
    # v_Fa67      = np.array([ 0.4082,    0.8165,    -0.4082])
    
    v_FS1       = np.array([0, 0, 1])
    v_i         = np.array([1, 0, 0])
    v_j         = np.array([0, 1, 0])
    v_k         = np.array([0, 0, 1])
    
    v_FS7   = np.cross(v_Fa67, v_FS6)
    v_Fa71  = np.cross(v_FS7, v_FS1)/magnitude(np.cross(v_FS7, v_FS1))
    
    #α71
    c71 = np.dot(v_FS7, v_FS1)
    s71 = np.dot(np.cross(v_FS7, v_FS1), v_Fa71)
    Frames.loc[6,'TwistAngle'] = np.arctan2(s71, c71)
    
    #θ7
    c7 = np.dot(v_Fa67, v_Fa71)
    s7 = np.dot(np.cross(v_Fa67, v_Fa71), v_FS7)
    JointAngle[:,6] = np.arctan2(s7, c7)
    
    #γ1
    cgamma1 = np.dot(v_Fa71, v_i)
    sgamma1 = np.dot(np.cross(v_Fa71, v_i), v_FS1)
    gamma1 = np.arctan2(sgamma1, cgamma1)
    
    try:
        #S7, a71, S1
        v_FP6orig = v_FPtool - np.dot(v_6Ptool, v_i)*v_Fa67 - np.cross(np.dot(v_6Ptool, v_j)*v_FS6, v_Fa67) - np.dot(v_6Ptool,v_k)*v_FS6
    except Exception as e:
        print(e)
        breakpoint()
        #S7
    Frames.loc[6,'JointOffset'] = np.dot(np.cross(v_FS1, v_FP6orig), v_Fa71)/s71
        #a71
        
    Frames.loc[6,'LinkLength']  = np.dot(np.cross(v_FP6orig, v_FS1), v_FS7) /s71
        #S1
    Frames.loc[0,'JointOffset'] = np.dot(np.cross(v_FP6orig, v_FS7), v_Fa71)/s71
    
    #X7, Y7, Z7
    c67 = np.dot(v_FS6, v_FS7)
    s67 = np.dot(np.cross(v_FS6, v_FS7), v_Fa67)
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
    
    return JointAngle

def joint_angle_updater(PositionVectorS, FTZS, FTXS, ThetaValueR):
    
    # FTTool = np.vstack([np.hstack([FTXS, np.cross(FTZS, FTXS), FTZS, PositionVectorS]), 
    #                     np.array([ 0,    0,                    0,    1])])
    # alpha6Tool = np.deg2rad(22.5)
    # ToolT6 = np.array([[np.cos(alpha6Tool), -np.sin(alpha6Tool),0, 0],
    #                    [np.sin(alpha6Tool), np.cos(alpha6Tool), 0, 0],
    #                    [0,                  0,                  1, 0],
    #                    [0,                  0,                  0, 1]])
    
    # FT6 = np.matmul(FTTool, ToolT6)
    
    v_FPtool    = np.array(PositionVectorS)
    v_FS6       = np.array(FTZS)
    v_Fa67      = np.array(FTXS)
    
    # v_FPtool    = np.reshape(FT6[0:3,3], (1,3))
    # v_FS6       = np.reshape(FT6[0:3,2], (1,3))
    # v_Fa67      = np.reshape(FT6[0:3,0], (1,3))
    
    try:
        JointAngleCommand = inverse_kinematics(v_FPtool, v_FS6, v_Fa67)
    except:
        breakpoint()
    JointAngleCommandDeg = np.rad2deg(JointAngleCommand[:,0:6])
    
    # if ((PositionVectorR is not None) and
    #     (FTZR is not None) and
    #     (FTXR is not None)):

        
    #     JointAngleRecieved = inverse_kinematics(PositionVectorR, FTZR, FTXR)
    #     JointAngleRecieved = ThetaValueR

            
    #     JointAngleRecievedDeg = np.rad2deg(JointAngleRecieved[:,0:6])
    # else:
    #     JointAngleRecievedDeg = None
    JointAngleRecievedDeg = np.rad2deg(ThetaValueR)
    
    # breakpoint()
    for i in range(8):
        for j in range(6):
            if not np.isnan(JointAngleCommandDeg[i][j]):
                dpg.set_value(f"{i},{j} Command", str(np.round(JointAngleCommandDeg[i][j], 3)))
                if JointAngleRecievedDeg is not None:
                    Delta = np.round(JointAngleCommandDeg[i][j] - JointAngleRecievedDeg[j], 3)
                    dpg.set_value(f"{i},{j} Delta", str(Delta))
                else:
                    dpg.set_value(f"{i},{j} Delta", 'Nan')
            else:
                dpg.set_value(f"{i},{j} Command", 'NaN')
                
        
    # breakpoint()
    return JointAngleCommandDeg