import dearpygui.dearpygui as dpg
from GrandCentralDispatch import grand_central_dispatch
from FTCommunications import get_FTLimits
from RobotCommunications import query_robot_state
from RealtimeDataProcessing import MakeSamplingButtons
import numpy as np

from GUIhelp import  _create_dynamic_textures, _create_static_textures

def logging_slider(VectorName, Units, default_value, min_value, max_value):
    SliderText = VectorName
    if Units is not None:
        SliderText = SliderText +" ("+Units+")"
    dpg.add_slider_float(tag='Log '+VectorName,label="Log "+VectorName, default_value=default_value, min_value=min_value, max_value=max_value,  format="%.3f", callback=grand_central_dispatch)



def VectorHelper(VectorName, Units, default_value, min_value, max_value, min_delta=0, max_delta=0, step=None, UDPRobotClientSocket=None, RobotServerAddressPort=None):
    with dpg.group():
        SliderText = VectorName
        if Units is not None:
            SliderText = SliderText +" ("+Units+")"
        with  dpg.group(horizontal=True):    
            dpg.add_text(SliderText+ '          ')
            dpg.add_button(tag='Bias Vector '+VectorName, label='Bias '+VectorName)
        
        if step is None:
            dpg.add_input_float(tag='Input '+VectorName,label="Input "+VectorName, default_value=default_value, min_value=min_value, max_value=max_value,  format="%.3f", on_enter=True, callback =lambda: query_robot_state(UDPRobotClientSocket, RobotServerAddressPort))
        else:
            dpg.add_input_float(tag='Input '+VectorName,label="Input "+VectorName, default_value=default_value, min_value=min_value, max_value=max_value,  format="%.0f", step=step, on_enter=True, callback=lambda: query_robot_state(UDPRobotClientSocket, RobotServerAddressPort))
        
        # dpg.add_input_float(tag='Input '+VectorName, default_value=1,callback=lambda: p('Input '+VectorName, None, None, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort))
        dpg.add_slider_float(tag='Robot '+VectorName,label="Robot "+VectorName, default_value=np.nan, min_value=min_value, max_value=max_value, format="%.3f")
        if not (min_delta == 0 and max_delta == 0):
            dpg.add_slider_float(tag='Delta '+VectorName,label="Delta "+VectorName, default_value=np.nan, min_value=min_delta, max_value=max_delta, format="%.3f")
        

def PlotHelper(PlotLabel,
               XAxis, XAxisLetter, XAxisUnits, XAxisMin, XAxisMax,
               YAxis, YAxisLetter, YAxisUnits, YAxisMin, YAxisMax):
    
    with dpg.plot(label=PlotLabel, fit_button=1):
        # REQUIRED: create x and y axes
        dpg.set_axis_limits(dpg.add_plot_axis(dpg.mvXAxis, label=XAxis+" ("+XAxisUnits+")"), XAxisMin, XAxisMax)
        dpg.set_axis_limits(dpg.add_plot_axis(dpg.mvYAxis, label=YAxis+" ("+YAxisUnits+")", tag=YAxis+" VS "+XAxis+" Y"), YAxisMin, YAxisMax)
    
        # series belong to a y axis
        
        if XAxis == 'Time':
            dpg.add_plot_legend()
            for Axis, Color in [['X','Red'],['Y','Green'],['Z','Blue']]:
                # breakpoint()
                dpg.add_line_series([], [], label=Axis, tag=YAxis+" VS "+XAxis+" "+Axis+" Line", parent=YAxis+" VS "+XAxis+" Y")
                dpg.bind_item_theme(YAxis+" VS "+XAxis+" "+Axis+" Line", Color+" Plot Line")

        else:
            Color = 'White'
            dpg.add_line_series([], [], label="a", tag=YAxis+" VS "+XAxis+" Line", parent=YAxis+" VS "+XAxis+" Y")
            dpg.bind_item_theme(YAxis+" VS "+XAxis+" Line", Color+" Plot Line")
            dpg.add_scatter_series([], [], label="a", tag=YAxis+" VS "+XAxis+" Marker", parent=YAxis+" VS "+XAxis+" Y")

