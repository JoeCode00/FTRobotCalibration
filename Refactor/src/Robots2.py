import numpy as np
#%% Validity and Checks
def check_vectors_valid(VectorList): #checks vector shape and if it has numbers
    if type(VectorList) != list:
        if type(VectorList) == np.ndarray:
            VectorList = [VectorList]
    for Vector in VectorList:
       if not (check_vector_dtype(Vector) and check_vector_shape(Vector)):
        return False
    return True
    
def check_T_valid(T): #checks transformation shape and if it has valid vectors
    return (check_T_dtype(T) and check_T_shape(T) and check_T_unit(T))
        
def check_R_valid(R): #checks rotation shape and if it has valid vectors
    return (check_R_dtype(R) and check_R_shape(R) and check_R_unit(R))

def check_vector_dtype(Vector): #Can't opperate on non-number vectors
    if Vector.dtype.kind != 'i' and Vector.dtype.kind != 'f':
        raise Exception('Vector must have dtype of integer or float, not {}'
                        .format(Vector.dtype))
        return False
    return True
        
def check_vector_shape(Vector): #All vectors are assumed non-homogenous
    if np.shape(Vector) != (3,1):
        raise Exception("Vector must have np.shape (3,1), not {}"
                        .format(np.shape(Vector)))
        return False
    return True

def vector_length(Vector): #Same as vector magnitude, sqrt of sum of squares
    check_vectors_valid(Vector)
    PreSqrtLength = 0
    for i in range(np.shape(Vector)[0]):
            PreSqrtLength = PreSqrtLength + Vector[i]**2
    return round(float(np.sqrt(PreSqrtLength)),6)

def check_T_dtype(T): #Can't opperate on non-number matrix
    if T.dtype.kind != 'i' and T.dtype.kind != 'f':
        raise Exception('T matrix must have dtype of integer or float, not {}'
                        .format(T.dtype))
        return False
    return True    

def check_T_shape(T): #Transformation matrix must be a 4x4
    if np.shape(T) != (4,4):
        raise Exception("T matrix must have np.shape (4,4), not {}"
                        .format(np.shape(T)))
        return False
    return True

def check_R_dtype(R): #Can't opperate on non-number matrix
    if R.dtype.kind != 'i' and R.dtype.kind != 'f':
        raise Exception('R matrix must have dtype of integer or float, not {}'
                        .format(R.dtype))
        return False
    return True
    
def check_R_shape(R): #Rotation matrix must be a 3x3
    if np.shape(R) != (3,3):
        raise Exception("R matrix must have np.shape (3,3), not {}"
                        .format(np.shape(R)))
        return False
    return True

def check_S_SOL_perp(S,SOL):
    if vdot(S,SOL).round(3) != 0:
        raise Exception("S",S,", SOL",SOL," not perpendicular")
        return False
    return True        

def unit_vector(Vector):
    check_vectors_valid(Vector)
    if vector_length(Vector) != 0:
        UnitVector = Vector / vector_length(Vector)
        check_unit_vector(UnitVector)
    else:
        UnitVector = Vector
    return UnitVector
        
# def make_vector_unit(Vector): #Defintion of unit vector
    # return unit_vector(Vector)
        
def check_unit_vector(Vector): #3 decimal precision
    if round(vector_length(Vector),3) == 1:
        return True
    else:
        raise Exception('vector is not unit vector, length {}'
                        .format(vector_length(Vector)))
    
def aligned_T(): #No rotation, no translation
    return np.identity(4)

def aligned_R():
    return R_from_T(aligned_T())

def aligned_P():
    return P_from_T(aligned_T())


def check_R_unit(R): #Rotation matrix must have 3 orthogonal unit vectors
    Axis = ['X', 'Y', 'Z']
    for i in range(3):
        Vector = R[:,i].reshape((3,1))
        if not check_unit_vector(Vector):
            raise Exception('col {} ({}) of R is not unit vector'
                            .format(i, Axis[i]))
            return False
    for i in range(3):
        Vector1Row = (i+1) % 3
        Vector2Row = (i+2) % 3
        Vector1 =  R[Vector1Row,:]
        Vector2 =  R[Vector2Row,:]
        if round(np.dot(Vector1, Vector2),2) != 0:
            raise Exception('row {} ({})  and row {} ({}) of R are not perp.'
                            .format(Vector1Row, Axis[Vector1Row], 
                                    Vector2Row, Axis[Vector2Row]))
            return False
    return True
                
def check_T_unit(T): #Checks R unit and bottom row valid
    R = R_from_T(T)    
    if check_R_unit(R):
        if np.array_equal(T[3,:], np.array([0,0,0,1])):
            return True
        else:
            raise Exception('T bottom row is not [0,0,0,1], instead it is {}'
                            .format(T[3,:].tolist()))
    else:
        raise Exception('R in T was not unit vector')
        return False



#%%

def R_from_T(T): #Rotation matrix is top left 3x3 of transformation matrix
    R = T[0:3,0:3]
    check_R_unit(R)
    return R

