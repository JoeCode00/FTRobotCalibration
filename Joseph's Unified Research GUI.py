import socket
from struct import pack, unpack
import sys
from matplotlib import use, gridspec, table
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button 

from datetime import datetime, timedelta
from numpy import arange, append, sqrt, pi, array, linspace, single, zeros, cos, sin, tan, size, sum, round, square, arcsin, arccos, arctan2, nan, cross, dot, rad2deg, full_like, where, array_equal
from pandas import DataFrame


def init_command_fig(HistorySeconds, FXYZLimit_N, TXYZLimit_Nm):
    CommandFig = plt.figure(figsize = (16, 12), animated='true')
    FigGridSpec = gridspec.GridSpec(2,2, figure = CommandFig, width_ratios = [1,1], height_ratios = [2,1])
    ButtonSliderSubfig = CommandFig.add_subfigure(gridspec.SubplotSpec(FigGridSpec, 0))
    GraphSubfig = CommandFig.add_subfigure(gridspec.SubplotSpec(FigGridSpec, 1))
    AnglesSubfig = CommandFig.add_subfigure(gridspec.SubplotSpec(FigGridSpec, 2))
    QuitSubfig = CommandFig.add_subfigure(gridspec.SubplotSpec(FigGridSpec, 3))

    GraphSubPlotMosaic = GraphSubfig.subplot_mosaic(
        [
            ['HistoryFXYZ', 'HistoryTXYZ'],
            ['PositionFXYZ', 'PositionTXYZ'],
        ], 
        )

    plt.show(block=False)
    plt.pause(0.1)

    ButtonSliderSubfig.set_facecolor('black')
    GraphSubfig.set_facecolor('black')
    QuitSubfig.set_facecolor('black')

    ButtonSliderSubfig.patch.set_linewidth(2)
    GraphSubfig.patch.set_linewidth(2)
    QuitSubfig.patch.set_linewidth(2)

    ButtonSliderSubfig.patch.set_edgecolor('white')
    GraphSubfig.patch.set_edgecolor('white')
    QuitSubfig.patch.set_edgecolor('white')

    plt.rcParams['text.color'] = 'White'

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

    for i in arange(SCol0Nslider):
        SCol0AxesArray[i] = ButtonSliderSubfig.add_axes(([SCol0XOffsetFromLeftWall,
                                          1-(SCol0Spacing*(i+1)),
                                          SCol0Width,SCol0Hight]))#x,y,w,h
        SCol0Array[i] = Slider(SCol0AxesArray[i],
                                 SCol0Info[i][4],
                                 valmin=SCol0Info[i][0],
                                 valmax=SCol0Info[i][1],
                                 valinit=SCol0Info[i][2],
                                 valstep=SCol0Info[i][3])

                #min value, max value, initial value, step value
    SCol1Info = [[-1000, 1000, 800, 1.0, 'Position Vector X'], 
                 [-1000, 1000, 800, 1.0, 'Position Vector Y'],
                 [-1000, 1000, 180, 1.0, 'Position Vector Z'],
                 [-10, 10, -0.5774, 0.01, 'FT-Z X'],
                 [-10, 10,  0.5774, 0.01, 'FT-Z Y'],
                 [-10, 10,  0.5774, 0.01, 'FT-Z Z'],
                 [-10, 10,  0.4082, 0.01, 'FT-X X'],
                 [-10, 10,  0.8165, 0.01, 'FT-X Y'],
                 [-10, 10, -0.4082, 0.01, 'FT-X Z'],
                 ]

    SCol1Nslider = len(SCol1Info)
    SCol1Width = 0.1
    SCol1Hight = 0.03
    SCol1XOffsetFromLeftWall = 0.45
    SCol1Spacing = 0.9/(SCol1Nslider+1)
    SCol1Array = [0]*SCol1Nslider
    SCol1AxesArray = [0]*SCol1Nslider  

    for i in arange(SCol1Nslider):
        SCol1AxesArray[i] = ButtonSliderSubfig.add_axes(([SCol1XOffsetFromLeftWall,
                                          1-(SCol1Spacing*(i+1)),
                                          SCol1Width,SCol1Hight]))#x,y,w,h
        SCol1Array[i] = Slider(SCol1AxesArray[i],
                                 SCol1Info[i][4],
                                 valmin=SCol1Info[i][0],
                                 valmax=SCol1Info[i][1],
                                 valinit=SCol1Info[i][2],
                                 valstep=SCol1Info[i][3])
            
    #quit button
    QuitAxes=QuitSubfig.add_axes([0,0,1,1])
    QuitButton = Button(QuitAxes,'Quit',image=None,color='0.25',hovercolor='red')

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
    BCol1Title = [  'Bias FT',
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

    BCol0Array = CreateButtons(ButtonSliderSubfig, BCol0Title,BCol0XOffsetFromLeftWall)
    BCol1Array = CreateButtons(ButtonSliderSubfig, BCol1Title,BCol1XOffsetFromLeftWall)
    BCol2Array = CreateButtons(ButtonSliderSubfig, BCol2Title,BCol2XOffsetFromLeftWall)
    BCol3Array = CreateButtons(ButtonSliderSubfig, BCol3Title,BCol3XOffsetFromLeftWall)


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

    HistoryFXYZ = GraphSubPlotMosaic['HistoryFXYZ']

    HistoryLineFX, = HistoryFXYZ.plot(0, 0, label='FX', color = 'red', animated = True)
    HistoryLineFY, = HistoryFXYZ.plot(0, 0, label='FY', color = 'green', animated = True)
    HistoryLineFZ, = HistoryFXYZ.plot(0, 0, label='FZ', color = 'blue', animated = True)
    HistoryFXYZ.set_xlim([-HistorySeconds, 0])
    HistoryFXYZ.set_ylim([-FXYZLimit_N, FXYZLimit_N])
    HistoryFXYZ.set_xlabel('Time (s)', color = 'white')
    HistoryFXYZ.set_ylabel('Force (N)', color = 'white')
    HistoryFXYZ.set_facecolor('black')
    HistoryFXYZ.grid(True, linestyle='-.')
    HistoryFXYZ.tick_params(axis = 'both', 
                            which = 'both', 
                            color = 'white',
                            labelcolor = 'white', 
                            grid_color = 'grey', 
                            grid_linewidth = 0.3)
    HistoryFXYZ.annotate('Force History', 
                          (0.5, 0.9), 
                          ha='center', 
                          va='center', 
                          xycoords = 'axes fraction',
                          fontsize=18,
                          color='darkgrey')

    HistoryTXYZ = GraphSubPlotMosaic['HistoryTXYZ']
    (HistoryLineTX,) = HistoryTXYZ.plot(0, 0, label='TX', color = 'darkred', animated = True)
    (HistoryLineTY,) = HistoryTXYZ.plot(0, 0, label='TY', color = 'darkgreen', animated = True)
    (HistoryLineTZ,) = HistoryTXYZ.plot(0, 0, label='TZ', color = 'darkblue', animated = True)
    HistoryTXYZ.set_xlim([-HistorySeconds, 0])
    HistoryTXYZ.set_ylim([-TXYZLimit_Nm, TXYZLimit_Nm])
    HistoryTXYZ.set_xlabel('Time (s)', color = 'white')
    HistoryTXYZ.set_ylabel('Torque (Nm)', color = 'white')
    HistoryTXYZ.set_facecolor('black')
    HistoryTXYZ.grid(True, linestyle='-.')
    HistoryTXYZ.tick_params(axis = 'both', 
                            which = 'both', 
                            color = 'white',
                            labelcolor = 'white', 
                            grid_color = 'grey', 
                            grid_linewidth = 0.3)
    HistoryTXYZ.annotate('Torque History', 
                          (0.5, 0.9), 
                          ha='center', 
                          va='center', 
                          xycoords = 'axes fraction',
                          fontsize=18,
                          color='darkgrey')

    PositionFXYZ = GraphSubPlotMosaic['PositionFXYZ']
    PositionLineFXYZ, = PositionFXYZ.plot(0, 0, label='PositionFXYZ', color = 'Orange', animated = True)
    PositionFXYZ.set_xlim([-FXYZLimit_N, FXYZLimit_N])
    PositionFXYZ.set_ylim([-FXYZLimit_N, FXYZLimit_N])
    PositionFXYZ.set_xlabel('Force X (N)', color = 'white')
    PositionFXYZ.set_ylabel('Force Y (N)', color = 'white')
    PositionFXYZ.set_facecolor('black')
    PositionFXYZ.grid(True, linestyle='-.')
    PositionFXYZ.tick_params(axis = 'both', 
                            which = 'both', 
                            color = 'white',
                            labelcolor = 'white', 
                            grid_color = 'grey', 
                            grid_linewidth = 0.3)
    PositionFXYZ.annotate('Force Position', 
                          (0.5, 0.9), 
                          ha='center', 
                          va='center', 
                          xycoords = 'axes fraction',
                          fontsize=18,
                          color='darkgrey')

    PositionTXYZ = GraphSubPlotMosaic['PositionTXYZ']
    PositionLineTXYZ, = PositionTXYZ.plot(0, 0, label='PositionTXYZ', color = 'Blue', animated = True)
    PositionTXYZ.set_xlim([-TXYZLimit_Nm, TXYZLimit_Nm])
    PositionTXYZ.set_ylim([-TXYZLimit_Nm, TXYZLimit_Nm])
    PositionTXYZ.set_xlabel('Torque X (Nm)', color = 'white')
    PositionTXYZ.set_ylabel('Torque Y (Nm)', color = 'white')
    PositionTXYZ.set_facecolor('black')
    PositionTXYZ.grid(True, linestyle='-.')
    PositionTXYZ.tick_params(axis = 'both', 
                            which = 'both', 
                            color = 'white',
                            labelcolor = 'white', 
                            grid_color = 'grey', 
                            grid_linewidth = 0.3)
    PositionTXYZ.annotate('Torque Position', 
                          (0.5, 0.9), 
                          ha='center', 
                          va='center', 
                          xycoords = 'axes fraction',
                          fontsize=18,
                          color='darkgrey')

    AngleTableRowLabels = ['Choice '+str(i) for i in range(8)]
    AngleTableColLabels = ['phi1'] + ['theta '+ str(i) for i in range(2,7,1)]

    AnglesSubfigAxes = AnglesSubfig.add_axes([0, 0, 1, 1])
    AnglesSubfigAxes.set_facecolor('black')
    AnglesSubfigTable = table.table(AnglesSubfigAxes, 
                        cellText = array(zeros((len(AngleTableRowLabels), len(AngleTableColLabels)))), 
                            bbox = [0.1, 0.1, 0.9, 0.9], 
                            edges = 'closed', 
                            rowLabels = AngleTableRowLabels, 
                            colLabels = AngleTableColLabels)
    
    for Cell in AnglesSubfigTable.get_children():
        Cell.set(color = 'black')
        Cell.set_text_props(color = 'white')

    plt.show(block=False)
    plt.pause(0.1)


    bg = CommandFig.canvas.copy_from_bbox(GraphSubfig.bbox)
    CommandFig.canvas.blit(CommandFig.bbox)
    
    return CommandFig, bg, PositionFXYZ, PositionTXYZ, HistoryLineFX, HistoryLineFY, HistoryLineFZ, HistoryLineTX, HistoryLineTY, HistoryLineTZ, PositionLineFXYZ, PositionLineTXYZ, GraphSubPlotMosaic, ButtonSliderSubfig, GraphSubfig, AnglesSubfigTable, SCol1Array, SCol0Array, BCol0Array, BCol1Array, BCol2Array, BCol3Array, QuitButton

def CreateButtons(ButtonSliderSubfig, ButtonTitle,ButtonXOffsetFromLeftWall):

    

    NButton = len(ButtonTitle)
    ButtonWidth = 0.07
    ButtonHeight = 0.03
    ButtonNormalColor = '0.25'
    ButtonHoverColor = 'red'
    ButtonSpacing = 0.9/(NButton+1)
    ButtonArray = [0]*NButton
    ButtonAxesArray = [0]*NButton
    for i in arange(NButton):
        ButtonAxesArray[i] = ButtonSliderSubfig.add_axes(([ButtonXOffsetFromLeftWall,1-(ButtonSpacing*(i+1)),ButtonWidth,ButtonHeight]))#x,y,w,h
        ButtonArray[i] = Button(ButtonAxesArray[i],ButtonTitle[i],image=None,color=ButtonNormalColor,hovercolor=ButtonHoverColor)

    return ButtonArray

def update_command_variables(SCol0Array, SCol1Array, CommandFig):
        
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
    RobotBytesToSend = pack('Qiiddddddddd', 
                            0xFF00AA55,
                            # MagicNumberS, 
                            StateValueS,
                            ErrorValueS,
                            PositionVectorS[0], PositionVectorS[1], PositionVectorS[2],
                            FTZS[0], FTZS[1], FTZS[2],
                            FTXS[0], FTXS[1], FTXS[2],
                            )
    
    
    
    return MagicNumberS, StateValueS, ErrorValueS, PositionVectorS, FTZS, FTXS, RobotBytesToSend

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
                )  = unpack('Qiiiiiiiiddddddddddddddd', BytesAddressPair[0])
                
            
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

