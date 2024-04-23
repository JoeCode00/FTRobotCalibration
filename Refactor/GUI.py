import dearpygui.dearpygui as dpg
from GUI_Setup import show
from RobotCommunications import unpack_robot_data, send_robot_data, get_robot_data, get_RobotServerBufferSize, setup_robot_socket, get_RobotServerAddressPort, must_get_robot_state
from FTCommunications import setup_socket, get_FT_data, bias, get_FTLimits
from InverseKinematics import unit_vector, joint_angle_updater
from RealtimeDataProcessing import process_FT_data, FT_graph_updater, robot_state_delta_updater, bias_robot_vector, absolute_scalar_delta
from InputJointAngles import input_joint_angles 
from datetime import datetime
from GrandCentralDispatch import info, grand_central_dispatch
from FPS import FPS_counter
from Logging import data_logger_updater, make_log_entry


import win32con
import win32gui
import numpy as np
import pandas as pd
import os

def main():
    SensorConnected = True # XXX
    FTSamplingLowerLimit = 1 # XXX N
    
    RobotServerBufferSize    = get_RobotServerBufferSize()
    UDPRobotClientSocket = setup_robot_socket()
    RobotServerAddressPort = get_RobotServerAddressPort()
    
    dpg.create_context()
    dpg.create_viewport(title='Joseph Research GUI', width=1920, height=1080)
    show(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    hwnd = win32gui.FindWindow('Joseph Research GUI', None)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 300, 200, 0)
    info(sender='System', app_data='Startup')
    
    FTPort = 49152
    FTSocketAddress = "192.168.1.20"
    CountsPerForceAndTorque = 1000000
    FXYZLimit_N, TXYZLimit_Nm = get_FTLimits()
    
    FTSocket = setup_socket()
    bias(FTSocket, FTSocketAddress, FTPort)
    FTData = np.array(np.zeros((300,8,2)), dtype = object)
    FTData[0,0,0] = datetime.now()
    
    LoggingColumns = [dpg.get_item_alias(item) for item 
                      in dpg.get_item_children('Logging Group 1')[1][1:]] + [dpg.get_item_alias(item) for item 
                                        in dpg.get_item_children('Logging Group 2')[1][1:]]

    LoggingDF = pd.DataFrame(columns = LoggingColumns)
    
    MagicNumberR = None
    StateValueR = None
    ErrorValueR = None
    EncoderValueR = None
    ThetaValueR = None
    PositionVectorR = None
    FTZR = None
    FTXR = None
    
    Frames = 0
    PreviousSecond = datetime.now().second
    
    
    
    
    FirstRun = True
    while dpg.is_dearpygui_running():
        try:
            Frames, CurrentSecond = FPS_counter(Frames, PreviousSecond)
            PreviousSecond = CurrentSecond
            
            # if Frames == 0 and (datetime.now().second == 0 or datetime.now().second == 30):
                # query_robot_state(UDPRobotClientSocket, RobotServerAddressPort)
            
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            MagicNumberR = None
            if dpg.get_value('Send_To_Robot') == 'True' or dpg.get_value('Send_To_Robot') == 'Continious' or FirstRun:
                send_robot_data(UDPRobotClientSocket, RobotServerAddressPort)
                
                if dpg.get_value('Send_To_Robot') == 'True':
                    dpg.set_value('Send_To_Robot', 'False')
                
            BytesAddressPair = get_robot_data(UDPRobotClientSocket, RobotServerBufferSize)
            
            if BytesAddressPair is not None or FirstRun:
                try:
                    MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = unpack_robot_data(BytesAddressPair)
                    # breakpoint()
                    # grand_central_dispatch('Bias Vector',None,None, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                    # info(sender='Robot Com', app_data='Data Rec')
                except:
                    False
            
            
            robot_state_delta_updater(StateValueR, ErrorValueR, PositionVectorR, FTZR, FTXR)
            
            NewFTData = get_FT_data(SensorConnected, FTSocket, FTSocketAddress, FTPort)
            FTData = process_FT_data(FTData, NewFTData, SensorConnected, CountsPerForceAndTorque)
            
            FT_graph_updater(FTData)
            
            FTX = FTData[0,1,0]
            FTY = FTData[0,2,0]
            FTZ = FTData[0,3,0]
            FTPythag = np.sqrt(FTX**2 + FTY**2 + FTZ**2)
            
            if FTPythag > FTSamplingLowerLimit:
                dpg.set_value('FTZ In Range','True')
            elif dpg.get_value('FTZ In Range') == 'True':
                dpg.set_value('FTZ In Range','False')
                
            
            LoggingNote = None
            PositionVectorS, FTZS, FTXS = input_joint_angles()
            FTZS = unit_vector(FTZS)
            FTXS = unit_vector(FTXS)
        
            # joint_angle_updater(PositionVectorS, FTZS, FTXS, PositionVectorR, FTZR, FTXR)
            if ThetaValueR is not None:
                joint_angle_updater(PositionVectorS, FTZS, FTXS, ThetaValueR)
                
            if FirstRun:
                bias_robot_vector('Bias Vector', Log=False)
                
            data_logger_updater(LoggingNote, FTData, EncoderValueR, ThetaValueR, PositionVectorS, FTZS, FTXS, PositionVectorR, FTZR, FTXR)
            
            if dpg.get_value('LogData') == 'True' or dpg.get_value('LogData') == 'Continious':
                make_log_entry(LoggingDF)
                if dpg.get_value('LogData') == 'True':
                    dpg.set_value('LogData', 'False')
                    
            if dpg.get_value('LogData2') == 'True':
                if dpg.get_value('FTZ In Range') == 'True':
                    make_log_entry(LoggingDF)
                else:
                    info(sender='ERROR', app_data='FT Not In Sample Range')
                dpg.set_value('LogData2', 'False')
            
            elif  dpg.get_value('LogData2') == 'Auto':
                if dpg.get_value('FTZ In Range') == 'True':
                    make_log_entry(LoggingDF)
                    dpg.set_value('LogData2', 'False')
            
            if dpg.get_value('Auto Decend') == 'Send Goto Start':
                send_robot_data(UDPRobotClientSocket, RobotServerAddressPort)
                dpg.set_value('Auto Decend', 'Await 0 Delta')
            
            if dpg.get_value('Auto Decend') == 'Await 0 Delta':
                AbsoluteScalarDelta = absolute_scalar_delta()   
                if AbsoluteScalarDelta <= 0.001:
                    dpg.set_value('Auto Decend', 'True')
                
            if dpg.get_value('Auto Decend') == 'True' or dpg.get_value('Auto Decend') == 'Decending':
                # breakpoint()
                if dpg.get_value('Auto Decend') == 'True':
                    bias(FTSocket, FTSocketAddress, FTPort)
                    dpg.set_value('LogData2', 'Auto')
                    dpg.set_value('Auto Decend', 'Decending')
                    
                if dpg.get_value('Auto Decend') == 'Decending':
                    MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = must_get_robot_state(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
                    RobotCurrentZ = PositionVectorR[2]
                    if RobotCurrentZ <= dpg.get_value('Safe Z'):
                        dpg.set_value('Immediate Z Move Step', 0.05)
                    if RobotCurrentZ <= dpg.get_value('Unsafe Z'):
                        dpg.set_value('Immediate Z Move Step', 0.001)   
                    
                    if dpg.get_value('FTZ In Range') == 'False':
                        # breakpoint()
                        grand_central_dispatch('Immediate Z Move Down',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize)
                    else:
                        dpg.set_value('Auto Decend', 'False')
                        dpg.set_value('Auto Ascend', 'True')
                        
            if dpg.get_value('Auto Ascend') == 'True' or dpg.get_value('Auto Ascend') == 'Ascending':
                # breakpoint()
                if dpg.get_value('Auto Ascend') == 'True':
                    dpg.set_value('Immediate Z Move Step', 0.1)
                    dpg.set_value('Auto Ascend', 'Ascending')
                    
                if dpg.get_value('Auto Ascend') == 'Ascending':
                    MagicNumberR, StateValueR, ErrorValueR, EncoderValueR, ThetaValueR, PositionVectorR, FTZR, FTXR = must_get_robot_state(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
                    RobotCurrentZ = PositionVectorR[2]

                    if RobotCurrentZ < dpg.get_value('Safe Z'):
                        grand_central_dispatch('Immediate Z Move Up',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize)
                    else:
                        dpg.set_value('Auto Ascend', 'False')
                    
            dpg.render_dearpygui_frame()
            FirstRun = False
        except Exception as e:
            info(sender='ERROR', app_data=e)
    
    
    try:
        FileName = [s for s in LoggingDF.index.to_list() if s != ''][0].replace(':','').replace('.','')
    except:
        FileName = datetime.now().strftime('%Y-%M-%dT%H%M%S')
        
    FolderPath = 'C:\\Users\\Joe\\OneDrive - University of Florida\\Research\\Data\\'
    
    while FileName in os.listdir(FolderPath):
        FileName = FileName + ' (New)'
        
    FilePath = 'C:\\Users\\Joe\\OneDrive - University of Florida\\Research\\Data\\'+FileName+'.xlsx'
    
    try:
        LoggingDF.to_excel(FilePath)
        print('Saved at '+FilePath)
    except Exception as e:
        print('ERROR SAVING')
        print(e)
        breakpoint()
        print('ERROR SAVING')
        
    dpg.destroy_context()
    
if (__name__ == '__main__'): 
    main()