def vector_from_R(R, Axis):
    check_R_valid(R)
    if Axis == 'x' or Axis == 'X' or Axis == 'a' or Axis == 'A' or Axis == 1:
        Vector = R[:,0].reshape((3,1))
    if Axis == 'y' or Axis == 'Y' or Axis == 2:
        Vector = R[:,1].reshape((3,1))
    if Axis == 'z' or Axis == 'Z' or Axis == 's' or Axis == 'S' or Axis == 3:
        Vector = R[:,2].reshape((3,1))
    check_vectors_valid([Vector])
    return Vector

def P_from_T(T): #Position vector is top right 3x1 of transformation matrix
    check_T_valid(T)
    return T[0:3,3].reshape((3,1))

def z_from_T(T):
    check_T_valid(T)
    return T[0:3,2].reshape((3,1))

def S_from_T(T):
    check_T_valid(T)
    return T[0:3,2].reshape((3,1))

def line_from_T(T, ReturnStacked = False):
    check_T_valid(T)
    P = P_from_T(T)
    S = z_from_T(T)
    SOL = vcross(P, S)
    if ReturnStacked:
        return vector_stack(S, SOL)
    else:
        return S, SOL
    

def T_from_RP(R,P): #Transformation matrix placing R to TL 3x3 and P to TR 3x1
    check_R_valid(R)
    check_vectors_valid([P])
    T = aligned_T()
    T[0:3,0:3] = R
    T[0:3,3] = P.reshape(3)
    return T
    
def R_from_axis_rotation(Axis, RotRad): #(2.38 - 2.40)
    if Axis == 'X' or Axis == 'x' or Axis == 0:
        R = np.array([[1, 0, 0],
                      [0, np.cos(RotRad), -np.sin(RotRad)],
                      [0, np.sin(RotRad), np.cos(RotRad)]])
    elif Axis == 'Y' or Axis == 'y' or Axis == 1:
        R = np.array([[np.cos(RotRad), 0, np.sin(RotRad)],
                      [0, 1, 0],
                      [-np.sin(RotRad), 0, np.cos(RotRad)]])
    elif Axis == 'Z' or Axis == 'z' or Axis == 2:
        R = np.array([[np.cos(RotRad), -np.sin(RotRad), 0],
                      [np.sin(RotRad), np.cos(RotRad), 0],
                      [0,0,1]])
    check_R_valid(R)
    return R

def P_from_PorigRP(Porig,R, P): #(2.14)
    check_R_valid(R)
    check_vectors_valid([Porig , P])
    NewP = np.add(Porig, np.matmul(R,P))
    check_vectors_valid(NewP)
    return NewP

def P_from_TP(T, P): #P vectors are never assumed homogeneous (2.32)
    check_T_valid(T)
    check_vectors_valid(P)
    NewP = np.matmul(T,P_to_homogeneous(P))[0:3].reshape((3,1))
    return NewP

def P_to_homogeneous(P): #(4,1) where top 3 are P, bottom is 1
    HP = np.array(np.ones((4,1)),dtype=float)
    HP[0:3,0] = P[0:3,0]
    return HP

def P_from_homogeneous(HP):
    P = HP[0:3,:]
    check_vectors_valid([P])
    return P

def R_from_origin_rotation(ZVector, RotRad): #(2.61), ZVector must be made unit
    check_vectors_valid(ZVector)
    ZVectorUnit = unit_vector(ZVector)
    mx = ZVectorUnit[0,0]
    my = ZVectorUnit[1,0]
    mz = ZVectorUnit[2,0]
    C = np.cos(RotRad)
    S = np.sin(RotRad)
    R = np.array([[(mx**2)*(1-C)+C,    mx*my*(1-C)-mz*S,   mx*mz*(1-C)+my*S],
               [mx*my*(1-C)+mz*S,   (my**2)*(1-C)+C,    my*mz*(1-C)-mx*S],
               [mx*mz*(1-C)-my*S ,  my*mz*(1-C)+mx*S,   (mz**2)*(1-C)+C]])
    check_R_valid(R)
    return R

