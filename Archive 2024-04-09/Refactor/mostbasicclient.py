import socket

UDPRobotClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPRobotClientSocket.settimeout(0.05)
RobotServerBufferSize    = 1024
RobotServerAddressPort = ("192.168.1.105", 23)

while True:
    RobotBytesToSend = b'hello'
    UDPRobotClientSocket.sendto(RobotBytesToSend, RobotServerAddressPort)
    
    try:
        BytesAddressPair = UDPRobotClientSocket.recvfrom(RobotServerBufferSize)
        print('Recieved:',BytesAddressPair[0])       
    except socket.timeout as e:
        err = e.args[0]
        if err == 'timed out':
            True
    except socket.error as e:
        print(e)
        