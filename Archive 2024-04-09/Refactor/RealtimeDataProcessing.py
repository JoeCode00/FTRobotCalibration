from datetime import datetime
import numpy as np
import struct
import dearpygui.dearpygui as dpg
from InputJointAngles import input_joint_angles
from RobotCommunications import must_get_robot_state
# from GrandCentralDispatch import grand_central_dispatch

def process_FT_data(FTData, NewFTData, SensorConnected, CountsPerForceAndTorque):
    FTData = np.roll(FTData, 1, axis=0)
    FTData[0,0,:] = datetime.now()
    for i in range(0,6,1):
        if SensorConnected:
            FTData[0,i+1,0] = int.from_bytes(NewFTData[12+i*4:15+i*4],
                                            'big',signed=True
                                            )/CountsPerForceAndTorque*256
        else:
            FTData[0,i+1,0] = list(struct.unpack('>ffffff',NewFTData))[i]
    for Row in range(FTData.shape[0]-1):
        if FTData[Row,0,0] != 0:
            FTData[Row,7,0] = (FTData[Row,0,0] - datetime.now()).total_seconds()
    return FTData

def FT_graph_updater(FTData):
    dpg.set_value('Force VS Time X Line', [FTData[:,7,0].tolist(), FTData[:,1,0].tolist()])
    dpg.set_value('Force VS Time Y Line', [FTData[:,7,0].tolist(), FTData[:,2,0].tolist()])
    dpg.set_value('Force VS Time Z Line', [FTData[:,7,0].tolist(), FTData[:,3,0].tolist()])
    dpg.set_value('Torque VS Time X Line', [FTData[:,7,0].tolist(), FTData[:,4,0].tolist()])
    dpg.set_value('Torque VS Time Y Line', [FTData[:,7,0].tolist(), FTData[:,5,0].tolist()])
    dpg.set_value('Torque VS Time Z Line', [FTData[:,7,0].tolist(), FTData[:,6,0].tolist()])
    dpg.set_value('Force Y VS Force X Line', [FTData[:,1,0].tolist(), FTData[:,2,0].tolist()])
    dpg.set_value('Torque Y VS Torque X Line', [FTData[:,4,0].tolist(), FTData[:,5,0].tolist()])
    dpg.set_value('Force Y VS Force X Marker', [[FTData[0,1,0]], [FTData[0,2,0]]])
    dpg.set_value('Torque Y VS Torque X Marker', [[FTData[0,4,0]], [FTData[0,5,0]]])
    
def bias_robot_vector(sender, Log = True):
    VectorName = sender[12:]
    
    if VectorName == '':
        VectorNameList = ['PX', 'PY', 'PZ',
                          'FTX X', 'FTX Y', 'FTX Z',
                          'FTZ X', 'FTZ Y', 'FTZ Z']
    else:
        VectorNameList = [VectorName]
    
    for VectorName in VectorNameList:
        RobotData = dpg.get_value('Robot '+VectorName)
        dpg.set_value('Input '+VectorName, RobotData)    
    
def robot_state_delta_updater(StateValueR, ErrorValueR, PositionVectorR, FTZR, FTXR):
    if StateValueR is not None:
        dpg.set_value('Robot State Value', StateValueR)
    if ErrorValueR is not None:
        dpg.set_value('Robot Error Value', ErrorValueR)
    PositionVectorS, FTZS, FTXS = input_joint_angles()
    for PrefixSet in [['P', PositionVectorR, PositionVectorS], 
                      ['FTX ', FTXR, FTXS], 
                      ['FTZ ', FTZR, FTZS]]:
        for AxisSet in [['X', 0],
                        ['Y', 1], 
                        ['Z',2]]:
            VectorName = PrefixSet[0]+AxisSet[0]
            if PrefixSet[1] is not None:
                RobotValue = PrefixSet[1][AxisSet[1]]
                dpg.set_value('Robot '+VectorName, RobotValue)
            else:
                RobotValue = dpg.get_value('Robot '+VectorName)
            if PrefixSet[2] is not None:
                SendingValue = PrefixSet[2][AxisSet[1]]
                DeltaValue = SendingValue - RobotValue
                dpg.set_value('Delta '+VectorName, DeltaValue)

