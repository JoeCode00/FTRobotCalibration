import dearpygui.dearpygui as dpg
def input_state_error_values():
    try:
        StateValueS = int(dpg.get_value('Input State Value'))
    except Exception as e:
        print(e)
        StateValueS = None
    try:
        ErrorValueS = int(dpg.get_value('Input Error Value'))
    except Exception as e:
        print(e)
        ErrorValueS = None
    return StateValueS, ErrorValueS