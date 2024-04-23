import socket
import numpy as np

Port = 49152
Command = 2
Num_Samples = 1
sockaddr_in = "192.168.1.1"
cpft = 1000000

FTData = np.array(np.single(np.zeros(6)))

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
sock.sendto(bias,(sockaddr_in,Port))

request = b'\x12\x34\x00\x02\x00\x00\x00\x01'

while True:
    sock.sendto(request,(sockaddr_in,Port))
    data, addr = sock.recvfrom(36)
    for i in range(24,1):
        FTData[:,i]=FTData[:,i-1]
    for i in range(0,6,1):
        FTData[i]=int.from_bytes(data[12+i*4:15+i*4],'big',signed=True)/cpft
        FTData[i]=round(FTData[i]*1000)
    #print("\033[H\033[J")
    #time.sleep(.001)
    print(FTData)