class QuitIndex():
    def QuitFunc(self, event):
        print('quitting')
        plt.close("all")
        UDPRobotClientSocket.close()
        global QuitBool
        
        QuitBool = True
        # UDPRobotClientSocket.close()

class BCol0Index():
    def Button0(self, event):
        global BCol0Current
        BCol0Current=BCol0Title[0]
        try:
            UDPRobotClientSocket.sendto(RobotBytesToSend, RobotServerAddressPort)
            
            
            print(BCol0Title[0])
            print('Packet Sent:')
            print('Magic Number: {}'.format(MagicNumberS))
            print('State Variable: {}'.format(StateValueS))
            print('Error Value: {}'.format(ErrorValueS))
            print('Position Vector: {}'.format(PositionVectorS))
            print('FT-Z: {}'.format(FTZS))
            print('FT-X: {}'.format(FTXS))
            print('Sent: {}'.format(RobotBytesToSend))
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
        global BCol1Current, FTSocket, FTSocketAddress, FTPort
        BCol1Current=BCol1Title[0]
        bias(FTSocket, FTSocketAddress, FTPort)
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

  # Calculate the length of the vector.
  length = sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

  # Divide each component of the vector by the length.
  unit_vector = [vector[0] / length, vector[1] / length, vector[2] / length]

  return unit_vector

