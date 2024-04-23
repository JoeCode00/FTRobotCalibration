# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:31:29 2024

@author: Joe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
# from mpl_toolkits import mplot3d 
from ForwardKinematics import forward_kinematics
import src.Robots2 as R2

def Fig1():
    # breakpoint()
    x = ExcelData['Probe PX']
    y = ExcelData['Probe PY']
    z = ExcelData['Probe PZ']
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    
    base = 30
    
    XMax = roundmultiple(np.max(x), base=base, direction='LargerMag')
    XMin = roundmultiple(np.min(x), base=base, direction='SmallerMag')
    YMax = roundmultiple(np.max(y), base=base, direction='LargerMag')
    YMin = roundmultiple(np.min(y), base=base, direction='SmallerMag')
    ZMax = roundmultiple(np.max(z), base=base, direction='LargerMag')
    ZMin = 0
    
    XCount = int((XMax-XMin)/base)+1
    YCount = int((YMax-YMin)/base)+1
    ZCount = int((ZMax-ZMin)/base)+1
    
    XTicks = np.linspace(XMin, XMax, XCount)
    YTicks = np.linspace(YMin, YMax, YCount)
    ZTicks = np.linspace(ZMin, ZMax, ZCount)
    
    ax.set_box_aspect((np.ptp(XTicks), np.ptp(YTicks), np.ptp(ZTicks)))
    
    triang = mtri.Triangulation(x, y)
    ax.plot_trisurf(triang, z, cmap='jet')
    ax.scatter(x,y,z, marker='.', s=10, c="black", alpha=0.5)
    ax.view_init(elev=60, azim=-45)
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    
    ax.xaxis.set_ticks(XTicks)
    ax.yaxis.set_ticks(YTicks)
    ax.zaxis.set_ticks(ZTicks)
    
    XTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(XTicks)]
    YTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(YTicks)]
    ZTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(ZTicks)]
    
    ax.xaxis.set_ticklabels(XTickLabels)
    ax.yaxis.set_ticklabels(YTickLabels)
    ax.zaxis.set_ticklabels(ZTickLabels)
    ax.set_title('Probe Points XYZ')
    
def Fig2():
    # breakpoint()
    x = ExcelData['Probe PX']
    y = ExcelData['Probe PY']
    z = ExcelData['Probe PZ']
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    
    base = 30
    
    XMax = roundmultiple(np.max(x), base=base, direction='LargerMag')
    XMin = roundmultiple(np.min(x), base=base, direction='SmallerMag')
    YMax = roundmultiple(np.max(y), base=base, direction='LargerMag')
    YMin = roundmultiple(np.min(y), base=base, direction='SmallerMag')
    ZMax = roundmultiple(np.max(z), base=1, direction='LargerMag')
    ZMin = roundmultiple(np.min(z), base=1, direction='SmallerMag')
    
    XCount = int((XMax-XMin)/base)+1
    YCount = int((YMax-YMin)/base)+1
    ZCount = 30
    
    XTicks = np.linspace(XMin, XMax, XCount)
    YTicks = np.linspace(YMin, YMax, YCount)
    ZTicks = np.linspace(ZMin, ZMax, ZCount)
    
    # ax.set_box_aspect((np.ptp(XTicks), np.ptp(YTicks), np.ptp(ZTicks)))
    
    triang = mtri.Triangulation(x, y)
    ax.plot_trisurf(triang, z, cmap='jet')
    ax.scatter(x,y,z, marker='.', s=10, c="black", alpha=0.5)
    ax.view_init(elev=60, azim=-45)
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    
    ax.xaxis.set_ticks(XTicks)
    ax.yaxis.set_ticks(YTicks)
    ax.zaxis.set_ticks(ZTicks)
    
    XTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(XTicks)]
    YTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(YTicks)]
    ZTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(ZTicks)]
    
    ax.xaxis.set_ticklabels(XTickLabels)
    ax.yaxis.set_ticklabels(YTickLabels)
    ax.zaxis.set_ticklabels(ZTickLabels)
    ax.set_title('Probe Points Scaled Z')
    
