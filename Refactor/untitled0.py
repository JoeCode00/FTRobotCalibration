import numpy as np
from InverseKinematics import inverse_kinematics
PositionVectorR = np.array([ ])
FTZR = np.array([])
FTXR = np.array([0.707,0.707,0])

v_FPtool    = PositionVectorR
v_FS6       = FTZR
v_Fa67      = FTXR

breakpoint()
inverse_kinematics(v_FPtool, v_FS6, v_Fa67)