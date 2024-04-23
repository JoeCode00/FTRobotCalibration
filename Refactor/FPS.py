import dearpygui.dearpygui as dpg
from datetime import datetime
def FPS_counter(Frames, PreviousSecond):
    CurrentSecond = datetime.now().second
    if PreviousSecond != CurrentSecond:
        # print(str(Frames) + " FPS")
        dpg.set_value('FPS Text', 'FPS: '+str(Frames))
        PreviousSecond = CurrentSecond
        Frames = 0
    else:
        Frames = Frames + 1
    return Frames, CurrentSecond