def get_FT_data(SensorConnected, FTSocket, FTSocketAddress, FTPort, FTData):
    
    if SensorConnected:
        request = b'\x12\x34\x00\x02\x00\x00\x00\x01'

        FTSocket.sendto(request,(FTSocketAddress, FTPort))
        NewFTData, addr = FTSocket.recvfrom(36)
    else:
        FX = sin(datetime.now().microsecond/1000000*2*pi)*10
        FY = sin(datetime.now().microsecond/1000000*2*pi+2*pi/3)*10
        FZ = sin(datetime.now().microsecond/1000000*2*pi+4*pi/3)*10
        TX = cos(datetime.now().microsecond/1000000*2*pi)
        TY = cos(datetime.now().microsecond/1000000*2*pi+2*pi/3)
        TZ = cos(datetime.now().microsecond/1000000*2*pi+4*pi/3)
        NewFTData = pack('>ffffff', FX, FY, FZ, TX, TY, TZ)
        
    return NewFTData
        
def process_FT_data(NewFTData, FTData, SensorConnected, CountsPerForceAndTorque):
    
    FTData = append(FTData, zeros((1,FTData.shape[1],FTData.shape[2])), axis = 0)
    
    FTData[FTData.shape[0]-1,0,:] = datetime.now()
    for i in range(0,6,1):
        if SensorConnected:
            FTData[FTData.shape[0]-1,i+1,0] = int.from_bytes(NewFTData[12+i*4:15+i*4],
                                           'big',signed=True
                                           )/CountsPerForceAndTorque*256
        else:

            FTData[FTData.shape[0]-1,i+1,0] = list(unpack('>ffffff',NewFTData))[i]
    return FTData

