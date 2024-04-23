import socket
import struct
import sys

def recieve_robot_data():
    DataRecievedBool = False
    try:
        MagicNumberR = 0
        StateValueR = 0
        ErrorValueR = 0
        EncoderValueR = [0]*6
        ThetaValueR = [0]*6
        PositionVectorR = [0]*3
        FTZR = [0]*3
        FTXR = [0]*3
        
        try:
            BytesAddressPair = UDPRobotClientSocket.recvfrom(RobotServerBufferSize)
        except socket.timeout as e:
            err = e.args[0]
            # this next if/else is a bit redundant, but illustrates how the
            # timeout exception is setup
            if err == 'timed out':
                # sleep(0.01)
                True
            # else:
            #     print(e)
            #     sys.exit(1)
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
                
            
                (MagicNumberR, 
                StateValueR,
                ErrorValueR,
                EncoderValueR[0], EncoderValueR[1], EncoderValueR[2], EncoderValueR[3], EncoderValueR[4], EncoderValueR[5],
                ThetaValueR[0], ThetaValueR[1], ThetaValueR[2], ThetaValueR[3], ThetaValueR[4], ThetaValueR[5],
                PositionVectorR[0], PositionVectorR[1], PositionVectorR[2],
                FTZR[0], FTZR[1], FTZR[2],
                FTXR[0], FTXR[1], FTXR[2]
                )  = struct.unpack('Qiiiiiiiiddddddddddddddd', BytesAddressPair[0])
                
            
                # clientMsg = "Message from Robot Server:{}".format(message)
                # clientIP  = "Client IP Address:{}".format(address)
                print('Packet Echo Recieved:')
                print('Magic Number: {}'.format('%x' % MagicNumberR))
                print('State Variable: {}'.format(StateValueR))
                print('Error Value: {}'.format(ErrorValueR))
                print('Encoder Value: {}'.format(EncoderValueR))
                print('Theta Value: {}'.format(ThetaValueR))
                print('Position Vector: {}'.format(PositionVectorR))
                print('FT-Z: {}'.format(FTZR))
                print('FT-X: {}'.format(FTXR))
                print('Recieved: {}'.format(BytesAddressPair[0]))
                DataRecievedBool = True
        
    except SystemExit:
        sys.exit(1)
        
    return DataRecievedBool, [MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR]


def main():
    global RobotServerAddressPort
    RobotServerAddressPort   = ("192.168.1.105", 23)
    global RobotServerBufferSize
    RobotServerBufferSize    = 1024
    global UDPRobotClientSocket
    UDPRobotClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    try:
        UDPRobotClientSocket.settimeout(0.05)
        while True:
            MagicNumberS = b'ff00aa55'
            RobotBytesToSend = struct.pack('Qiiddddddddd', 
                                    0xFF00AA55,
                                    # MagicNumberS, 
                                    0,
                                    0,
                                    0, 0, 0,
                                    0, 0, 0,
                                    0, 0, 0,
                                    )
            UDPRobotClientSocket.sendto(RobotBytesToSend, RobotServerAddressPort)
            
            DataRecievedBool, DataRecievedList = recieve_robot_data()

            if DataRecievedBool:
                MagicNumberR = DataRecievedList[0]
                StateValueR = DataRecievedList[1]
                ErrorValueR = DataRecievedList[2]
                EncoderValueR = DataRecievedList[3]
                ThetaValueR = DataRecievedList[4]
                PositionVectorR = DataRecievedList[5]
                FTZR = DataRecievedList[6]
                FTXR = DataRecievedList[7]
            
            
    except KeyboardInterrupt:
        UDPRobotClientSocket.close()
        
if (__name__ == '__main__'): 
    main()