import socket
import struct
import sys
import numpy as np
from InputStateErrorValues import input_state_error_values
from InputJointAngles import input_joint_angles
import dearpygui as dpg
import time
# from GrandCentralDispatch import info

def get_RobotServerAddressPort():
    return ("192.168.1.105", 23)

def get_RobotServerBufferSize():
    return 1024

def setup_robot_socket():
    UDPRobotClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPRobotClientSocket.settimeout(0.001)
    # UDPRobotClientSocket.bind(('192.168.1.21', 23))
    return UDPRobotClientSocket

def unpack_robot_data(BytesAddressPair):
    MagicNumberR = 0
    StateValueR = 0
    ErrorValueR = 0
    EncoderValueR = np.array(np.zeros((6)))
    ThetaValueR = np.array(np.zeros((6)))
    PositionVectorR = np.array(np.zeros((3)))
    FTZR = np.array(np.zeros((3)))
    FTXR = np.array(np.zeros((3)))
    try:
        (MagicNumberR, 
        StateValueR,
        ErrorValueR,
        EncoderValueR[0], EncoderValueR[1], EncoderValueR[2], EncoderValueR[3], EncoderValueR[4], EncoderValueR[5],
        ThetaValueR[0], ThetaValueR[1], ThetaValueR[2], ThetaValueR[3], ThetaValueR[4], ThetaValueR[5],
        PositionVectorR[0], PositionVectorR[1], PositionVectorR[2],
        FTZR[0], FTZR[1], FTZR[2],
        FTXR[0], FTXR[1], FTXR[2]
        )  = struct.unpack('Qiiiiiiiiddddddddddddddd', BytesAddressPair[0])
        
        return MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR
    except: return None

def get_robot_data(UDPRobotClientSocket, RobotServerBufferSize):
    BytesAddressPair = None
    try:
        BytesAddressPair = UDPRobotClientSocket.recvfrom(RobotServerBufferSize)
        # print('Recieved:',BytesAddressPair[0])   
    except socket.timeout as e:
        err = e.args[0]
        if err == 'timed out': True
    except socket.error as e:
        print(e) 
        
    return BytesAddressPair

def send_robot_data(UDPRobotClientSocket, RobotServerAddressPort):
    
        StateValueS, ErrorValueS = input_state_error_values()
        # breakpoint()
        PositionVectorS, FTZS, FTXS = input_joint_angles()
        
        MagicNumberS = 0xFF00AA55
        RobotBytesToSend = struct.pack('Qiiddddddddd', 
                                MagicNumberS,
                                StateValueS,
                                ErrorValueS,
                                PositionVectorS[0], PositionVectorS[1], PositionVectorS[2],
                                FTZS[0], FTZS[1], FTZS[2],
                                FTXS[0], FTXS[1], FTXS[2],
                                )
        UDPRobotClientSocket.sendto(RobotBytesToSend, RobotServerAddressPort)
        
def query_robot_state(UDPRobotClientSocket, RobotServerAddressPort):
    try:
        StateValueS, ErrorValueS = input_state_error_values()
        StateValueS = 3 #query
        PositionVectorS, FTZS, FTXS = input_joint_angles()
        MagicNumberS = 0xFF00AA55
    
        RobotBytesToSend = struct.pack('Qiiddddddddd', 
                            MagicNumberS,
                            StateValueS,
                            ErrorValueS,
                            PositionVectorS[0], PositionVectorS[1], PositionVectorS[2],
                            FTZS[0], FTZS[1], FTZS[2],
                            FTXS[0], FTXS[1], FTXS[2],
                            )
        # breakpoint()
        UDPRobotClientSocket.sendto(RobotBytesToSend, RobotServerAddressPort)
    except Exception as e:
        print(e)
        
def must_get_robot_state(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize):
    query_robot_state(UDPRobotClientSocket, RobotServerAddressPort)
    BytesAddressPair = None
    while BytesAddressPair is None:
        print('Awaiting Robot Data')
        try:
            BytesAddressPair = UDPRobotClientSocket.recvfrom(RobotServerBufferSize)
        except:
            query_robot_state(UDPRobotClientSocket, RobotServerAddressPort)
    MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = unpack_robot_data(BytesAddressPair)
    return MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR
            
        