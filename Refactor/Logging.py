import dearpygui.dearpygui as dpg
from GrandCentralDispatch import info
def data_logger_updater(LoggingNote, FTData, EncoderValueR, ThetaValueR, PositionVectorS, FTZS, FTXS, PositionVectorR, FTZR, FTXR):
    FTDataToLog = FTData[0,:,0]
    Timestamp = FTDataToLog[0].isoformat()
    
    dpg.set_value('Log DateTime', Timestamp)
    if LoggingNote is not None:
        dpg.set_value("Logging Note", LoggingNote)
    
    dpg.set_value("Log FX", FTDataToLog[1])
    dpg.set_value("Log FY", FTDataToLog[2])
    dpg.set_value("Log FZ", FTDataToLog[3])
    dpg.set_value("Log TX", FTDataToLog[4])
    dpg.set_value("Log TY", FTDataToLog[5])
    dpg.set_value("Log TZ", FTDataToLog[6])
    
    if EncoderValueR is not None:
        for i in range(6):
            dpg.set_value("Log Encoder "+str(i+1), EncoderValueR[i])
            dpg.set_value("Log Theta "+str(i+1), ThetaValueR[i])
        dpg.set_value("Log PX", PositionVectorR[0])
        dpg.set_value("Log PY", PositionVectorR[1])
        dpg.set_value("Log PZ", PositionVectorR[2])
        dpg.set_value("Log FTX X", FTXR[0])
        dpg.set_value("Log FTX Y", FTXR[1])
        dpg.set_value("Log FTX Z", FTXR[2])
        dpg.set_value("Log FTZ X", FTZR[0])
        dpg.set_value("Log FTZ Y", FTZR[1])
        dpg.set_value("Log FTZ Z", FTZR[2])    
        
def make_log_entry(LoggingDF):
    LoggingGroup1 = dpg.get_item_children('Logging Group 1')[1]
    LoggingRow = dpg.get_value(LoggingGroup1[0])
    
    if LoggingRow == '':
        LoggingRow = dpg.get_value(LoggingGroup1[1])

    if LoggingRow in LoggingDF.index.to_list():
        LoggingRow = LoggingRow + ' '+str(LoggingDF.index.to_list().count(LoggingRow))
        
    for item in LoggingGroup1[1:]:
        LoggingDF.loc[LoggingRow, dpg.get_item_alias(item)] = dpg.get_value(item)
        
    LoggingGroup2 = dpg.get_item_children('Logging Group 2')[1]
    
    for item in LoggingGroup2[0:]:
        LoggingDF.loc[LoggingRow, dpg.get_item_alias(item)] = dpg.get_value(item)    
        
    info(sender='Data Logging', app_data='Log Entry')