def Fig3():
    # breakpoint()
    x = ExcelData['Probe PX']
    y = ExcelData['Probe PY']
    z = ExcelData['Probe PZ']
    
    xPlane = ExcelData['Plane PX']
    yPlane = ExcelData['Plane PY']
    zPlane = ExcelData['Plane PZ']
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    
    base = 30
    
    XMax = roundmultiple(np.max(x), base=base, direction='LargerMag')
    XMin = roundmultiple(np.min(x), base=base, direction='SmallerMag')
    YMax = roundmultiple(np.max(y), base=base, direction='LargerMag')
    YMin = roundmultiple(np.min(y), base=base, direction='SmallerMag')
    ZMax = roundmultiple(np.max(z), base=1, direction='LargerMag')
    ZMin = roundmultiple(np.min(z), base=1, direction='SmallerMag')
    
    XCount = int((XMax-XMin)/base)+1
    YCount = int((YMax-YMin)/base)+1
    ZCount = 30
    
    XTicks = np.linspace(XMin, XMax, XCount)
    YTicks = np.linspace(YMin, YMax, YCount)
    ZTicks = np.linspace(ZMin, ZMax, ZCount)
    
    # ax.set_box_aspect((np.ptp(XTicks), np.ptp(YTicks), np.ptp(ZTicks)))
    # breakpoint()
    triang = mtri.Triangulation(xPlane, yPlane)
    ax.plot_trisurf(triang, zPlane, color=[0,0,1,0.5])
    ax.scatter(x,y,z, marker='.', s=10, c="black", alpha=0.5)
    ax.view_init(elev=-6, azim=6)
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    
    ax.xaxis.set_ticks(XTicks)
    ax.yaxis.set_ticks(YTicks)
    ax.zaxis.set_ticks(ZTicks)
    
    XTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(XTicks)]
    YTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(YTicks)]
    ZTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(ZTicks)]
    
    ax.xaxis.set_ticklabels(XTickLabels)
    ax.yaxis.set_ticklabels(YTickLabels)
    ax.zaxis.set_ticklabels(ZTickLabels)
    ax.set_title('Probe Points Best Fit Plane')
    
def Fig4():
    # breakpoint()
    x = ExcelData['Probe PX']
    y = ExcelData['Probe PY']
    z = ExcelData['Plane Delta']

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    
    base = 30
    
    XMax = roundmultiple(np.max(x), base=base, direction='LargerMag')
    XMin = roundmultiple(np.min(x), base=base, direction='SmallerMag')
    YMax = roundmultiple(np.max(y), base=base, direction='LargerMag')
    YMin = roundmultiple(np.min(y), base=base, direction='SmallerMag')
    ZMax = np.max(z)
    ZMin = np.min(z)
    
    XCount = int((XMax-XMin)/base)+1
    YCount = int((YMax-YMin)/base)+1
    ZCount = 30
    
    XTicks = np.linspace(XMin, XMax, XCount)
    YTicks = np.linspace(YMin, YMax, YCount)
    ZTicks = np.linspace(ZMin, ZMax, ZCount)
    
    # ax.set_box_aspect((np.ptp(XTicks), np.ptp(YTicks), np.ptp(ZTicks)))
    # breakpoint()
    triang = mtri.Triangulation(x, y)
    
    colorlist = ['orange' if zvalue>=0 else 'blue' for zvalue in z]
    # ax.plot_trisurf(triang, zPlane, color=[0,0,1,0.5])
    ax.bar3d(x,y,np.zeros(len(z)), 10,10,z, color=colorlist, alpha=0.5)
    ax.view_init(elev=30, azim=-150)
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Distance to Plane (mm)')
    
    ax.xaxis.set_ticks(XTicks)
    ax.yaxis.set_ticks(YTicks)
    ax.zaxis.set_ticks(ZTicks)
    
    XTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(XTicks)]
    YTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(YTicks)]
    ZTickLabels = [str(np.round(s,3)) if (index%2==0 or s==0) else '' for index, s in enumerate(ZTicks)]
    
    ax.xaxis.set_ticklabels(XTickLabels)
    ax.yaxis.set_ticklabels(YTickLabels)
    ax.zaxis.set_ticklabels(ZTickLabels)
    ax.set_title('Distance To Best Fit Plane')
    
