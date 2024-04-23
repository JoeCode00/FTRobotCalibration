# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 14:38:27 2023

@author: Joe
"""
import socket
from struct import pack, unpack
import sys
from math import sqrt
from matplotlib import use
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button 
import numpy as np

use("Qt5agg")

def InitFig():
    Fig=[0]*2
    plt.show(block = False)

    Fig[0] = plt.figure(figsize=(10,6),animated='false') #buttons
    plt.rcParams['text.color'] = 'White'
    Fig[0].set_facecolor('Black')
    

    Fig[0].canvas.setFocus()
    
    #Sliders
    #TO ADD A SLIDER:
    #Add a line to SliderInfo
    #Add a line to .val block in main loop
    
            #min value, max value, initial value, step value
    SCol0Info = [[0, 50, 0, 1, 'State Value'], 
                 [0, 50, 0, 1, 'Error Value'],
                 [0, 100, 50, 1.0, 'Slider 2  '],
                 [0, 100, 50, 1.0, 'Slider 3  '],
                 [0, 100, 50, 1.0, 'Slider 4  '],
                 [0, 100, 50, 1.0, 'Slider 5  ']
                 ]
    
    
    SCol0Nslider = len(SCol0Info)
    SCol0Width = 0.1
    SCol0Hight = 0.03
    SCol0XOffsetFromLeftWall = 0.1
    SCol0Spacing = 0.9/(SCol0Nslider+1)
    SCol0Array = [0]*SCol0Nslider
    SCol0AxesArray = [0]*SCol0Nslider  
    
    for i in np.arange(SCol0Nslider):
        SCol0AxesArray[i] = plt.axes(([SCol0XOffsetFromLeftWall,
                                          1-(SCol0Spacing*(i+1)),
                                          SCol0Width,SCol0Hight]))#x,y,w,h
        SCol0Array[i] = Slider(SCol0AxesArray[i],
                                 SCol0Info[i][4],
                                 valmin=SCol0Info[i][0],
                                 valmax=SCol0Info[i][1],
                                 valinit=SCol0Info[i][2],
                                 valstep=SCol0Info[i][3])

                #min value, max value, initial value, step value
    SCol1Info = [[-100, 100, -50, 1.0, 'Position Vector X'], 
                 [-100, 100, -30, 1.0, 'Position Vector Y'],
                 [-100, 100, -10, 1.0, 'Position Vector Z'],
                 [-100, 100,  10, 1.0, 'FT-Z X'],
                 [-100, 100,  20, 1.0, 'FT-Z Y'],
                 [-100, 100,  30, 1.0, 'FT-Z Z'],
                 [-100, 100,  40, 1.0, 'FT-X X'],
                 [-100, 100,  50, 1.0, 'FT-X Y'],
                 [-100, 100,  60, 1.0, 'FT-X z'],
                 ]
    
    
    SCol1Nslider = len(SCol1Info)
    SCol1Width = 0.1
    SCol1Hight = 0.03
    SCol1XOffsetFromLeftWall = 0.45
    SCol1Spacing = 1/(SCol1Nslider+1)
    SCol1Array = [0]*SCol1Nslider
    SCol1AxesArray = [0]*SCol1Nslider  
    
    for i in np.arange(SCol1Nslider):
        SCol1AxesArray[i] = plt.axes(([SCol1XOffsetFromLeftWall,
                                          1-(SCol1Spacing*(i+1)),
                                          SCol1Width,SCol1Hight]))#x,y,w,h
        SCol1Array[i] = Slider(SCol1AxesArray[i],
                                 SCol1Info[i][4],
                                 valmin=SCol1Info[i][0],
                                 valmax=SCol1Info[i][1],
                                 valinit=SCol1Info[i][2],
                                 valstep=SCol1Info[i][3])
        

    
    

    #quit button
    QuitAxes=plt.axes([.05,.05,.3,.1])
    QuitButton = Button(QuitAxes,'Quit Figure',image=None,color='0.25',hovercolor='red')

    # QuitButton.label.setColor('White')
    QuitCallback=QuitIndex()
    QuitButton.on_clicked(QuitCallback.QuitFunc)
    
    #TO ADD A BUTTON: 
    #Add a title to the title array
    #Add a line to the .onclicked list
    #Add an entry to the correct index
    #Add if statement in main loop, calling new "function"
    
    #Buttons
    global BCol0Title
    BCol0Title = [  'Send To Robot',
                    'Button 1',
                    'Button 2',
                    'Button 3',
                    'Button 4',
                    'Button 5',  
                    ]
     
    global BCol1Title
    BCol1Title = [  'Button 6',
                    'Button 7',
                    'Button 8',
                    'Button 9',
                    'Button 10',
                    'Button 11',
                    ]
    
    global BCol2Title
    BCol2Title = [  'Button 12',
                    'Button 13',
                    'Button 14',
                    'Button 15',
                    'Button 16',
                    'Button 17',
                    ]
    
    global BCol3Title
    BCol3Title = [  'Button 18',
                    'Button 19',
                    'Button 20',
                    'Button 21',
                    'Button 22',
                    'Button 23',
                    ]

    BCol0XOffsetFromLeftWall = 0.6
    BCol1XOffsetFromLeftWall = 0.7
    BCol2XOffsetFromLeftWall = 0.8
    BCol3XOffsetFromLeftWall = 0.9
    
    BCol0Array = CreateButtons(Fig, BCol0Title,BCol0XOffsetFromLeftWall)
    BCol1Array = CreateButtons(Fig, BCol1Title,BCol1XOffsetFromLeftWall)
    BCol2Array = CreateButtons(Fig, BCol2Title,BCol2XOffsetFromLeftWall)
    BCol3Array = CreateButtons(Fig, BCol3Title,BCol3XOffsetFromLeftWall)
    

    BCol0Callback=BCol0Index()
    BCol0Array[0].on_clicked(BCol0Callback.Button0)
    BCol0Array[1].on_clicked(BCol0Callback.Button1)
    BCol0Array[2].on_clicked(BCol0Callback.Button2)
    BCol0Array[3].on_clicked(BCol0Callback.Button3)
    BCol0Array[4].on_clicked(BCol0Callback.Button4)
    BCol0Array[5].on_clicked(BCol0Callback.Button5)
    

    BCol1Callback=BCol1Index()
    BCol1Array[0].on_clicked(BCol1Callback.Button0)
    BCol1Array[1].on_clicked(BCol1Callback.Button1)
    BCol1Array[2].on_clicked(BCol1Callback.Button2)
    BCol1Array[3].on_clicked(BCol1Callback.Button3)
    BCol1Array[4].on_clicked(BCol1Callback.Button4)
    BCol1Array[5].on_clicked(BCol1Callback.Button5)
    

    BCol2Callback=BCol2Index()
    BCol2Array[0].on_clicked(BCol2Callback.Button0)
    BCol2Array[1].on_clicked(BCol2Callback.Button1)
    BCol2Array[2].on_clicked(BCol2Callback.Button2)
    BCol2Array[3].on_clicked(BCol2Callback.Button3)
    BCol2Array[4].on_clicked(BCol2Callback.Button4)
    BCol2Array[5].on_clicked(BCol2Callback.Button5)
    
    BCol3Callback=BCol3Index()
    BCol3Array[0].on_clicked(BCol3Callback.Button0)
    BCol3Array[1].on_clicked(BCol3Callback.Button1)
    BCol3Array[2].on_clicked(BCol3Callback.Button2)
    BCol3Array[3].on_clicked(BCol3Callback.Button3)
    BCol3Array[4].on_clicked(BCol3Callback.Button4)
    BCol3Array[5].on_clicked(BCol3Callback.Button5)
    Fig[0].show()
    
    return Fig, SCol1Array, SCol0Array, BCol0Array, BCol1Array, BCol2Array, BCol3Array, QuitButton

def CreateButtons(Fig, ButtonTitle,ButtonXOffsetFromLeftWall):
    NButton = len(ButtonTitle)
    ButtonWidth = 0.07
    ButtonHeight = 0.05
    ButtonNormalColor = '0.25'
    ButtonHoverColor = 'red'
    ButtonSpacing = 1/(NButton+1)
    ButtonArray = [0]*NButton
    ButtonAxesArray = [0]*NButton
    for i in np.arange(NButton):
        ButtonAxesArray[i] = plt.axes(([ButtonXOffsetFromLeftWall,1-(ButtonSpacing*(i+1)),ButtonWidth,ButtonHeight]))#x,y,w,h
        ButtonArray[i] = Button(ButtonAxesArray[i],ButtonTitle[i],image=None,color=ButtonNormalColor,hovercolor=ButtonHoverColor)
        # ButtonArray[i].label.setColor('White')
    return ButtonArray

class QuitIndex():
    def QuitFunc(self, event):
        print('quitting')
        plt.close("all")
        UDPClientSocket.close()
        global QuitBool
        
        QuitBool = True
        # UDPClientSocket.close()

class BCol0Index():
    def Button0(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[0]
        try:
            UDPClientSocket.sendto(BytesToSend, serverAddressPort)
            print(BCol0Title[0])
            print('Packet Sent:')
            print('Magic Number: {}'.format(MagicNumberS))
            print('State Variable: {}'.format(StateValueS))
            print('Error Value: {}'.format(ErrorValueS))
            print('Position Vector: {}'.format(PositionVectorS))
            print('FT-Z: {}'.format(FTZS))
            print('FT-X: {}'.format(FTXS))
            print('Sent: {}'.format(BytesToSend))
            print('\n')
        except NameError as e:
            print(e)
        
        
    def Button1(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[1]
        print(BCol0Title[1])
    def Button2(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[2]
        print(BCol0Title[2])
    def Button3(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[3]
        print(BCol0Title[3])
    def Button4(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[4]
        print(BCol0Title[4])
    def Button5(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[5]
        print(BCol0Title[5])
        
class BCol1Index():
    def Button0(self, event):
        global BCol1Current
        BCol1Current=BCol1Title[0]
        print(BCol1Title[0])
    def Button1(self, event):
        global BCol1Current
        BCol1Current=BCol1Title[1]
        print(BCol1Title[1])
    def Button2(self, event):
        global BCol1Current
        BCol1Current=BCol1Title[2]
        print(BCol1Title[2])
    def Button3(self, event):
        global BCol1Current
        BCol1Current=BCol1Title[3]
        print(BCol1Title[3])
    def Button4(self, event):
        global BCol1Current
        BCol1Current=BCol1Title[4]
        print(BCol1Title[4])
    def Button5(self, event):
        global BCol1Current
        BCol1Current=BCol1Title[5]
        print(BCol1Title[5])
        
class BCol2Index():
    def Button0(self, event):
        global BCol2Current
        BCol2Current=BCol2Title[0]
        print(BCol2Title[0])
    def Button1(self, event):
        global BCol2Current
        BCol2Current=BCol2Title[1]
        print(BCol2Title[1])
    def Button2(self, event):
        global BCol2Current
        BCol2Current=BCol2Title[2]
        print(BCol2Title[2])
    def Button3(self, event):
        global BCol2Current
        BCol2Current=BCol2Title[3]
        print(BCol2Title[3])
    def Button4(self, event):
        global BCol2Current
        BCol2Current=BCol2Title[4]
        print(BCol2Title[4])
    def Button5(self, event):
        global BCol2Current
        BCol2Current=BCol2Title[5]
        print(BCol2Title[5])
        
class BCol3Index():
    def Button0(self, event):
        global BCol3Current
        BCol3Current=BCol3Title[0]
        print(BCol3Title[0])
    def Button1(self, event):
        global BCol3Current
        BCol3Current=BCol3Title[1]
        print(BCol3Title[1])
    def Button2(self, event):
        global BCol3Current
        BCol3Current=BCol3Title[2]
        print(BCol3Title[2])
    def Button3(self, event):
        global BCol3Current
        BCol3Current=BCol3Title[3]
        print(BCol3Title[3])
    def Button4(self, event):
        global BCol3Current
        BCol3Current=BCol3Title[4]
        print(BCol3Title[4])
    def Button5(self, event):
        global BCol3Current
        BCol3Current=BCol3Title[5]
        print(BCol3Title[5])
        


def unit_vector(vector):
  """
  Converts a 3D vector to a unit vector.

  Args:
    vector: A 3D vector.

  Returns:
    A unit vector.
  """

  # Calculate the length of the vector.
  length = sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

  # Divide each component of the vector by the length.
  unit_vector = [vector[0] / length, vector[1] / length, vector[2] / length]

  return unit_vector

def main():
    global QuitBool
    QuitBool = False
    Fig, SCol1Array, SCol0Array, BCol0Array, BCol1Array, BCol2Array, BCol3Array, QuitButton = InitFig()
    
    global BCol0Current
    BCol0Current = 'BCol0CurrentButton'
    
    global BCol1Current
    BCol1Current = 'BCol1CurrentButton'
    
    global BCol2Current
    BCol2Current = 'BCol2CurrentButton'
    
    global BCol3Current
    BCol3Current = 'BCol3CurrentButton'
    
    global serverAddressPort
    serverAddressPort   = ("192.168.0.1", 23)
    
    global bufferSize
    bufferSize          = 102400
    
    localIP = '192.168.0.3'
    localPort = 5049
    # Create a UDP socket at client side
    
    global UDPClientSocket
    UDPClientSocket = socket.socket(
            family = socket.AF_INET,
            type   = socket.SOCK_DGRAM,
            proto  = socket.IPPROTO_IP,
            fileno = None)
    UDPClientSocket.bind((localIP, localPort))
    try:
        UDPClientSocket.settimeout(0.05)
    
        # Send to server using created UDP socket
    
        while QuitBool == False:
            try:
                global BytesToSend, MagicNumberS, StateValueS, ErrorValueS, PositionVectorS, FTZS, FTXS
                
                #poll all sliders
                StateValueS  = int(SCol0Array[0].val)
                ErrorValueS  = int(SCol0Array[1].val)
                # Slider2     = SCol0Array[2].val
                # Slider3     = SCol0Array[3].val
                # Slider4     = SCol0Array[4].val
                # Slider5     = SCol0Array[5].val
                
                PositionVectorS = [0]*3
                FTZS = [0]*3 
                FTXS = [0]*3
                
                PositionVectorS[0]   = SCol1Array[0].val
                PositionVectorS[1]   = SCol1Array[1].val
                PositionVectorS[2]   = SCol1Array[2].val
                FTZS[0]  = SCol1Array[3].val
                FTZS[1]  = SCol1Array[4].val
                FTZS[2]  = SCol1Array[5].val
                FTXS[0]  = SCol1Array[6].val
                FTXS[1]  = SCol1Array[7].val
                FTXS[2]  = SCol1Array[8].val
                
                #make FTZ and FTX unit vectors
                FTZS = unit_vector(FTZS)
                FTXS = unit_vector(FTXS)
                
                
                MagicNumberS = b'ff00aa55'
                BytesToSend = pack('Qiiddddddddd', 
                                    0xFF00AA55,
                                    StateValueS,
                                    ErrorValueS,
                                    PositionVectorS[0], PositionVectorS[1], PositionVectorS[2],
                                    FTZS[0], FTZS[1], FTZS[2],
                                    FTXS[0], FTXS[1], FTXS[2],
                                    )
                # breakpoint()
                Fig[0].canvas.draw()
                Fig[0].canvas.flush_events()
                try:
                    BytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
                except socket.timeout as e:
                    err = e.args[0]
                    # this next if/else is a bit redundant, but illustrates how the
                    # timeout exception is setup
                    if err == 'timed out':
                        # sleep(0.01)
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
                        EncoderValueR = [0]*6
                        ThetaValueR = [0]*6
                        PositionVectorR = [0]*3
                        FTZR = [0]*3
                        FTXR = [0]*3
                        
                        breakpoint()
                        (MagicNumberR, 
                        StateValueR,
                        ErrorValueR,
                        EncoderValueR[0], EncoderValueR[1], EncoderValueR[2], EncoderValueR[3], EncoderValueR[4], EncoderValueR[5],
                        ThetaValueR[0], ThetaValueR[1], ThetaValueR[2], ThetaValueR[3], ThetaValueR[4], ThetaValueR[5],
                        PositionVectorR[0], PositionVectorR[1], PositionVectorR[2],
                        FTZR[0], FTZR[1], FTZR[2],
                        FTXR[0], FTXR[1], FTXR[2]
                        )  = unpack('Qiiiiiiiiddddddddddddddd', BytesAddressPair[0])
                        
                    
                        # clientMsg = "Message from Robot Server:{}".format(message)
                        # clientIP  = "Client IP Address:{}".format(address)
                        print('Packet Echo Recieved:')
                        print('Magic Number: {:02X}'.format(MagicNumberR))
                        print('State Variable: {}'.format(StateValueR))
                        print('Error Value: {}'.format(ErrorValueR))
                        print('Encoder Value: {}'.format(EncoderValueR))
                        print('Theta Value: {}'.format(ThetaValueR))
                        print('Position Vector: {}'.format(PositionVectorR))
                        print('FT-Z: {}'.format(FTZR))
                        print('FT-X: {}'.format(FTXR))
                        print('Recieved: {}'.format(BytesAddressPair[0]))
        
                Fig[0].canvas.draw()
                Fig[0].canvas.flush_events()
            except SystemExit:
                sys.exit(1)
    except KeyboardInterrupt:
        UDPClientSocket.close()
    
        
if (__name__ == '__main__'): 
    main()