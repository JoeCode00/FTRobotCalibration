from InputJointAngles import input_joint_angles 
from InputStateErrorValues import input_state_error_values
from RobotCommunications import send_robot_data, query_robot_state, must_get_robot_state
import dearpygui.dearpygui as dpg
from datetime import datetime
import numpy as np
from RealtimeDataProcessing import bias_robot_vector, robot_state_delta_updater, MakeSamplingButtons
import struct
from SurfaceSampling import safe_position_grid_and_names
from RobotCommunications import must_get_robot_state
# from GrandCentralDispatch import info

def grand_central_dispatch(sender, app_data, user_data, UDPRobotClientSocket=None, RobotServerAddressPort=None, RobotServerBufferSize=None):
    # breakpoint()
    
    if sender[:11] == 'Bias Vector':
        bias_robot_vector(sender)
        
    elif sender[:5] == 'Input':
        query_robot_state(UDPRobotClientSocket, RobotServerAddressPort)
        
    elif sender[:16] == 'Immediate Z Move':
        # breakpoint()
        if sender == 'Immediate Z Move Up':
            Direction = 1
        elif sender == 'Immediate Z Move Down':
            Direction = -1
        
        CommandedVector = dpg.get_value('Immediate Z Move Step')*Direction
        PositionVectorS, FTZS, FTXS = input_joint_angles()
        PositionVectorSZ = PositionVectorS[2]
        NewZValue = PositionVectorSZ + CommandedVector
        
        dpg.set_value('Input '+'PZ', NewZValue)
        PositionVectorS, FTZS, FTXS = input_joint_angles()
        MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = must_get_robot_state(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
        robot_state_delta_updater(StateValueR, ErrorValueR, PositionVectorR, FTZR, FTXR)
        send_robot_data(UDPRobotClientSocket, RobotServerAddressPort)
        info(sender=sender, app_data='Sent')

    elif sender[:8] == 'Sampling':
        if sender == 'Sampling Set Safe Origin':
            MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = must_get_robot_state(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
            SafePositionGridAndNames = safe_position_grid_and_names(PositionVectorR)
            dpg.delete_item('Sampling Button Container')
            MakeSamplingButtons(SafePositionGridAndNames, UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)

        
    else:
        match sender:
            case 'ESTOP':
                StateValueS, ErrorValueS = input_state_error_values()
                StateValueS = 1
                PositionVectorS, FTZS, FTXS = input_joint_angles()
                MagicNumberS = 0xFF00AA55
                # RobotBytesToSend = struct.pack('Qiiddddddddd', 
                #                         MagicNumberS,
                #                         StateValueS,
                #                         ErrorValueS,
                #                         PositionVectorS[0], PositionVectorS[1], PositionVectorS[2],
                #                         FTZS[0], FTZS[1], FTZS[2],
                #                         FTXS[0], FTXS[1], FTXS[2],
                #                         )
                # UDPRobotClientSocket.sendto(RobotBytesToSend, RobotServerAddressPort)
                info(sender=sender, app_data='EStop Sent')
            case 'BP':
                info(sender=sender, app_data='Break Point')
                breakpoint()
    
            case 'Bias':
                from FTCommunications import get_FTPort, get_FTSocketAddress, setup_socket, bias
                FTSocket = setup_socket()
                FTPort = get_FTPort()
                FTSocketAddress = get_FTSocketAddress()  
                bias(FTSocket, FTSocketAddress, FTPort)   
                info(sender=sender, app_data='Bias Command Sent')
                
            
            case _:
                info(sender=sender, app_data=app_data, user_data=user_data)

def info(sender=None, app_data=None, user_data=None):
    TimeStamp = datetime.now().strftime('%H:%M:%S.%f')
    InfoString = ''
    if sender is not None:
        try:
            InfoString = InfoString + ' ['+ str(sender) + ']'
        except:
            False
    if app_data is not None:
        try:
            InfoString = InfoString + ' ' + str(app_data)
        except:
            False
    if user_data is not None:
        try:
            InfoString = InfoString + ' ' + str(user_data)
        except:
            False 
    if InfoString == '':
        InfoString = 'Failed to get info'
        
    InfoString = TimeStamp + ':' + InfoString
    
    PastInfoCount = 5
    PastInfo = np.array(np.zeros((PastInfoCount)), dtype=object)
    for i in range(PastInfoCount):
        PastInfo[i] = dpg.get_value('Past Info '+str(i))
    PastInfo = np.roll(PastInfo, 1, axis=0)
    PastInfo[0] = InfoString
    
    for i in range(PastInfoCount):
        dpg.set_value('Past Info '+str(i), PastInfo[i])
    print(InfoString)
    return