def origin_rotation_from_R(R, sign='+'): #2.8.2, returns unit vector and angle 
    check_R_valid(R)
    RotRadCos = (R[0,0]+R[1,1]+R[2,2]-1)/2
    if sign == '+':
        RotRad = np.arccos(RotRadCos) #0<=RotRad<=180
    elif sign == '-':
        RotRad = -np.arccos(RotRadCos) #-180<=Rotrad<=0
    else:
        raise Exception('Invalid sign ({} or {}): {}'
                        .format(chr(43), chr(8722), sign))
    ZVector = np.array([[0.0],[0.0],[0.0]])
    from math import isclose
    if isclose(RotRadCos, 1.0, abs_tol = 0.0001):
        # the rotation angle is zero (no rotation)
        return ZVector, 0.0
    elif isclose(RotRadCos, -1.0, abs_tol = 0.0001):
        # the rotation angle is 180 degrees
        mx = np.sqrt((R[0,0]-RotRadCos)/(1-RotRadCos)) #(2.72)
        my = np.sqrt((R[1,1]-RotRadCos)/(1-RotRadCos)) #(2.73)
        mz = np.sqrt((R[2,2]-RotRadCos)/(1-RotRadCos)) #(2.74)
        RotRad = np.pi
    else:
        mx = (R[2, 1]-R[1, 2])/(2*np.sin(RotRad)) #(2.66)
        my = (R[0, 2]-R[2, 0])/(2*np.sin(RotRad)) #(2.67)
        mz = (R[1, 0]-R[0, 1])/(2*np.sin(RotRad)) #(2.68)
        
    ZVector = np.array([[mx],[my],[mz]])
    ZVector = unit_vector(ZVector)
    return ZVector, RotRad

def T_from_non_origin_rotation(APP, m, RotRad):
    check_vectors_valid([APP, m])
    m = unit_vector(m)
    AA1T = T_from_RP(aligned_R(), APP)
    A1A2R = R_from_origin_rotation(m, RotRad)
    A1A2T = T_from_RP(A1A2R, aligned_P())
    A2BT = T_from_RP(aligned_R(), -APP)
    ABT = np.matmul(np.matmul(AA1T, A1A2T), A2BT)
    return ABT

def T_from_robot_param(ai, alpharadij, Sij, thetaradij): #(3.6)
    cij = np.cos(thetaradij)
    sij = np.sin(thetaradij)
    ci = np.cos(alpharadij)
    si = np.sin(alpharadij)
    
    T = np.array([[cij,        -sij,        0,      ai],
                  [sij*ci,     cij*ci,     -si,   -si*Sij],
                  [sij*si,     cij*si,      ci,    ci*Sij],
                  [0,          0,           0,      1]])
    check_T_unit(T)
    return T
    
def inv_T(ABT): #(2.30)
    ABRT = R_from_T(ABT).T
    APB0 = P_from_T(ABT)
    NewP = -np.matmul(ABRT, APB0)
    BAT = aligned_T()
    BAT[0:3, 0:3] = ABRT
    BAT[0:3, 3] = NewP.reshape(3)
    check_T_unit(BAT)
    return BAT

def vcross(Vi, Vj): #np.cross only (1,3) vectors not (3,1), transpose is req.
    check_vectors_valid([Vi, Vj])
    return np.cross(Vi.T, Vj.T).T

def vdot(Vi, Vj): #np.vdot automatically squeezes (3,1) to (3,)
    check_vectors_valid([Vi, Vj])
    return np.vdot(Vi, Vj)

#%%

def angle(sin, cos): #np.arctan2 uses the sign of sin and cos for quadrant
    return np.arctan2(sin, cos)

def cij(Si, Sj): #(5.6)
    check_vectors_valid([Si, Sj])
    return vdot(Si, Sj)

def sij(Si, Sj, Aij): #(5.7)
    check_vectors_valid([Si, Sj, Aij])
    return vdot(vcross(Si, Sj), Aij)

def angleij(Si, Sj, Aij): #Find alphaij from vectors Si, Sj, ai
    check_vectors_valid([Si, Sj, Aij])
    cos = cij(Si, Sj)
    sin = sij(Si, Sj, Aij)
    return angle(sin, cos)

def cj(Aij, Ajk): #(5.8)
    check_vectors_valid([Aij, Ajk])
    return vdot(Aij, Ajk)

def sj(Sj, Aij, Ajk): #(5.9)
    check_vectors_valid([Sj, Aij, Ajk])
    return vdot(vcross(Aij, Ajk), Sj)

def anglej(Sj, Aij, Ajk): #Find thetaj from vectors Sj, ai, ajk
    check_vectors_valid([Sj, Aij, Ajk])
    cos = cj(Aij, Ajk)
    sin = sj(Sj, Aij, Ajk)
    return np.arctan2(sin, cos)

