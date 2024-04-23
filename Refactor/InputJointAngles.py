import dearpygui.dearpygui as dpg
def input_joint_angles():
    PositionVectorS = [dpg.get_value('Input PX'),
                       dpg.get_value('Input PY'),
                       dpg.get_value('Input PZ')]
    FTZS = [dpg.get_value('Input FTZ X'),
            dpg.get_value('Input FTZ Y'),
            dpg.get_value('Input FTZ Z')]
    
    FTXS = [dpg.get_value('Input FTX X'),
            dpg.get_value('Input FTX Y'),
            dpg.get_value('Input FTX Z')]
    return PositionVectorS, FTZS, FTXS