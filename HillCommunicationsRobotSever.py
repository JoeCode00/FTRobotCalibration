import sys
import socket

from struct import unpack, pack
from time import sleep
from numpy import pi
from random import random

localIP     = "192.168.1.105"
localPort   = 23
bufferSize  = 1024

PacketCount = 0

# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# UDPServerSocket.setsockopt(level, optname, value)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
try:
    UDPServerSocket.settimeout(1)
    # UDPServerSocket.setblocking(False)
    print("UDP server up and listening")
    
    while True:
        try:
            BytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        except socket.timeout as e:
            err = e.args[0]
            # this next if/else is a bit redundant, but illustrates how the
            # timeout exception is setup
            if err == 'timed out':
                sleep(0.01)
                continue
            else:
                print(e)
                sys.exit(1)
        except socket.error as e:
            # Something else happened, handle error, exit, etc.
            print(e)
            sys.exit(1)
        else:
            if len(BytesAddressPair) == 0:
                print('orderly shutdown on server end')
                sys.exit(0)
            else:
                # got a message do something :)
                PositionVectorR = [0]*3
                FTZR = [0]*3
                FTXR = [0]*3
            
                (MagicNumberR, StateValueR, ErrorValueR, PositionVectorR[0], PositionVectorR[1], PositionVectorR[2], FTZR[0], FTZR[1], FTZR[2], FTXR[0], FTXR[1], FTXR[2])  = unpack('Qiiddddddddd', BytesAddressPair[0])
                
            
                PacketCount = PacketCount+1
            
                # clientMsg = "Message from Robot Server:{}".format(message)
                # clientIP  = "Client IP Address:{}".format(address)
                print('Packet Recieved:', PacketCount)
                # print('Magic Number: {}'.format(MagicNumberR))
                print('State Variable: {}'.format(StateValueR))
                # print('Error Value: {}'.format(ErrorValueR))
                # print('Position Vector: {}'.format(PositionVectorR))
                # print('FT-Z: {}'.format(FTZR))
                # print('FT-X: {}'.format(FTXR))
                # print('Recieved: {}'.format(BytesAddressPair[0]))
                
                
                MagicNumberS = 0xFF00AA55
                StateValueS = StateValueR
                ErrorValueS = ErrorValueR
                EncoderValueS = [i for i in range(-300,300,100)]
                # ThetaValueS = [i*pi/3 for i in range(0,6)]
                ThetaValueS = [1,2,3,4,5,6]
                
                # PositionVectorS = PositionVectorR
                PositionVectorS = [800+random(), 100+random(),300+random()]
                
                FTZS = FTZR
                FTXS = FTXR
                BytesToSend = pack('Qiiiiiiiiddddddddddddddd',
                                    MagicNumberS, 
                                    StateValueS,
                                    ErrorValueS,
                                    EncoderValueS[0], EncoderValueS[1], EncoderValueS[2], EncoderValueS[3], EncoderValueS[4], EncoderValueS[5],
                                    ThetaValueS[0], ThetaValueS[1], ThetaValueS[2], ThetaValueS[3], ThetaValueS[4], ThetaValueS[5],
                                    PositionVectorS[0], PositionVectorS[1], PositionVectorS[2],
                                    FTZS[0], FTZS[1], FTZS[2],
                                    FTXS[0], FTXS[1], FTXS[2]
                                    )
                Address = BytesAddressPair[1]
                # BytesToSend = b'Hello From Server'
                
                # while True:
                UDPServerSocket.sendto(BytesToSend, Address)
                # print('Echoed Packet')
                # print('Sent: {}'.format(BytesToSend))                 
    
except KeyboardInterrupt:
    print('ended')
    UDPServerSocket.close()
    
except OSError as e:
    print(e)
    sleep(10)