def close_the_loop(_6Ptool, FPtool, FS6, Fa67, a67, alpha67):
    check_vectors_valid([_6Ptool, FPtool, FS6, Fa67])
    check_unit_vector(FS6) #FS6 and Fa67 must be unit vectors
    check_unit_vector(Fa67)
    
    FS7 = vcross(Fa67, FS6) #(5.5)
    FS1 = np.array([[0],[0],[1]]) #FS1 aligned with fixed Z axis
    a71direction = 1 #Choice of Fa71, 1 = S7 to S1, -1 = S1 to S7
    #(5.10)
    Fa71 = vcross(FS7, FS1)/vector_length(vcross(FS7, FS1))*a71direction
    alpha71 = angleij(FS7, FS1, Fa71) #(5.11, 5.12)
    theta7 = anglej(FS7, Fa67, Fa71) #(5.13, 5.14)
    FX = np.array([[1],[0],[0]]) #Definition of fixed axes
    FY = np.array([[0],[1],[0]])
    FZ = np.array([[0],[0],[1]])
    gamma1 = anglej(FS1, Fa71, FX) #(5.15, 5.16)
    
    #(5.6)
    FP6OrigTerm1 = FPtool
    FP6OrigTerm2 = -vdot(_6Ptool, FX)*Fa67
    FP6OrigTerm3 = -vcross(vdot(_6Ptool, FY)*FS6, Fa67)
    FP6OrigTerm4 = -vdot(_6Ptool, FZ)*FS6
    
    FP6Orig = np.sum([FP6OrigTerm1, FP6OrigTerm2, 
                      FP6OrigTerm3, FP6OrigTerm4], axis = 0)
    
    #Special Case 1: S1 and S7 are parallel
    c71 = cij(FS7, FS1)
    s71 = sij(FS7, FS1, Fa71) 
    if round(c71, 3) == 1 or round(c71, 3) == -1:
        S7 = 0
        S1 = vdot(-FP6Orig, FS1)
        a71 = vector_length(-(np.add(FP6Orig, S1*FS1)))
        #Special Case 2: S1 and S7 are collinear
        if round(a71, 3) == 0:
            theta7 = 0
    else: #Normal Case
        S7 = vdot(vcross(FS1, FP6Orig), Fa71)/s71
        a71 = vdot(vcross(FP6Orig, FS1), FS7)/s71
        S1 = vdot(vcross(FP6Orig, FS7), Fa71) / s71

    return a71, S7, S1, alpha71, theta7, gamma1

def solve_trig(A, B, D):    #Returns radian angles theta that solve 
                            #A*cos(theta)+B*sin(theta)+D=0
    if A != 0 and B != 0: #Handles cases 1 and 2
        singamma = B / np.sqrt(A**2 + B**2) #(6.195)
        cosgamma = A / np.sqrt(A**2 + B**2) #(6.196)
        gamma = angle(singamma, cosgamma)
        thetaa =  np.arccos(-D / np.sqrt(A**2 + B**2)) + gamma #(6.199)
        thetab = -np.arccos(-D / np.sqrt(A**2 + B**2)) + gamma
    else: #Handles case 3
        thetaa = 0
        thetab = 0
    return np.array([thetaa, thetab])

def array_to_tex(Array, ArrayTexNameStr=None, Boxed = False):
    if ArrayTexNameStr==None:
        ArrayTexNameStr = ''
        
    if ArrayTexNameStr != '':
        ArrayTexNameStr = ArrayTexNameStr + '='
    
    S = chr(92)
    if Boxed == True:
        TexPrefix = S+'boxed{'+ArrayTexNameStr +'\left['+S+'begin{array}{c}\n'
        TexSuffix = S+'end{array}'+S+'right]}'
    else:
        TexPrefix = ArrayTexNameStr + '\left['+S+'begin{array}{c}\n'
        TexSuffix = S+'end{array}'+S+'right]'
    TexNewLine = S+S
    ConsoleNewLine = '\n'
    TexNewCol = ' & '
    
    TexOutput = TexPrefix
    for i in range(np.shape(Array)[0]):
        for j in range(np.shape(Array)[1]):
            Value = Array[i,j]
            try:
                ValueStr = str(Value)
            except:
                raise Exception('Cannot convert {} at ({},{}) to string'
                                .format(Value, i ,j))
            if j != 0:
                TexOutput = TexOutput + TexNewCol
            TexOutput = TexOutput + ValueStr
        if i != np.shape(Array)[0]-1:
            TexOutput = TexOutput + TexNewLine + ConsoleNewLine
    TexOutput = TexOutput + ConsoleNewLine + TexSuffix
    TexOutput = TexOutput.replace('.0 &', ' &')
    TexOutput = TexOutput.replace('.0'+TexNewLine, ' '+TexNewLine)
    TexOutput = TexOutput.replace('.0\n', ' \n')
    TexOutput = TexOutput.replace('-0 &', '0 &')
    TexOutput = TexOutput.replace('-0 '+TexNewLine, '0 '+TexNewLine)
    TexOutput = TexOutput.replace('-0\n', '0 \n')
    return TexOutput

