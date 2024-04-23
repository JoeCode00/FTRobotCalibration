import numpy as np
from datetime import datetime
import struct
import socket


def get_FTPort():
    return 49152

def get_FTSocketAddress():
    return "192.168.1.20"

def get_FTLimits():
    FXYZLimit_N = 75/10
    TXYZLimit_Nm = 4/10
    return FXYZLimit_N, TXYZLimit_Nm

def setup_socket():
    FTSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return FTSocket

def get_FT_data(SensorConnected, FTSocket, FTSocketAddress, FTPort):
    
    if SensorConnected:
        request = b'\x12\x34\x00\x02\x00\x00\x00\x01'

        FTSocket.sendto(request,(FTSocketAddress, FTPort))
        NewFTData, addr = FTSocket.recvfrom(36)
    else:
        # FX = np.sin(datetime.now().microsecond/1000000*2*np.pi)*3*(datetime.now().second/30)
        # FY = np.sin(datetime.now().microsecond/1000000*2*np.pi+2*np.pi/3)*3
        # FZ = np.sin(datetime.now().microsecond/1000000*2*np.pi+4*np.pi/3)*3
        # TX = np.cos(datetime.now().microsecond/1000000*2*np.pi)/3*(datetime.now().second/30)
        # TY = np.cos(datetime.now().microsecond/1000000*2*np.pi+2*np.pi/3)/3
        # TZ = np.cos(datetime.now().microsecond/1000000*2*np.pi+4*np.pi/3)/3
        FX = 0
        FY = 0
        if datetime.now().second % 5 == 0:
            FZ = datetime.now().microsecond/500000
        else:
            FZ = 0
        TX = 0
        TY = 0
        TZ = 0
        
        NewFTData = struct.pack('>ffffff', FX, FY, FZ, TX, TY, TZ)
        
    return NewFTData
        


def bias(FTSocket, FTSocketAddress, FTPort):
    Bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
    FTSocket.sendto(Bias,(FTSocketAddress,FTPort))