def recent_FT_data_chunk(FTData, HistorySeconds):
    

    # breakpoint()
    FTDataRecentHistory = None
    FTDataRecentHistoryIsNew = True
    RecentDataFinding = True
    
    NowDateTime = datetime.now()
    
    for Row in range(FTData.shape[0]-1,0,-1):
            RecordDateTime = FTData[Row,0,0]
            TimeGap = NowDateTime - RecordDateTime
            
            if TimeGap < timedelta(seconds = HistorySeconds):
                if FTDataRecentHistoryIsNew:
                    FTDataRecentHistoryIsNew = False
                    FTDataRecentHistory = array(zeros((1,8,2)), dtype = object)
                    FTDataRecentHistory[0,0:7,:] = FTData[Row,:,:]
                    FTDataRecentHistory[0,7,:] = -TimeGap.total_seconds()
                    
                else:
                    # AddTimeGap = append()
                    FTDataRecentHistory = append(FTDataRecentHistory, array(zeros((1,8,2)), dtype = object), axis = 0)
                    FTDataRecentHistory[FTDataRecentHistory.shape[0]-1,0:7,:] = FTData[Row,:,:]
                    FTDataRecentHistory[FTDataRecentHistory.shape[0]-1,7,:] = -TimeGap.total_seconds()
                    
            else: 
                
                continue
                
            
    return FTDataRecentHistory

def magnitude(vector):
    return sqrt(sum(square(vector)))

def normalizejointangles(array):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            while array[i][j] >= pi:
                array[i][j] = array[i][j] - 2*pi
            while array[i][j] <= -pi:
                array[i][j] = array[i][j] + 2*pi
    return array

def phi1(Choice, JointAngle, Frames, X7, Y7, s71, gamma1):
    S4 = Frames.loc[3,'JointOffset']
    S6 = Frames.loc[5,'JointOffset']
    S7 = Frames.loc[6,'JointOffset']
    a71 = Frames.loc[6,'LinkLength']
    A = -S6*Y7 + S7*s71
    B = -S6*X7 - a71
    phi1arccosArg = -S4/sqrt(square(A)+square(B))
    if Choice < 4:
        JointAngle[Choice,0] = arccos(phi1arccosArg) + arctan2(B,A) - gamma1
    else:
        JointAngle[Choice,0] = -arccos(phi1arccosArg) + arctan2(B,A) - gamma1
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def XYZ17(Choice, JointAngle, X7, Y7, Z7, c12, s12, c67, s67, c71, s71, gamma1):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    theta7 = JointAngle[Choice][6]
    c7 = cos(theta7)
    s7 = sin(theta7)
    
    BarX1 = s12*s1
    BarY1 = -(s71*c12 + c71*s12*c1)
    BarZ1 = c71*c12 - s71*s12*c1

    X17 = BarX1*c7 - BarY1*s7
    Y17 = c67*(BarX1*s7 + BarY1*c7) - s67*BarZ1
    Z17 = s67*(BarX1*s7 + BarY1*c7) - c67*BarZ1
    return X17, Y17, Z17        