def ExpandXYZ(Text, Links):
    for i in range(len(Text)):
        if Text[i:].isnumeric():
            Numbers = Text[i:]
            Prefix = Text[:i]
            break
        
    DirectionCount = 0
    for i in range(len(Numbers)-1):
        if (int(Numbers[i])%Links)<int(Numbers[i+1]):
            DirectionCount = DirectionCount + 1
        elif (int(Numbers[i])%Links)>int(Numbers[i+1]):
            DirectionCount = DirectionCount - 1
        else:
            raise Exception('Concecutive Numbers')
    
    if DirectionCount >= 0: 
        Direction = '+'
    elif DirectionCount < 0: 
        Direction = '-'        
    
    match Prefix:
        case 'x': Prefix = 'X'
        case 'y': Prefix = 'Y'
        case 'z': Prefix = 'Z'
        case 'xStar': Prefix = "Xstar"
        case 'xstar': Prefix = "Xstar"
        case 'XStar': Prefix = "Xstar"
        
    if len(Numbers) == 1:
        j = Numbers[0]
        i = str(((int(j)-1)-1)%Links+1)
        k = str(((int(j)+1)-1)%Links+1)
        match Prefix:
            case "X": Expanded = 'X'+j+' = s'+i+j+'*s'+j+''
            case "Y": Expanded = 'Y'+j+' = -(s'+j+k+'*c'+i+j+' + c'+j+k+'*s'+i+j+'*c'+j+')'
            case "Z": Expanded = 'Z'+j+' = c'+j+k+'*c'+i+j+' - s'+j+k+'*s'+i+j+'*c'+j+''
            case "BarX": Expanded = 'BarX'+j+' = s'+j+k+'*s'+j+''
            case "BarY": Expanded = 'BarY'+j+' = -(s'+i+j+'*c'+j+k+' + c'+i+j+'*s'+j+k+'*c'+j+')'
            case "BarZ": Expanded = 'BarZ'+j+' = c'+i+j+'*c'+j+k+' - s'+i+j+'*s'+j+k+'*c'+j+''
        return Expanded
    
    elif Direction == "+":
        FrontNumbers = Numbers[:len(Numbers)-1] #..ij
        LastNum = Numbers[len(Numbers)-1] #k
        LastNumPlusOne = str(((int(LastNum)+1)-1)%Links+1) #l            
        match Prefix:
            case "X": Expanded = 'X'+FrontNumbers+LastNum+' = X'+FrontNumbers+'*c'+LastNum+' - Y'+FrontNumbers+'*s'+LastNum+''
            case "Xstar": Expanded = 'Xstar'+FrontNumbers+LastNum+' = '+'X'+FrontNumbers+'*s'+LastNum+' + Y'+FrontNumbers+'*c'+LastNum+''
            case "Y": Expanded = 'Y'+FrontNumbers+LastNum+' = c'+LastNum+LastNumPlusOne+'*(X'+FrontNumbers+'*s'+LastNum+' + Y'+FrontNumbers+'*c'+LastNum+') - s'+LastNum+LastNumPlusOne+'*Z'+FrontNumbers+''
            case "Z": Expanded = 'Z'+FrontNumbers+LastNum+' = s'+LastNum+LastNumPlusOne+'*(X'+FrontNumbers+'*s'+LastNum+' + Y'+FrontNumbers+'*c'+LastNum+') + c'+LastNum+LastNumPlusOne+'*Z'+FrontNumbers+''
        return Expanded
    
    else: #reverse case
        FrontNumbers = Numbers[:len(Numbers)-1] #...kj
        FirstNum = Numbers[len(Numbers)-1] #i
        FirstNumMinusOne = str(((int(FirstNum)-1)-1)%Links+1) #h      
        
        if len(Numbers) == 2:
            match Prefix:
                case "X": Expanded = 'X'+FrontNumbers+FirstNum+' = BarX'+FrontNumbers+'*c'+FirstNum+' - BarY'+FrontNumbers+'*s'+FirstNum
                case "Xstar": Expanded = 'Xstar'+FrontNumbers+FirstNum+' = BarX'+FrontNumbers+'*s'+FirstNum+' + BarY'+FrontNumbers+'*c'+FirstNum
                case "Y": Expanded = 'Y'+FrontNumbers+FirstNum+' = c'+FirstNumMinusOne+FirstNum+'*(BarX'+FrontNumbers+'*s'+FirstNum+' + BarY'+FrontNumbers+'*c'+FirstNum+') - s'+FirstNumMinusOne+FirstNum+'*BarZ'+FrontNumbers+''
                case "Z": Expanded = 'Z'+FrontNumbers+FirstNum+' = s'+FirstNumMinusOne+FirstNum+'*(BarX'+FrontNumbers+'*s'+FirstNum+' + BarY'+FrontNumbers+'*c'+FirstNum+') + c'+FirstNumMinusOne+FirstNum+'*BarZ'+FrontNumbers+''
        else:
            match Prefix:
                case "X": Expanded = 'X'+FrontNumbers+FirstNum+' = X'+FrontNumbers+'*c'+FirstNum+' - Y'+FrontNumbers+'*s'+FirstNum+''
                case "Xstar": Expanded = 'Xstar'+FrontNumbers+FirstNum+' = X'+FrontNumbers+'*s'+FirstNum+' + Y'+FrontNumbers+'*c'+FirstNum+''
                case "Y": Expanded = 'Y'+FrontNumbers+FirstNum+' = c'+FirstNumMinusOne+FirstNum+'*(X'+FrontNumbers+'*s'+FirstNum+' + Y'+FrontNumbers+'*c'+FirstNum+') - s'+FirstNumMinusOne+FirstNum+'*Z'+FrontNumbers+''
                case "Z": Expanded = 'Z'+FrontNumbers+FirstNum+' = s'+FirstNumMinusOne+FirstNum+'*(X'+FrontNumbers+'*s'+FirstNum+' + Y'+FrontNumbers+'*c'+FirstNum+') + c'+FirstNumMinusOne+FirstNum+'*Z'+FrontNumbers+''        
        return Expanded
        