def Fig5():
    # breakpoint()
    x = ExcelData['Probe PX']
    y = ExcelData['Probe PY']
    z = ExcelData['Probe PZ']
    
    xPlane = ExcelData['Plane PX']
    yPlane = ExcelData['Plane PY']
    zPlane = ExcelData['Plane PZ']
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    
    base = 30
    
    XMax = roundmultiple(np.max(x), base=base, direction='LargerMag')
    XMin = roundmultiple(np.min(x), base=base, direction='SmallerMag')
    YMax = roundmultiple(np.max(y), base=base, direction='LargerMag')
    YMin = roundmultiple(np.min(y), base=base, direction='SmallerMag')
    ZMax = roundmultiple(np.max(z), base=base, direction='LargerMag')
    ZMin = 0
    
    XCount = int((XMax-XMin)/base)+1
    YCount = int((YMax-YMin)/base)+1
    ZCount = int((ZMax-ZMin)/base)+1
    
    XTicks = np.linspace(XMin, XMax, XCount)
    YTicks = np.linspace(YMin, YMax, YCount)
    ZTicks = np.linspace(ZMin, ZMax, ZCount)
    
    ax.set_box_aspect((np.ptp(XTicks), np.ptp(YTicks), np.ptp(ZTicks)))
    # breakpoint()
    triang = mtri.Triangulation(xPlane, yPlane)
    ax.plot_trisurf(triang, zPlane, color=[0,0,1,0.5])
    ax.scatter(x,y,z, marker='.', s=10, c="black", alpha=0.5)
    ax.view_init(elev=33, azim=-30)
    
    
    
    import matplotlib as mpl
    
    for Index in ExcelData.index.values:
        if Index%5 == 0:
            ProbePoint = ExcelData.loc[Index,['Probe PX', 'Probe PY', 'Probe PZ']].to_numpy(dtype='f').reshape(3,1)
            ForceS = ExcelData.loc[Index,['Fixed Force SX', 'Fixed Force SY', 'Fixed Force SZ']].to_numpy(dtype='f').reshape(3,1)
            FixedForceMagnitude = ExcelData.loc[Index,'Fixed Force Magnitude']
            DirectionPoint = ProbePoint+ForceS*FixedForceMagnitude*75
            ax.plot([ProbePoint[0,0], DirectionPoint[0,0]], [ProbePoint[1,0], DirectionPoint[1,0]], zs=[ProbePoint[2,0], DirectionPoint[2,0]], linewidth=1.5, color=mpl.colormaps['viridis']((FixedForceMagnitude-ExcelData['Fixed Force Magnitude'].min())/(ExcelData['Fixed Force Magnitude'].max()-ExcelData['Fixed Force Magnitude'].min())))
    
    # Normalizer 
    cmap = plt.get_cmap('viridis')
    norm = mpl.colors.Normalize(vmin=ExcelData['Fixed Force Magnitude'].min(), vmax=ExcelData['Fixed Force Magnitude'].max()) 
      
    # creating ScalarMappable 
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm) 
    sm.set_array([]) 
    plt.colorbar(sm, label='Force Magnitude (N)') 
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    
    ax.xaxis.set_ticks(XTicks)
    ax.yaxis.set_ticks(YTicks)
    ax.zaxis.set_ticks(ZTicks)
    
    XTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(XTicks)]
    YTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(YTicks)]
    ZTickLabels = [str(int(s)) if (index%2==0 or s==0) else '' for index, s in enumerate(ZTicks)]
    
    # breakpoint()
    ax.xaxis.set_ticklabels(XTickLabels)
    ax.yaxis.set_ticklabels(YTickLabels)
    ax.zaxis.set_ticklabels(ZTickLabels)
    ax.set_title('Force Vector in Fixed Frame')

def roundmultiple(x, base=5, direction=None):
    if direction is not None:
        direction = direction.lower()
    
    if direction == 'largermag':
        if x >= 0: direction = 'up'
        else: direction = 'down'
    elif direction == 'smallermag':
        if x >= 0: direction = 'down'
        else: direction = 'up'
    
    if direction == 'up' or direction == 'ceil':
        return base * np.ceil(x/base)
    elif direction == 'down' or direction == 'floor':
        return base * np.floor(x/base)
    else:
        return base * round(x/base)
    
ExcelData = pd.read_excel('O:\OneDrive - University of Florida\Research\Data\InputData.xlsx')

ExcelData[['Log TX','Log TY', 'Log TZ']] = ExcelData[['Log TX','Log TY', 'Log TZ']]/1000