def theta5(Choice, JointAngle, Z17):
    if Choice % 4 == 2 or Choice % 4 == 3:
        JointAngle[Choice, 4] = -arccos(Z17)
    else:
        JointAngle[Choice, 4] = arccos(Z17)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta6(Choice, JointAngle, X17, Y17):
    theta5 = JointAngle[Choice, 4]
    c6 = -X17/sin(theta5)
    s6 = Y17/sin(theta5)
    JointAngle[Choice, 5] = arctan2(s6, c6)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def XYZ671(Choice, JointAngle, c56, s56, c67, s67, c71, s71, c12, s12, gamma1):
    
    theta6 = JointAngle[Choice][5]
    c6 = cos(theta6)
    s6 = sin(theta6)
    
    X6 = s56*s6
    Y6 = -(s67*c56 + c67*s56*c6)
    Z6 = c67*c56 - s67*s56*c6
    
    theta7 = JointAngle[Choice][6]
    c7 = cos(theta7)
    s7 = sin(theta7)
    
    X67 = X6*c7 - Y6*s7
    Y67 = c71*(X6*s7 + Y6*c7) - s71*Z6
    Z67 = s71*(X6*s7 + Y6*s7) + c71*Z6
    
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    X671 = X67*c1 - Y67*s1
    Y671 = c12*(X67*s1 + Y67*c1) - s12*Z67  
    Z671 = s12*(X67*s1 + Y67*c1) - c12*Z67
    return X671, Y671, Z671

def XY71(Choice, JointAngle, gamma1, X7, Y7, Z7, c12, s12):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    X71 = X7*c1 - Y7*s1
    Y71 = c12*(X7*s1 + Y7*c1) - s12*Z7    
    return X71, Y71

def XYZ1(Choice, JointAngle, c12, s12, c71, s71, gamma1):
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    s1 = sin(theta1)
    
    X1 = s71*s1
    Y1 = -(s12*c71 + c12*s71*c1)
    Z1 = c12*c71 - s12*s71*c1
    return X1, Y1, Z1

def K(Choice, JointAngle, Frames, gamma1, X1, Y1, X71, Y71, X671, Y671):
    S1  = Frames.loc[0,'JointOffset']
    S5  = Frames.loc[4,'JointOffset']
    S6  = Frames.loc[5,'JointOffset']
    S7  = Frames.loc[6,'JointOffset']
    a71 = Frames.loc[6,'LinkLength']
    
    theta1 = JointAngle[Choice][0] + gamma1
    c1 = cos(theta1)
    
    K1 = -S5*X671 - S6*X71 - S7*X1 - a71*c1
    K2 = -S1 - S5*Y671 - S6*Y71 - S7*Y1
    return K1, K2

def theta3(Choice, JointAngle, Frames, K1, K2):
    a23 = Frames.loc[1,'LinkLength']
    a34 = Frames.loc[2,'LinkLength']
    
    A = (square(K1) + square(K2) - square(a23) - square(a34))/(2*a23*a34)
    
    if Choice % 2 == 0:
        JointAngle[Choice, 2] = arccos(A)
    else:
        JointAngle[Choice, 2] = -arccos(A)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta2(Choice, JointAngle, Frames, K1, K2):
    a23 = Frames.loc[1,'LinkLength']
    a34 = Frames.loc[2,'LinkLength']
    
    theta3 = JointAngle[Choice][2]
    c3 = cos(theta3)
    s3 = sin(theta3)
    
    A = K1/sqrt(square(a23 + a34*c3)+square(-a34*s3))
    B1 = (-a34*s3)
    B2 = (a23 + a34*c3)
    C = K2/sqrt(square(-a34*s3)+square(-a23 - a34*c3))
    D1 = (-a23 - a34*c3)
    D2 = (-a34)*s3
    
    theta2a =  arccos(A) + arctan2(B1, B2)
    theta2b = -arccos(A) + arctan2(B1, B2)
    theta2c =  arccos(C) + arctan2(D1, D2)
    theta2d = -arccos(C) + arctan2(D1, D2)
    
    if round(theta2a, 5) == round(theta2c, 5) or round(theta2a, 5) == round(theta2d, 5):
        JointAngle[Choice, 1] = theta2a
    elif round(theta2b, 5) == round(theta2c, 5) or round(theta2b, 5) == round(theta2d, 5):
        JointAngle[Choice, 1] = theta2b
    else:
        JointAngle[Choice, 1] = nan
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def theta4(Choice, JointAngle, X671, Y671, Z671):
    theta2 = JointAngle[Choice][1]
    c2 = cos(theta2)
    s2 = sin(theta2)
    
    c23 = 1
    s23 = 0
    
    X6712 = X671*c2-Y671*s2
    Y6712 = c23*(X671*s2 + Y671*c2) - s23*Z671
    Z6712 = s23*(X671*s2 + Y671*c2) - c23*Z671
    
    theta3 = JointAngle[Choice][2]
    c3 = cos(theta3)
    s3 = sin(theta3)
    
    c34 = 1
    s34 = 0
    
    X67123 = X6712*c3 - Y6712*s3
    Y67123 = c34*(X6712*s3 + Y6712*c3) - s34*Z6712
    
    JointAngle[Choice, 3] = arctan2(-X67123, -Y67123)
    JointAngle = normalizejointangles(JointAngle)
    return JointAngle