def vector_origin_to_perp_plane(DO, S):
    """return p"""
    p = -DO*S/(vdot(S,S)) #1.13
    check_vectors_valid(p)
    return p

def vector_origin_to_perp_line(S,SOL):
    """return p"""
    check_S_SOL_perp(S,SOL)
    p = vcross(S,SOL)/vdot(S,S) #1.59
    check_vectors_valid(p)
    return p

def vector_unique_perp_to_lines(Si,Sj):
    """return Aij"""
    check_vectors_valid([Si, Sj])
    Si = unit_vector(Si)
    Sj = unit_vector(Sj)
    Aij = vcross(Si, Sj)/vector_length(vcross(Si, Sj)) #(1.136)
    check_vectors_valid(Aij)
    return Aij

def twist_angle(Si, Sj, Aij):
    """return alphaijrad"""
    check_vectors_valid([Si, Sj, Aij])
    cos_alphaijrad = vdot(Si, Sj)
    sin_alphaijrad = vdot(vcross(Si, Sj), Aij)
    alphaijrad = angle(sin_alphaijrad, cos_alphaijrad)
    return alphaijrad

def unit_line(S,SOL):
    check_line_valid(S, SOL)
    VectorLength = vector_length(S)
    if np.round(VectorLength, 3) != 0:
        S = S/VectorLength
        SOL = SOL/VectorLength
        check_line_valid(S, SOL)
    return S, SOL

def check_line_valid(S, SOL):
    check_vectors_valid([S, SOL])
    DotProduct = np.round(vdot(S, SOL), 3)
    if DotProduct == 0:
        return True
    else:
        raise Exception('Line is not perpendicular, S dot SOL =',DotProduct)
        
def unit_plane(DO, S):
    """return DO, S"""
    check_vectors_valid([S])
    VectorLength = vector_length(S)
    S = S/VectorLength
    DO = DO/VectorLength
    return DO, S

def mutual_moment(Si, SOLi, Sj, SOLj):
    """return mutual moment scalar"""
    check_vectors_valid([Si, SOLi, Sj, SOLj])
    Si, SOLi = unit_line(Si, SOLi)
    Sj, SOLj = unit_line(Sj, SOLj)
    return vdot(Si, SOLj)+vdot(Sj, SOLi)

def link_length_from_lines_angle(Si, SOLi, Sj, SOLj, alphaijrad):
    """return link length scalar ai"""
    check_vectors_valid([Si, SOLi, Sj, SOLj])
    Si, SOLi = unit_line(Si, SOLi)
    Sj, SOLj = unit_line(Sj, SOLj)
    mm = mutual_moment(Si, SOLi, Sj, SOLj)
    ai = -mm/np.sin(alphaijrad)
    return ai


def point_from_line_link_length(SOLi, Sj, SOLj, Aij, ai):
    """return point rE1"""
    check_vectors_valid([SOLi, Sj, SOLj, Aij])
    Sj, SOLj = unit_line(Sj, SOLj)
    rEi = (vcross(SOLi,(SOLj-(vcross(ai*Aij,Sj)))))/(vdot(SOLi, Sj)) #(1.160)
    check_vectors_valid([rEi])
    return rEi

def point_closest_to_point_on_line(Si, SOLi, Pi):
    """return point r"""
    check_vectors_valid([Si, SOLi, Pi])
    return Pi+(vcross(Si, (SOLi-vcross(Pi, Si)))/vdot(Si,Si)) #1.127
    

def point_from_intersecting_lines(Si, SOLi, Sj, SOLj):
    """return point r"""
    check_vectors_valid([Si, SOLi, Sj, SOLj])
    Si, SOLi = unit_vector(Si, SOLi)
    Sj, SOLj = unit_vector(Sj, SOLj)
    r = vcross(SOLi, SOLj)/vdot(SOLi, Sj)
    return r

def point_from_intersecting_plane_and_line(Si, SOLi, DOj, Sj):
    """return point r"""
    check_vectors_valid([Si, SOLi, Sj])
    return vcross(Sj, SOLi) - (DOj*Si)/vdot(Sj, Si)

def point_from_point_plane(r, DO, S):
    check_vectors_valid([r, S])
    rp = r - (vdot(r,S)+DO)/(vdot(S,S))*S
    return rp

def line_from_intersecting_planes(DOi, Si, DOj, Sj):
    """return S3, SOL3"""
    check_vectors_valid([Si, Sj])
    S3 = vcross(Si, Sj)
    SOL3 = (-DOj)*Si-(-DOi)*Sj
    S3, SOL3 = unit_vector(S3, SOL3)
    check_line_valid(S3, SOL3)
    return S3, SOL3