def show(UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize):
    
    # dpg.set_primary_window('Primary', True)
    # dpg.set_item_focus()
    
    dpg.set_global_font_scale(1.2)
    dpg.add_texture_registry(label="Demo Texture Container", tag="__demo_texture_container")
    dpg.add_colormap_registry(label="Demo Colormap Registry", tag="__demo_colormap_registry")

    with dpg.theme(tag="__demo_hyperlinkTheme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [29, 151, 236, 25])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [29, 151, 236])

    
    _create_static_textures()
    _create_dynamic_textures()
    
    with dpg.window(label="Info Window", width=425, height=200, pos=(1500, 850), tag="Info Window"):
        # ColumnWidth = dpg.get_item_width('Robot Control')/3*0.95
        RowHeight = dpg.get_item_height('Info Window')/3*0.95
        with dpg.collapsing_header(label="Most Recent Info", default_open =True):
            with dpg.group(height=RowHeight):
                dpg.add_text('', tag='Past Info 0')
        with dpg.collapsing_header(label="Past Info", default_open =True):
            with dpg.group(height=RowHeight*2):
                dpg.add_text('', tag='Past Info 1')
                dpg.add_text('', tag='Past Info 2')
                dpg.add_text('', tag='Past Info 3')
                dpg.add_text('', tag='Past Info 4')

    with dpg.window(label="Robot Control", width=850, height=1000, pos=(0, 0), tag="Robot Control"):
        ColumnWidth = dpg.get_item_width('Robot Control')/3*0.95
        RowHeight = dpg.get_item_height('Robot Control')/8*0.95
        with dpg.collapsing_header(label="Buttons", default_open =True):
            with dpg.group(horizontal=True, height=RowHeight):
                dpg.add_button(label="ESTOP", tag='ESTOP', callback=lambda:grand_central_dispatch('ESTOP',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize), width=200)
                dpg.add_button(label="Breakpoint", tag='BP', callback=grand_central_dispatch)
                dpg.add_button(label="F/T Bias", tag='Bias', callback=grand_central_dispatch)
                dpg.add_button(label="Robot Command \nBias", tag='Bias Vector', callback=grand_central_dispatch)
                # dpg.add_button(label="Send To Robot", tag='Send_To_Robot',callback=button_send_to_robot)
                with dpg.group():
                    dpg.add_text('Send To Robot')
                    dpg.add_radio_button(items=['False','True', 'Continious'], default_value='False',label="Send To Robot", tag='Send_To_Robot')
                    dpg.add_text('FPS: 0', tag='FPS Text')
                with dpg.group():
                    dpg.add_text('Abs Delta:')
                    dpg.add_text('',tag='Abs Delta')
                    
        
        with dpg.collapsing_header(label="Position Input/Current", default_open =True):
            with dpg.group(horizontal=True, height=RowHeight):
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="PX", Units="mm", default_value=np.nan, min_value=-1000, max_value=1000, min_delta=-10, max_delta=10, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="PY", Units="mm", default_value=np.nan, min_value=-1000, max_value=1000, min_delta=-10, max_delta=10, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="PZ", Units="mm", default_value=np.nan, min_value=-1000, max_value=1000, min_delta=-10, max_delta=10, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                    
        with dpg.collapsing_header(label="FTX Input/Current", default_open =True):
            with dpg.group(horizontal=True, height=RowHeight):
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="FTX X", Units=None, default_value=1, min_value=-1, max_value=1, min_delta=-0.1, max_delta=0.1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="FTX Y", Units=None, default_value=0, min_value=-1, max_value=1, min_delta=-0.1, max_delta=0.1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="FTX Z", Units=None, default_value=0, min_value=-1, max_value=1, min_delta=-0.1, max_delta=0.1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                    
        with dpg.collapsing_header(label="FTZ Input/Current", default_open =True):
            with dpg.group(horizontal=True, height=RowHeight):
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="FTZ X", Units=None, default_value=0, min_value=-1, max_value=1, min_delta=-0.1, max_delta=0.1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="FTZ Y", Units=None, default_value=0, min_value=-1, max_value=1, min_delta=-0.1, max_delta=0.1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                with dpg.child_window(width=ColumnWidth):
                    VectorHelper(VectorName="FTZ Z", Units=None, default_value=1, min_value=-1, max_value=1, min_delta=-0.1, max_delta=0.1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
        
        with dpg.collapsing_header(label="State and Error Input/Current", default_open =True):
            with dpg.group(horizontal=True, height=RowHeight*2.5):
                with dpg.child_window(width=ColumnWidth*1.5):
                    dpg.add_text('State')
                    VectorHelper(VectorName="State Value", Units=None, default_value=0, min_value=0, max_value=10, min_delta=0, max_delta=0, step=1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                    dpg.add_text('0: NoOp')
                    dpg.add_text('1: EMERGENCY STOP')
                    dpg.add_text('2: Position Command')
                    dpg.add_text('3: Position Query')
                with dpg.child_window(width=ColumnWidth*1.5):
                    dpg.add_text('Error')
                    VectorHelper(VectorName="Error Value", Units=None, default_value=0, min_value=0, max_value=10, min_delta=0, max_delta=0, step=1, UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort)
                    dpg.add_text('0: No Error')
                    dpg.add_text('1: Magic Number Error')
                    dpg.add_text('2: Invalid Encoder Value(s) Recieved')
                    dpg.add_text('3: Invalid Theta Value(s) received')
                    dpg.add_text('4: Invalid Position Vector received')
                    dpg.add_text('5: Invalid FT-z Unit Vector received')
                    dpg.add_text('6: Invalid FT-x Unit Vector received')
        
    with dpg.window(label="Sampling Control", width=875, height=700, pos=(0, 325), tag="Sampling Control"):

        from SurfaceSampling import safe_position_grid_and_names
        SafeOriginXYZ = [0, 0, 1000]
        SafePositionGridAndNames = safe_position_grid_and_names(SafeOriginXYZ)
        
        RowHeight = 80
        with dpg.group(horizontal=True):
            with dpg.group():
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_button(label="Set Position \nAs Safe Origin", tag='Sampling Set Safe Origin', callback=lambda:grand_central_dispatch('Sampling Set Safe Origin',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize), width=dpg.get_item_width('Sampling Control')/7, height=RowHeight/2)
                        dpg.add_button(label="Unsafe Height", tag='Sampling Set Unsafe Height', callback=lambda:grand_central_dispatch('Sampling Set Unsafe Height',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize), width=dpg.get_item_width('Sampling Control')/7, height=RowHeight/2)
                    
                    with dpg.group():
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Immediate Z\nMove Up", tag='Immediate Z Move Up', callback=lambda:grand_central_dispatch('Immediate Z Move Up',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize), width=dpg.get_item_width('Sampling Control')/7, height=RowHeight/2)
                            dpg.add_button(label="Immediate Z\nMove Down", tag='Immediate Z Move Down', callback=lambda:grand_central_dispatch('Immediate Z Move Down',None,None,UDPRobotClientSocket=UDPRobotClientSocket, RobotServerAddressPort=RobotServerAddressPort, RobotServerBufferSize=RobotServerBufferSize), width=dpg.get_item_width('Sampling Control')/7, height=RowHeight/2)
                        dpg.add_input_float(tag='Immediate Z Move Step', default_value=0.1, min_value=0, max_value=10,  format="%.6f", step=0.1, width=dpg.get_item_width('Sampling Control')/3.5)
                    
                with dpg.group(horizontal=True, height=RowHeight):
                    with dpg.group():
                        dpg.add_text('Safe Z')
                        dpg.add_input_float(tag='Safe Z', default_value=np.nan, min_value=0, max_value=10,  format="%.3f", step=0.001, width=dpg.get_item_width('Sampling Control')/7)
                    with dpg.group():
                        dpg.add_text('Unsafe Z')
                        dpg.add_input_float(tag='Unsafe Z', default_value=np.nan, min_value=0, max_value=10,  format="%.3f", step=0.001, width=dpg.get_item_width('Sampling Control')/7)
                    with dpg.group():
                        dpg.add_text('Current Point: ', tag='Sampling Current Point')
                        
            with dpg.group(horizontal=True, width=dpg.get_item_width('Sampling Control')/4):
                with dpg.group():
                    dpg.add_text('Auto Decend')
                    dpg.add_radio_button(items=['False','Send Goto Start','Await 0 Delta','True','Decending'], default_value='False',label="Auto Decend", tag='Auto Decend')
                with dpg.group():
                    dpg.add_text('Log Data')
                    dpg.add_radio_button(items=['False','True','Auto'], default_value='False',label="Log Data 2", tag='LogData2', callback=grand_central_dispatch)
                
                with dpg.group():
                    dpg.add_text('FTZ In Range')
                    dpg.add_radio_button(items=['False','True'], default_value='False',label="FTZ In Range", tag='FTZ In Range')
                
                with dpg.group():
                    dpg.add_text('Auto Ascend')
                    dpg.add_radio_button(items=['False','True','Ascending'], default_value='False',label="Auto Ascend", tag='Auto Ascend')
        with dpg.group(tag="Sampling Goto Buttons"):
            MakeSamplingButtons(SafePositionGridAndNames, UDPRobotClientSocket, RobotServerAddressPort, RobotServerBufferSize)
                        
    with dpg.window(label="Robot Angles (Command | Delta)", width=1000, height=250, pos=(850, 0), tag="Robot Angles"):
        with dpg.table(tag="Joint Angles", header_row=True, resizable=True, delay_search=True, row_background=True,
                    borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="phi 1")
            dpg.add_table_column(label="")
            dpg.add_table_column(label="theta 2")
            dpg.add_table_column(label="")
            dpg.add_table_column(label="theta 3")
            dpg.add_table_column(label="")
            dpg.add_table_column(label="theta 4")
            dpg.add_table_column(label="")
            dpg.add_table_column(label="theta 5")
            dpg.add_table_column(label="")
            dpg.add_table_column(label="theta 6")
            dpg.add_table_column(label="")
            
            for i in range(8):
                with dpg.table_row():
                    for j in range(8):
                        dpg.add_text("invalid", tag=f"{i},{j} Command")
                        dpg.add_text("invalid", tag=f"{i},{j} Delta")
                    
                        
    with dpg.window(label="Force/Torque Graphs", tag="Force/Torque Graphs", width=650, height=800, pos=(850, 250)):
        
        with dpg.theme(tag="Red Plot Line"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0), category=dpg.mvThemeCat_Plots)
        with dpg.theme(tag="Green Plot Line"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0), category=dpg.mvThemeCat_Plots)
        with dpg.theme(tag="Blue Plot Line"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots)
        with dpg.theme(tag="White Plot Line"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255), category=dpg.mvThemeCat_Plots)
        
        
        
        ColumnWidth = dpg.get_item_width('Force/Torque Graphs')/2*0.95
        RowHeight = dpg.get_item_height('Force/Torque Graphs')/2*0.95
        with dpg.group(horizontal=True, height=RowHeight):
            with dpg.group(width=ColumnWidth):
                PlotHelper("Force History",
                            'Time', 't', 's', -5, 0,
                            'Force', 'F', 'N', -6, 6)
            with dpg.group(width=ColumnWidth):
                # breakpoint()
                PlotHelper("Torque History",
                            'Time', 't', 's', -5, 0,
                            'Torque', 'T', 'Nm', -0.4, 0.4)
                
        with dpg.group(horizontal=True, height=RowHeight):
            with dpg.group(width=ColumnWidth):
                # breakpoint()
                PlotHelper("Force Position",
                            'Force X', 'F', 'N', -6, 6,
                            'Force Y', 'F', 'N', -6, 6)
            with dpg.group(width=ColumnWidth):
                PlotHelper("Torque Position",
                            'Torque X', 'T', 'Nm', -0.4, 0.4,
                            'Torque Y', 'T', 'Nm', -0.4, 0.4)
                
    with dpg.window(label="Data Logging", width=450, height=650, pos=(1500, 250), tag="Data Logging"):
        # ColumnWidth = dpg.get_item_width('Robot Control')/3*0.95
        RowHeight = dpg.get_item_height('Robot Control')/8*0.95
        with dpg.collapsing_header(label="Buttons", default_open =True):
            with dpg.group(horizontal=True, height=RowHeight):
                dpg.add_radio_button(items=['False','True','Continious'], default_value='False',label="Log Data", tag='LogData', callback=grand_central_dispatch)
                dpg.add_button(label="Open Data", tag='OpenData', callback=grand_central_dispatch)
        with dpg.collapsing_header(label="Data", default_open =True):    
                with dpg.group(horizontal=True):
                    with dpg.group(width = 100, tag = 'Logging Group 1'):
                        FXYZLimit_N, TXYZLimit_Nm = get_FTLimits()
                        dpg.add_input_text(label="Logging Note", tag = "Logging Note", hint="Logging Note")
                        dpg.add_text('DateTime', tag='Log DateTime')
                        logging_slider(VectorName="FX", Units="N", default_value=np.nan, min_value=-FXYZLimit_N, max_value=FXYZLimit_N)
                        logging_slider(VectorName="FY", Units="N", default_value=np.nan, min_value=-FXYZLimit_N, max_value=FXYZLimit_N)
                        logging_slider(VectorName="FZ", Units="N", default_value=np.nan, min_value=-FXYZLimit_N, max_value=FXYZLimit_N)
                        logging_slider(VectorName="TX", Units="Nm", default_value=np.nan, min_value=-TXYZLimit_Nm, max_value=TXYZLimit_Nm)
                        logging_slider(VectorName="TY", Units="Nm", default_value=np.nan, min_value=-TXYZLimit_Nm, max_value=TXYZLimit_Nm)
                        logging_slider(VectorName="TZ", Units="Nm", default_value=np.nan, min_value=-TXYZLimit_Nm, max_value=TXYZLimit_Nm)
                        
                        logging_slider(VectorName="PX", Units="mm", default_value=np.nan, min_value=-1000, max_value=1000)
                        logging_slider(VectorName="PY", Units="mm", default_value=np.nan, min_value=-1000, max_value=1000)
                        logging_slider(VectorName="PZ", Units="mm", default_value=np.nan, min_value=-1000, max_value=1000)
                        logging_slider(VectorName="FTX X", Units=None, default_value=np.nan, min_value=-1, max_value=1)
                        logging_slider(VectorName="FTX Y", Units=None, default_value=np.nan, min_value=-1, max_value=1)
                        logging_slider(VectorName="FTX Z", Units=None, default_value=np.nan, min_value=-1, max_value=1)
                        logging_slider(VectorName="FTZ X", Units=None, default_value=np.nan, min_value=-1, max_value=1)
                        logging_slider(VectorName="FTZ Y", Units=None, default_value=np.nan, min_value=-1, max_value=1)
                        logging_slider(VectorName="FTZ Z", Units=None, default_value=np.nan, min_value=-1, max_value=1)
                    with dpg.group(width = 100, tag = 'Logging Group 2'):
                        # EncoderValueR ThetaValueR
                        for i in range(6):
                            logging_slider(VectorName="Encoder "+str(i+1), Units=None, default_value=np.nan, min_value=-10000, max_value=10000)
                        for i in range(6):
                            logging_slider(VectorName="Theta "+str(i+1), Units=None, default_value=np.nan, min_value=-np.pi*2, max_value=np.pi*2)