def inverse_kinematics(v_FPtool, v_FS6, v_Fa67):#0   1   2   3   4   5   6
    Frames = DataFrame(data = {'LinkLength': [0,         700,    900,    0,      0,      0,      0],     #a12 a23 a34 a45 a56 a67 a71
                               'TwistAngle': [3*pi/2,    0,      0,      3*pi/2, pi/2,   pi/2,   0],     #α12 α23 α34 α45 α56 α67 α71
                               'JointOffset':[0,         0,      0,      98,     145,    152.4,  0]})    #S1  S2  S3  S4  S5  S6  S7
    
    #ϕ1  θ2  θ3  θ4  θ5  θ6  θ7
    JointAngle = array(zeros((8,7))) #pose, joint                                  
    
    v_6Ptool    = array([20,         30,         50])
    # v_FPtool    = array([800,        800,        180])
    # v_FS6       = array([-0.5774,    0.5774,    0.5774])
    # v_Fa67      = array([ 0.4082,    0.8165,    -0.4082])
    
    v_FS1       = array([0, 0, 1])
    v_i         = array([1, 0, 0])
    v_j         = array([0, 1, 0])
    v_k         = array([0, 0, 1])
    
    v_FS7   = cross(v_Fa67, v_FS6)
    v_Fa71  = cross(v_FS7, v_FS1)/magnitude(cross(v_FS7, v_FS1))
    
    #α71
    c71 = dot(v_FS7, v_FS1)
    s71 = dot(cross(v_FS7, v_FS1), v_Fa71)
    Frames.loc[6,'TwistAngle'] = arctan2(s71, c71)
    
    #θ7
    c7 = dot(v_Fa67, v_Fa71)
    s7 = dot(cross(v_Fa67, v_Fa71), v_FS7)
    JointAngle[:,6] = arctan2(s7, c7)
    
    #γ1
    cgamma1 = dot(v_Fa71, v_i)
    sgamma1 = dot(cross(v_Fa71, v_i), v_FS1)
    gamma1 = arctan2(sgamma1, cgamma1)
    
    #S7, a71, S1
    v_FP6orig = v_FPtool - dot(v_6Ptool, v_i)*v_Fa67 - cross(dot(v_6Ptool, v_j)*v_FS6, v_Fa67) - dot(v_6Ptool,v_k)*v_FS6
        #S7
    Frames.loc[6,'JointOffset'] = dot(cross(v_FS1, v_FP6orig), v_Fa71)/s71
        #a71
    Frames.loc[6,'LinkLength']  = dot(cross(v_FP6orig, v_FS1), v_FS7) /s71
        #S1
    Frames.loc[0,'JointOffset'] = dot(cross(v_FP6orig, v_FS7), v_Fa71)/s71
    
    #X7, Y7, Z7
    c67 = dot(v_FS6, v_FS7)
    s67 = dot(cross(v_FS6, v_FS7), v_Fa67)
    X7 = s67*s7
    Y7 = -(s71*c67 + c71*s67*c7)
    Z7 = c71*c67 - s71*s67*c7
    
    for Choice in range(8):
        #ϕ1
        JointAngle = phi1(Choice, JointAngle, Frames, X7, Y7, s71, gamma1)
        
        c12 = 0
        s12 = -1
        X17, Y17, Z17 = XYZ17(Choice, JointAngle, X7, Y7, Z7, c12, s12, c67, s67, c71, s71, gamma1)
        
        #θ5
        JointAngle = theta5(Choice, JointAngle, Z17)
        
        #θ6
        JointAngle = theta6(Choice, JointAngle, X17, Y17)    
        
        c56 = 0
        s56 = 1
        X671, Y671, Z671 = XYZ671(Choice, JointAngle, c56, s56, c67, s67, c71, s71, c12, s12, gamma1)
        X71, Y71 = XY71(Choice, JointAngle, gamma1, X7, Y7, Z7, c12, s12)
        X1, Y1, Z1 = XYZ1(Choice, JointAngle, c12, s12, c71, s71, gamma1)
        K1, K2 = K(Choice, JointAngle, Frames, gamma1, X1, Y1, X71, Y71, X671, Y671)
        
        #θ3
        JointAngle = theta3(Choice, JointAngle, Frames, K1, K2)
        
        #θ2
        JointAngle = theta2(Choice, JointAngle, Frames, K1, K2)
    
        #θ4
        JointAngle = theta4(Choice, JointAngle, X671, Y671, Z671)
    
    return JointAngle