def line_from_two_points(Pi, Pj):
    """return S1Unit, SOL1Unit"""
    check_vectors_valid([Pi, Pj])
    Si = Pj - Pi
    SOLi = vcross(Pj, Si)
    SiUnit, SOLiUnit = unit_vector(Si, SOLi)
    check_line_valid(SiUnit, SOLiUnit)
    return SiUnit, SOLiUnit

def plane_from_lines(Si, SOLi, Sj):
    """return DO, S
    plane coordinates = [DO;S]"""
    check_vectors_valid([Si, SOLi, Sj])
    S = vcross(Si, Sj)
    DO = -vdot(SOLi, Sj)
    DO, S = unit_plane(DO, S)
    return DO, S

def plane_from_point_and_line(r0, Si, SOLi):
    """return DO, S
    plane coordinates = [DO;S]"""
    check_vectors_valid([r0, Si, SOLi])
    DO = -vdot(r0, SOLi)
    S = SOLi - vcross(r0, Si)
    DO, S = unit_plane(DO, S)
    return DO, S

def force_from_magnitude_and_line(f, Si, SOLi):
    """return F, Mo
    
    force coordinates = [F, Mo]
    """
    check_vectors_valid([Si, SOLi])
    SiUnit, SOLiUnit = unit_line(Si, SOLi)
    F = f*SiUnit
    Mo = f*SOLiUnit
    return F, Mo

def force_magnitude_direction_from_force(F):
    """return f, S"""
    check_vectors_valid([F])
    f = vector_length(F)
    S = unit_vector(F)
    return f, S

def moment_vector_from_opposing_lines(Si, SOLi, Sj, SOLj, f):
    """return M"""
    check_line_valid(Si, SOLi)
    check_line_valid(Sj, SOLj)
    SiUnit, SOLiUnit = unit_line(Si, SOLi)
    SjUnit, SOLjUnit = unit_line(Sj, SOLj)
    M = f*(SOLiUnit + SOLjUnit)
    return M

def moment_magnitude_direction_from_moment_vector(M):
    """return m, Sm"""
    check_vectors_valid([M])
    m = vector_length(M)
    Sm = unit_vector(M)
    return m, Sm

def dyname_from_from_forces(ListOfForces):
    """
    ListOfForces = [[F1, Mo1],[F2, Mo2],...,[Fn, Mon]]
    
    return F, M0
    """
    F = np.array([[0],[0],[0]])
    M0 = np.array([[0],[0],[0]])
    for Force in ListOfForces:
        FNew = Force[0]
        MNew = Force[1]
        check_vectors_valid([FNew, MNew])
        F = F + FNew
        M0 = M0 + MNew
    return F, M0
        
def wrench_from_dyname(F, M0):
    """
    return F, Mt, Ma

    W = [f, Mt] + [0, Ma]
    """
    check_vectors_valid([F, M0])
    f, S = force_magnitude_direction_from_force(F)
    Ma = vdot(M0, S)*S
    Mt = M0-Ma
    return F, Mt, Ma

def dyname_from_wrench(W):
    """
    return F, M0
    """    
    F = W[0:3,0].reshape(3,1)
    M0 = W[3:6,0].reshape(3,1)
    check_vectors_valid([F, M0])
    return F, M0

def screw_from_wrench(F, M0=None, ReturnStacked=False):
    """
    return S, SO
    """
    # check_vectors_valid([F, Mt, Ma])
    # M0 = Mt + Ma
    if M0 is None:
        M0 = F[3:6, :]
        F = F[0:3, :]
        
        
    S = unit_vector(F)
    SO = M0/vector_length(F)
    if ReturnStacked:
        return vector_stack(S, SO)
    else:
        return S, SO

def wrench_from_screw_forcem(S, SO, f):
    """return F, Mt, Ma"""
    check_vectors_valid([S, SO])
    F = f*S
    M0=SO*vector_length(F)
    Ma = vdot(M0, S)*S
    Mt = M0-Ma
    return F, M0

def pitch_from_force_moment(f, m):
    if f != 0:
        h = m/f
        return h
    else:
        raise Exception('F cannot equal 0')
        return None

def pitch_from_wrench(F, M0=None):
    """
    return h
    """
    # check_vectors_valid([F, Mt, Ma])
    if M0 is None:
        M0 = F[3:6,:]
        F = F[0:3, :]
    h = vdot(F, M0)/vdot(F, F)
    return h
    
def pitch_from_screw(S, SO = None):
    """return h"""
    if SO is None:
        SO = S[3:6, :]
        S = S[0:3, :]
        
    check_vectors_valid([S, SO])
    h = vdot(S, SO)/vdot(S, S)
    return h

def line_from_screw(S, SO = None, ReturnStacked = False):
    """return S, SOL"""
    if SO is None:
        
        SO = S[3:6, :]
        S = S[0:3, :]
    
    check_vectors_valid([S, SO])
    h = pitch_from_screw(S, SO)
    SOL = SO - h*S
    check_line_valid(S, SOL)
    
    if ReturnStacked:
        return vector_stack(S, SOL)
    else:
        return S, SOL