ExcelData[['Probe PX','Probe PY', 'Probe PZ']] = 0
for Index in ExcelData.index.values:
    # VectorTool0 = [ExcelData.loc[Index, 'Log PX'], 
    #                ExcelData.loc[Index, 'Log PY'],
    #                ExcelData.loc[Index, 'Log PZ']]
    ThetaList = [ExcelData.loc[Index, 'Log Theta 1'],
                 ExcelData.loc[Index, 'Log Theta 2'],
                 ExcelData.loc[Index, 'Log Theta 3'],
                 ExcelData.loc[Index, 'Log Theta 4'],
                 ExcelData.loc[Index, 'Log Theta 5'],
                 ExcelData.loc[Index, 'Log Theta 6'],]
    
    T0j, Tij = forward_kinematics(ThetaList)
    P0Probe = R2.P_from_T(T0j[7])[:,0]

    ExcelData.loc[Index,'Probe PX'] = P0Probe[0]
    ExcelData.loc[Index,'Probe PY'] = P0Probe[1]
    ExcelData.loc[Index,'Probe PZ'] = P0Probe[2]
    
A = ExcelData[['Probe PX', 'Probe PY', 'Probe PZ']].to_numpy()
B = -np.ones(A.shape[0]).T
HatX = np.matmul(np.matmul(np.linalg.inv(np.matmul(A.T,A)), A.T), B).reshape(3,1)
HatXMagnitude = R2.vector_length(HatX)
UnitHatX = HatX/HatXMagnitude
PlaneDO = 1/HatXMagnitude

ExcelData[['Plane PX', 
           'Plane PY', 
           'Plane PZ', 
           'Plane Delta', 
           'Fixed Force SX', 
           'Fixed Force SY', 
           'Fixed Force SZ',
           'Fixed Force Magnitude',
           'Fixed Moment SOLX',
           'Fixed Moment SOLY',
           'Fixed Moment SOLZ',
           'Fixed Moment Magnitude']] = 0

for Index in ExcelData.index.values:
    ProbePoint = ExcelData.loc[Index,['Probe PX', 'Probe PY', 'Probe PZ']].to_numpy(dtype='f').reshape(3,1)
    PlanePoint = R2.point_from_point_plane(ProbePoint, PlaneDO, UnitHatX)
    PlaneX, PlaneY, PlaneZ = PlanePoint[:,0].tolist()
    ExcelData.loc[Index,'Plane PX'] = PlaneX
    ExcelData.loc[Index,'Plane PY'] = PlaneY
    ExcelData.loc[Index,'Plane PZ'] = PlaneZ
    DeltaVector = PlanePoint - ProbePoint
    DeltaX, DeltaY, DeltaZ = DeltaVector[:,0].tolist()
    Delta = np.sqrt(DeltaX**2 + DeltaY**2 + DeltaZ**2)
    
    if DeltaZ < 0:
        Delta = -Delta
    ExcelData.loc[Index,'Plane Delta'] = Delta
    
    FTOrigin = R2.P_from_T(T0j[6])
    FTForceVector = ExcelData.loc[Index,['Log FX', 'Log FY', 'Log FZ']].to_numpy(dtype='f').reshape(3,1)
    FTForceS = R2.unit_vector(FTForceVector)
    
    
    FixedForceVector = np.matmul(R2.R_from_T(T0j[6]),FTForceS)
    SFixedForceX, SFixedForceY, SFixedForceZ = FixedForceVector[:,0].tolist()
    FixedForceMagnitude = R2.vector_length(FTForceVector)
    FixedForceSOL = R2.vcross(FTOrigin, FTForceS)
    
    FixedMomentS = np.array([[0],[0],[0]])
    FixedMomentSOL = ExcelData.loc[Index,['Log TX', 'Log TY', 'Log TZ']].to_numpy(dtype='f').reshape(3,1)
    
    FixedMoment = FixedForceSOL + FixedMomentSOL
    
    FixedMomentMagnitude = R2.vector_length(FixedMoment)
    SOLFixedMomentX, SOLFixedMomentY, SOLFixedMomentZ = FixedMoment[:,0].tolist()
    
    ExcelData.loc[Index,'Fixed Force SX'] = SFixedForceX
    ExcelData.loc[Index,'Fixed Force SY'] = SFixedForceY
    ExcelData.loc[Index,'Fixed Force SZ'] = SFixedForceZ
    ExcelData.loc[Index,'Fixed Force Magnitude'] = FixedForceMagnitude
    ExcelData.loc[Index,'Fixed Moment SOLX'] = SOLFixedMomentX
    ExcelData.loc[Index,'Fixed Moment SOLY'] = SOLFixedMomentY
    ExcelData.loc[Index,'Fixed Moment SOLZ'] = SOLFixedMomentZ
    ExcelData.loc[Index,'Fixed Moment Magnitude'] = FixedMomentMagnitude
    
Fig5()
Fig4()
Fig3()
Fig2()
Fig1()

plt.show()