def bias(FTSocket, FTSocketAddress, FTPort):

    Bias = b'\x12\x34\x00\x42\x00\x00\x00\x00'
    FTSocket.sendto(Bias,(FTSocketAddress,FTPort))

def main():
    viridis = plt.cm.get_cmap('viridis', 12)
    
    #FT Figure Section
    global FTPort, SensorConnected, FTSocketAddress, CountsPerForceAndTorque
    FTPort = 49152
    SensorConnected = False
    FTSocketAddress = "192.168.1.20"
    CountsPerForceAndTorque = 1000000


    # FXYZLimit_N = 75
    # TXYZLimit_Nm = 4

    FXYZLimit_N = 75/10
    TXYZLimit_Nm = 4/10

    AveragingWeights = [1,0,0,0]
    
    global FTSocket
    FTSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    bias(FTSocket, FTSocketAddress, FTPort)
    

    # Constants
    SamplingRate_Hz = 1000  # Sampling rate of the simulated data [Hz]
    DAQInterval_ms = round(1000 / 100)  # [ms]
    ChartDrawInterval_ms = round(1000 / 50)  # [ms]

    #Command Figure Section
    use("Qt5agg")
    plt.ion()
    global QuitBool
    QuitBool = False
    
    HistorySeconds = 5
    CommandFig, bg, PositionFXYZ, PositionTXYZ, HistoryLineFX, HistoryLineFY, HistoryLineFZ, HistoryLineTX, HistoryLineTY, HistoryLineTZ, PositionLineFXYZ, PositionLineTXYZ, GraphSubPlotMosaic, ButtonSliderSubfig, GraphSubfig, AnglesSubfigTable, SCol1Array, SCol0Array, BCol0Array, BCol1Array, BCol2Array, BCol3Array, QuitButton = init_command_fig(HistorySeconds, FXYZLimit_N, TXYZLimit_Nm)

    global BCol0Current
    BCol0Current = 'BCol0CurrentButton'
    
    global BCol1Current
    BCol1Current = 'BCol1CurrentButton'
    
    global BCol2Current
    BCol2Current = 'BCol2CurrentButton'
    
    global BCol3Current
    BCol3Current = 'BCol3CurrentButton'
    
    global RobotServerAddressPort
    RobotServerAddressPort   = ("192.168.1.104", 23)
    
    global RobotServerBufferSize
    RobotServerBufferSize    = 1024
    
    localIP = '192.168.0.20'
    localPort = 5049
    # Create a UDP socket at client side
    
    global UDPRobotClientSocket
    UDPRobotClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # UDPRobotClientSocket.bind((localIP, localPort))

    FTData = array(zeros((1,7,2)), dtype = object)
    FTData[0,0,0] = datetime.now()
    
    v_FPtoolOld    = array([800,        800,        180])
    v_FS6Old       = array([-0.5774,    0.5774,    0.5774])
    v_Fa67Old      = array([ 0.4082,    0.8165,    -0.4082])
    JointAngleFirst = True
    
    PreviousSecond = datetime.now().second
    CurrentSecond = datetime.now().second
    Frames = 0
    
    JoingAngleCellRefreshing = False
    JointAngleCellRow = -1
    JointAngleCellCol = 0

    try:
        UDPRobotClientSocket.settimeout(0.05)
        while QuitBool == False:
            
            CurrentSecond = datetime.now().second
            if PreviousSecond != CurrentSecond:
                print(str(Frames) + " FPS")
                PreviousSecond = CurrentSecond
                Frames = 0
            else:
                Frames = Frames + 1
                
            CommandFig.canvas.restore_region(bg)

            global MagicNumberS, StateValueS, ErrorValueS, PositionVectorS, FTZS, FTXS, RobotBytesToSend
            MagicNumberS, StateValueS, ErrorValueS, PositionVectorS, FTZS, FTXS, RobotBytesToSend = update_command_variables(SCol0Array, SCol1Array, CommandFig)
            DataRecievedBool, DataRecievedList = recieve_robot_data()

            if DataRecievedBool:
                breakpoint()
                MagicNumberR = DataRecievedList[0]
                StateValueR = DataRecievedList[1]
                ErrorValueR = DataRecievedList[2]
                EncoderValueR = DataRecievedList[3]
                ThetaValueR = DataRecievedList[4]
                PositionVectorR = DataRecievedList[5]
                FTZR = DataRecievedList[6]
                FTXR = DataRecievedList[7]
            
            NewFTData = get_FT_data(SensorConnected, FTSocket, FTSocketAddress, FTPort, FTData)
            FTData = process_FT_data(NewFTData, FTData, SensorConnected, CountsPerForceAndTorque)
            FTDataRecentHistory = recent_FT_data_chunk(FTData, HistorySeconds)
            
            
            if FTDataRecentHistory is not None:
                HistoryLineFX.set_data(FTDataRecentHistory[:,7,0],FTDataRecentHistory[:,1,0])
                HistoryLineFY.set_data(FTDataRecentHistory[:,7,0],FTDataRecentHistory[:,2,0])
                HistoryLineFZ.set_data(FTDataRecentHistory[:,7,0],FTDataRecentHistory[:,3,0])
                HistoryLineTX.set_data(FTDataRecentHistory[:,7,0],FTDataRecentHistory[:,4,0])
                HistoryLineTY.set_data(FTDataRecentHistory[:,7,0],FTDataRecentHistory[:,5,0])
                HistoryLineTZ.set_data(FTDataRecentHistory[:,7,0],FTDataRecentHistory[:,6,0])
                
            PositionLineFXYZ.set_data(FTDataRecentHistory[:,1,0],FTDataRecentHistory[:,2,0])
            PositionLineTXYZ.set_data(FTDataRecentHistory[:,4,0],FTDataRecentHistory[:,5,0])
            
           
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
            
            v_FPtool    = array(PositionVectorS)
            v_FS6       = array(FTZS)
            v_Fa67      = array(FTXS)
            
            
            if not(array_equal(v_FPtool, v_FPtoolOld)) or (
                    not(array_equal(v_FS6, v_FS6Old))) or (
                    not(array_equal(v_Fa67, v_Fa67Old))) or (
                        JointAngleFirst == True) or (
                        JoingAngleCellRefreshing == True):
                
                if JoingAngleCellRefreshing == False:               
                    print("new angles")
                    JointAngleFirst = False
                    JointAngle = inverse_kinematics(v_FPtool, v_FS6, v_Fa67)
                    JointAngleDeg = rad2deg(JointAngle[:,0:6])
                    v_FPtoolOld = v_FPtool
                    v_FS6Old = v_FS6
                    v_Fa67Old = v_Fa67
                
                JoingAngleCellRefreshing = True


                # if JointAngleCellRow > 3:
                #     JointAngleCellRow = 0
                #     if JointAngleCellCol > 5:
                #         JointAngleCellCol = 0
                #     else: 
                #         JointAngleCellCol = JointAngleCellCol + 1
                # else: 
                #     JointAngleCellRow = JointAngleCellRow + 1
                    
                
                
                # print("("+str(JointAngleCellRow)+","+str(JointAngleCellCol)+")")
            
                # for CellRow in range(JointAngleDeg.shape[0]):
                #     for CellCol in range(JointAngleDeg.shape[1]):
                Cell = AnglesSubfigTable.properties()['celld'][JointAngleCellRow+1, JointAngleCellCol]
                CellValue = round(JointAngleDeg[JointAngleCellRow, JointAngleCellCol], 2)
                CellText = str(CellValue)
                Cell.set_text_props(text = CellText)
                
                if CellText != 'nan':
                    Cell.set(facecolor = viridis(CellValue/180))
                else:
                    Cell.set(facecolor = 'red')
                    
                # if JointAngleCellRow == 3 and (
                #    JointAngleCellCol == 5):
                #     JoingAngleCellRefreshing = False
                #     JointAngleCellRow = -1
                #     JointAngleCellCol = 0
                            
            CommandFig.canvas.restore_region(bg)
            GraphSubPlotMosaic['HistoryFXYZ'].draw_artist(HistoryLineFX)
            GraphSubPlotMosaic['HistoryFXYZ'].draw_artist(HistoryLineFY)
            GraphSubPlotMosaic['HistoryFXYZ'].draw_artist(HistoryLineFZ)
            GraphSubPlotMosaic['HistoryTXYZ'].draw_artist(HistoryLineTX)
            GraphSubPlotMosaic['HistoryTXYZ'].draw_artist(HistoryLineTY)
            GraphSubPlotMosaic['HistoryTXYZ'].draw_artist(HistoryLineTZ)
            GraphSubPlotMosaic['PositionFXYZ'].draw_artist(PositionLineFXYZ)
            GraphSubPlotMosaic['PositionTXYZ'].draw_artist(PositionLineTXYZ)
            
            CommandFig.canvas.blit(CommandFig.bbox)
            
            CommandFig.canvas.flush_events()
            
    except KeyboardInterrupt:
        UDPRobotClientSocket.close()
        
if (__name__ == '__main__'): 
    main()