def screw_from_line_pitch(S, SOL, h):
    """return S, SO"""
    check_line_valid(S, SOL)
    SO = SOL + h*S
    return S, SO
    

def translate_screw(BS, BSO, ABT):
    """return AS, ASO"""
    check_vectors_valid([BS, BSO])
    check_T_valid(ABT)
    ABR = R_from_T(ABT)
    APBO = P_from_T(ABT)
    AS = np.matmul(ABR, BS)
    ASO = np.matmul(ABR, BSO)+vcross(APBO, np.matmul(ABR, BS))
    check_vectors_valid([AS, ASO])
    return AS, ASO

def cylindroid_R(hi, hj, alphaijrad, aij):
    Numerator = aij**2+(hj-hi)**2
    Denominator = 4*(np.sin(alphaijrad))**2
    return np.sqrt(Numerator/Denominator)

def cylindroid_sigma(hi, hj, alphaijrad, aij):
    R = cylindroid_R(hi, hj, alphaijrad, aij)
    sigmaSin = (aij-(hj-hi)*(1/np.tan(alphaijrad)))/(2*R)
    sigmaCos = ((hj-hi)+aij*(1/np.tan(alphaijrad)))/(2*R)
    return angle(sigmaSin, sigmaCos)

def cylindroid_psi(f, fi, fj, alphaijrad):
    sin_psi = (fj/f)*np.sin(alphaijrad)
    cos_psi = ((fi/f)*np.sin(alphaijrad)+np.cos(alphaijrad)*sin_psi)/np.sin(alphaijrad)
    psi = angle(sin_psi, cos_psi)
    return psi


def pitch_from_velocity(Omegaij, VOij = None):
    if VOij is None:
        VOij = Omegaij[3:6, :]
        Omegaij = Omegaij[0:3, :]
    
    check_vectors_valid([Omegaij, VOij])
    h = vdot(Omegaij, VOij)/vdot(Omegaij, Omegaij)
    return h

    

def line_from_velocity(Omegaij, VOij = None, ReturnStacked = False):
    if VOij is None:
        VOij = Omegaij[3:6, :]
        Omegaij = Omegaij[0:3, :]
    
    check_vectors_valid([Omegaij, VOij])
    
    h = pitch_from_velocity(Omegaij, VOij)
    omegaij = vector_length(Omegaij)
    
    S = Omegaij/omegaij
    SOL = (VOij - h*Omegaij)/omegaij
    check_line_valid(S, SOL)
    
    if ReturnStacked:
        return vector_stack(S, SOL)
    else:
        return S, SOL

# def vector_to_string(V,VectorName,Underbar=False):
def vector_to_letter_string(V):
    check_vectors_valid(V)
    # if Underbar: 
    #     OutputString = r'\underbar '+VectorName+'='
    #     Axes = [r'\underbar i',r'\underbar j',r'\underbar k']
    # else: 
        # OutputString = VectorName+'='
    OutputString = ''
    Axes = ['i','j','k']
    
    for Count, Value in enumerate(V):
        Sign = ''
        if Count > 0:
            if Value>=0 or Value[0].round(4) == '0.0': Sign = '+'
        OutputString = OutputString + Sign + str(Value[0].round(4)) + Axes[Count]
    return OutputString
    
def array_to_string(Array):
    return sanitize_string(str([np.round(float(v),3) for v in Array])[1:-1])

def line_to_string(Si, SOLi):
    check_vectors_valid([Si, SOLi])
    return sanitize_string('{ '+array_to_string(np.round(Si,3))+' ; '+array_to_string(np.round(SOLi,3))+' }')

def dyname_to_string(F, M0):
    check_vectors_valid([F, M0])
    return sanitize_string('{ '+array_to_string(np.round(F, 3))+' ; '+array_to_string(np.round(M0, 3))+' }')

def wrench_to_string(wF, wM0 = None):
    return screw_to_string(Si = wF, SOi = wM0)

def screw_to_string(Si, SOi = None):
    if SOi is None:
        return sanitize_string('{ '+array_to_string(np.round(Si[0:3], 3))+' ; '+array_to_string(np.round(Si[3:6], 3))+' }')
    else:
        check_vectors_valid([Si, SOi])
        return sanitize_string('{ '+array_to_string(np.round(Si, 3))+' ; '+array_to_string(np.round(SOi, 3))+' }')

def sanitize_string(String):
    String = String.replace('-0.0,','0')
    String = String.replace('-0.0 ','0 ')
    String = String.replace('.0,',',')
    String = String.replace('.0 ',' ')
    return String

def vector_stack(V1, V2):
    check_vectors_valid([V1, V2])
    return np.vstack([V1, V2])

def vector_split(Vector):
    V1 = Vector[0:3,:]
    V2 = Vector[3:6,:]
    check_vectors_valid([V1, V2])
    return V1, V2