def MakeSamplingButtons(SafePositionGridAndNames, UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize):
    ColumnWidth = dpg.get_item_width('Sampling Control')/SafePositionGridAndNames.shape[0]*0.95
    RowHeight = dpg.get_item_height('Sampling Control')/1.5/SafePositionGridAndNames.shape[1]*0.95
    with dpg.group(parent = 'Sampling Goto Buttons', tag='Sampling Button Container'):
        for YPoint in range(SafePositionGridAndNames.shape[1]-1,-1,-1): 
            with dpg.group(horizontal=True, height=RowHeight):
                for XPoint in range(SafePositionGridAndNames.shape[0]):
                    sampling_button_helper(SafePositionGridAndNames, XPoint, YPoint, ColumnWidth, UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)

def sampling_button_helper(SafePositionGridAndNames, XPoint, YPoint, ColumnWidth, UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize):
    SafeXCoordsmm = SafePositionGridAndNames[XPoint, YPoint, 0]
    SafeYCoordsmm = SafePositionGridAndNames[XPoint, YPoint, 1]
    SafeZCoordsmm = SafePositionGridAndNames[XPoint, YPoint, 2]
    PointName = SafePositionGridAndNames[XPoint, YPoint, 3]
    ButtonTag = SafePositionGridAndNames[XPoint, YPoint, 4]
    PointNumber = SafePositionGridAndNames[XPoint, YPoint, 5]

    
    with dpg.child_window(width=ColumnWidth):
        dpg.add_button(label=PointName, tag=ButtonTag, 
                        callback= lambda: sampling_button_callback(ButtonTag, SafePositionGridAndNames, None, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize),
                       )
        # with dpg.tree_node(label="Combo"):
        dpg.add_combo(['Not Taken','Taken'], default_value='Not Taken', tag=ButtonTag+" Taken")
        # dpg.add_text('Not Taken', tag=ButtonTag+" Taken")
        
def sampling_button_callback(sender, app_data, user_data, UDPRobotClientSocket=None, RobotServerAddressPort=None, RobotServerBufferSize=None):
    SampleXYIndexes = [int(e) for e in sender[8:].split(',')]
    SafePositionGridAndNames = app_data
    SafeCoordinates = np.array(SafePositionGridAndNames[SampleXYIndexes[0], SampleXYIndexes[1], 0:3]).reshape((3,)).tolist()
    # SafeXCoordsmm = SafeCoordinates[0]
    # SafeYCoordsmm = SafeCoordinates[1]
    # SafeZCoordsmm = SafeCoordinates[2]
    MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = must_get_robot_state(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
    
    VectorNameList = ['PX', 'PY', 'PZ']
    for AxisIndex, VectorName in enumerate(VectorNameList):
        dpg.set_value('Input '+VectorName, SafeCoordinates[AxisIndex])
    robot_state_delta_updater(StateValueR, ErrorValueR, PositionVectorR, FTZR, FTXR)

# def recent_FT_data_chunk(FTData, HistorySeconds):
#     # breakpoint()
#     FTDataRecentHistory = None
#     FTDataRecentHistoryIsNew = True
#     RecentDataFinding = True
    
#     NowDateTime = datetime.now()
#     breakpoint()
#     for Row in range(FTData.shape[0]-1,0,-1):
#             RecordDateTime = FTData[Row,0,0]
#             TimeGap = NowDateTime - RecordDateTime
            
#             if TimeGap < timedelta(seconds = HistorySeconds):
#                 if FTDataRecentHistoryIsNew:
#                     FTDataRecentHistoryIsNew = False
#                     FTDataRecentHistory = np.array(np.zeros((1,8,2)), dtype = object)
#                     FTDataRecentHistory[0,0:7,:] = FTData[Row,:,:]
#                     FTDataRecentHistory[0,7,:] = -TimeGap.total_seconds()
                    
#                 else:
#                     # AddTimeGap = np.append()
#                     FTDataRecentHistory = np.append(FTDataRecentHistory, np.array(np.zeros((1,8,2)), dtype = object), axis = 0)
#                     FTDataRecentHistory[FTDataRecentHistory.shape[0]-1,0:7,:] = FTData[Row,:,:]
#                     FTDataRecentHistory[FTDataRecentHistory.shape[0]-1,7,:] = -TimeGap.total_seconds()
#             else: 
#                 continue
#     return FTDataRecentHistory