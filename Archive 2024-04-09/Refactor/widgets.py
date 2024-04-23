import dearpygui.dearpygui as dpg
import math
from math import sin, cos
import random
import webbrowser

from GUIhelp import _help, _config, _add_config_options, _hsv_to_rgb, _create_static_textures, _create_dynamic_textures, _update_dynamic_textures, _log
def BP():
    breakpoint()

def show():
   with dpg.collapsing_header(label="Widgets"):
   
       with dpg.tree_node(label="Basic"):

           with dpg.group(horizontal=True):
               dpg.add_button(label="Breakpoint", tag='BP', callback=BP)
               dpg.add_button(label="Button", callback=_log)
               dpg.add_button(label="Button", callback=_log, small=True)
               dpg.add_button(label="Button", callback=_log, arrow=True) # default direction is mvDir_Up
               dpg.add_button(label="Button", callback=_log, arrow=True, direction=dpg.mvDir_Left)
               dpg.add_button(label="Button", callback=_log, arrow=True, direction=dpg.mvDir_Right)
               dpg.add_button(label="Button", callback=_log, arrow=True, direction=dpg.mvDir_Down)

           dpg.add_checkbox(label="checkbox", callback=_log)
           dpg.add_radio_button(("radio a", "radio b", "radio c"), callback=_log, horizontal=True)
           dpg.add_selectable(label="selectable", callback=_log)

           with dpg.group(horizontal=True):

               for i in range(7):

                   with dpg.theme(tag="__demo_theme"+str(i)):
                       with dpg.theme_component(dpg.mvButton):
                           dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(i/7.0, 0.6, 0.6))
                           dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(i/7.0, 0.8, 0.8))
                           dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(i/7.0, 0.7, 0.7))
                           dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, i*5)
                           dpg.add_theme_style(dpg.mvStyleVar_FramePadding, i*3, i*3)

                   dpg.add_button(label="Click", callback=_log)
                   dpg.bind_item_theme(dpg.last_item(), "__demo_theme"+str(i))

           with dpg.group(horizontal=True):

               dpg.add_text("Press a button: ")
               widget = dpg.add_text("0")
               dpg.add_button(arrow=True, direction=dpg.mvDir_Left, user_data=widget, callback=lambda s, a, u: dpg.set_value(u, int(dpg.get_value(u))-1))
               dpg.add_button(arrow=True, direction=dpg.mvDir_Right, user_data=widget, callback=lambda s, a, u: dpg.set_value(u, int(dpg.get_value(u))+1))

           dpg.add_text("hover me")
           with dpg.tooltip(dpg.last_item()):
               dpg.add_text("I'm a simple tooltip!")

           dpg.add_separator()

           dpg.add_text("Value", label="Label", show_label=True)
           dpg.add_combo(("AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK"), label="combo", default_value="AAAA", callback=_log)
           dpg.add_input_text(label="input text", default_value="Hello, world!", callback=_log)
           _help(
                   "USER:\n"
                   "Hold SHIFT or use mouse to select text.\n"
                   "CTRL+Left/Right to word jump.\n"
                   "CTRL+A or double-click to select all.\n"
                   "CTRL+X,CTRL+C,CTRL+V clipboard.\n"
                   "CTRL+Z,CTRL+Y undo/redo.\n"
                   "ESCAPE to revert.\n\n")
           dpg.add_input_text(label="input text (w/ hint)", hint="enter text here", callback=_log)
           dpg.add_input_int(label="input int", callback=_log)
           dpg.add_input_float(label="input float", callback=_log, format="%.06f")
           dpg.add_input_float(label="input float scientific", format="%e", callback=_log)
           dpg.add_input_floatx(label="input floatx", callback=_log, default_value=[1,2,3,4])
           dpg.add_input_double(label="input double", callback=_log, format="%.14f")
           dpg.add_input_doublex(label="input doublex", callback=_log, default_value=[1,2,3,4], format="%.14f")
           dpg.add_drag_int(label="drag int", callback=_log)
           _help(
                   "Click and drag to edit value.\n"
                   "Hold SHIFT/ALT for faster/slower edit.\n"
                   "Double-click or CTRL+click to input value.")
           dpg.add_drag_int(label="drag int 0..100", format="%d%%", callback=_log)
           dpg.add_drag_float(label="drag float", callback=_log)
           dpg.add_drag_float(label="drag small float", default_value=0.0067, format="%.06f ns", callback=_log)
           dpg.add_slider_int(label="slider int", max_value=3, callback=_log)
           _help("CTRL+click to enter value.")
           dpg.add_slider_float(label="slider float", max_value=1.0, format="ratio = %.3f", callback=_log)
           dpg.add_slider_double(label="slider double", max_value=1.0, format="ratio = %.14f", callback=_log)
           dpg.add_slider_int(label="slider angle", min_value=-360, max_value=360, format="%d deg", callback=_log)
           _help(
                   "Click on the colored square to open a color picker.\n"
                   "Click and hold to use drag and drop.\n"
                   "Right-click on the colored square to show options.\n"
                   "CTRL+click on individual component to input value.\n")
           dpg.add_color_edit((102, 179, 0, 128), label="color edit 4", callback=_log)
           dpg.add_color_edit(default_value=(.5, 1, .25, .1), label="color edit 4", callback=_log)
           dpg.add_listbox(("Apple", "Banana", "Cherry", "Kiwi", "Mango", "Orange", "Pineapple", "Strawberry", "Watermelon"), label="listbox", num_items=4, callback=_log)
           dpg.add_color_button()

       with dpg.tree_node(label="Combo"):

           items = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
           combo_id = dpg.add_combo(items, label="combo", height_mode=dpg.mvComboHeight_Small)
           _add_config_options(combo_id, 1, "popup_align_left", "no_arrow_button", "no_preview")

       with dpg.tree_node(label="Color Picker & Edit"):

           _color_picker_id = dpg.generate_uuid()
           _color_edit_id = dpg.generate_uuid()

           def _color_picker_configs(sender, value, user_data):

               _old_config = dpg.get_item_configuration(user_data)

               if user_data ==_color_picker_id:
                   picker_mode = _old_config["picker_mode"]
               else:
                   display_mode = _old_config["display_mode"]
               alpha_preview = _old_config["alpha_preview"]
               display_type = _old_config["display_type"]
               input_mode = _old_config["input_mode"]

               # picker_mode
               if value == "mvColorPicker_bar":
                   picker_mode=dpg.mvColorPicker_bar
               elif value == "mvColorPicker_wheel":
                   picker_mode = dpg.mvColorPicker_wheel

               # alpha_preview
               elif value == "mvColorEdit_AlphaPreviewNone":
                   alpha_preview=dpg.mvColorEdit_AlphaPreviewNone
               elif value == "mvColorEdit_AlphaPreview":
                   alpha_preview = dpg.mvColorEdit_AlphaPreview
               elif value == "mvColorEdit_AlphaPreviewHalf":
                   alpha_preview = dpg.mvColorEdit_AlphaPreviewHalf

               # display_type
               elif value == "mvColorEdit_uint8":
                   display_type=dpg.mvColorEdit_uint8
               elif value == "mvColorEdit_float":
                   display_type = dpg.mvColorEdit_float

               # display_type
               elif value == "mvColorEdit_uint8":
                   display_type=dpg.mvColorEdit_uint8
               elif value == "mvColorEdit_float":
                   display_type = dpg.mvColorEdit_float

               # display_mode
               elif value == "mvColorEdit_rgb":
                   display_mode=dpg.mvColorEdit_rgb
               elif value == "mvColorEdit_hsv":
                   display_mode = dpg.mvColorEdit_hsv
               elif value == "mvColorEdit_hex":
                   display_mode = dpg.mvColorEdit_hex

               if user_data ==_color_picker_id:
                   dpg.configure_item(user_data, 
                                      picker_mode=picker_mode, 
                                      alpha_preview=alpha_preview,
                                      display_type=display_type,
                                      input_mode=input_mode
                                      )
               else:
                   dpg.configure_item(user_data, 
                                      alpha_preview=alpha_preview,
                                      display_type=display_type,
                                      input_mode=input_mode,
                                      display_mode=display_mode
                                      )

           dpg.add_text("Color Picker")

           with dpg.group(horizontal=True):
               _before_id = dpg.add_text("picker_mode:")
               dpg.add_radio_button(("mvColorPicker_bar", "mvColorPicker_wheel"), callback=_color_picker_configs, 
                                    user_data=_color_picker_id, horizontal=True)
           
           with dpg.group(horizontal=True):
               dpg.add_text("alpha_preview:")
               dpg.add_radio_button(("mvColorEdit_AlphaPreviewNone", "mvColorEdit_AlphaPreview", "mvColorEdit_AlphaPreviewHalf"), callback=_color_picker_configs, 
                                user_data=_color_picker_id, horizontal=True)

           with dpg.group(horizontal=True):
               dpg.add_text("display_type:")
               dpg.add_radio_button(("mvColorEdit_uint8", "mvColorEdit_float"), callback=_color_picker_configs, 
                                    user_data=_color_picker_id, horizontal=True)

           with dpg.group(horizontal=True):
               dpg.add_text("input_mode:")
               dpg.add_radio_button(("mvColorEdit_input_rgb", "mvColorEdit_input_hsv"), callback=_color_picker_configs, 
                                    user_data=_color_picker_id, horizontal=True)

           dpg.add_color_picker((255, 0, 255, 255), label="Color Picker", 
                   width=200, tag=_color_picker_id)

           _add_config_options(_color_picker_id, 3, 
                               "no_alpha", "no_side_preview", "display_rgb",
                               "display_hsv", "display_hex",
                               "no_small_preview", "no_inputs", "no_tooltip",
                               "no_label", "alpha_bar", before=_before_id)

           dpg.add_separator()

           dpg.add_text("Color Edit")

           with dpg.group(horizontal=True):
               _before_id = dpg.add_text("alpha_preview:")
               dpg.add_radio_button(("mvColorEdit_AlphaPreviewNone", "mvColorEdit_AlphaPreview", "mvColorEdit_AlphaPreviewHalf"), callback=_color_picker_configs, 
                                    user_data=_color_edit_id, horizontal=True)

           with dpg.group(horizontal=True):
               dpg.add_text("display_type:")
               dpg.add_radio_button(("mvColorEdit_uint8", "mvColorEdit_float"), callback=_color_picker_configs, 
                                    user_data=_color_edit_id, horizontal=True)

           with dpg.group(horizontal=True):
               dpg.add_text("display_mode:")
               dpg.add_radio_button(("mvColorEdit_rgb", "mvColorEdit_hsv", "mvColorEdit_hex"), callback=_color_picker_configs, 
                                    user_data=_color_edit_id, horizontal=True)

           with dpg.group(horizontal=True):
               dpg.add_text("input_mode:")
               dpg.add_radio_button(("mvColorEdit_input_rgb", "mvColorEdit_input_hsv"), callback=_color_picker_configs, 
                                    user_data=_color_edit_id, horizontal=True)

           dpg.add_color_edit((255, 0, 255, 255), label="Color Edit", 
                   width=200, tag=_color_edit_id)

           _add_config_options(_color_edit_id, 3, 
                               "no_alpha", "no_picker",
                               "no_options", "no_inputs", "no_small_preview",
                               "no_tooltip", "no_label", 
                               "no_drag_drop", "alpha_bar", before=_before_id)

       with dpg.tree_node(label="Colormaps"):
           dpg.add_text("Notes")
           dpg.add_text("Colormaps belong to a mvColorMapRegistry.", bullet=True, indent=20)
           with dpg.group(horizontal=True):
               dpg.add_text("Showing the registry will help with debugging. Press ", bullet=True, indent=20)
               dpg.add_button(label="here", small=True, callback=lambda:dpg.show_item("__demo_colormap_registry"))
           dpg.add_text("Colormaps are applied with 'bind_colormap(item_id, colormap_id)", bullet=True, indent=20)
           dpg.add_text("Colormaps can be applied to mvPlot, mvColorMapButton, mvColorMapSlider, mvColorMapScale", bullet=True, indent=20)
           dpg.add_text("Colormaps can be sampled with 'sample_colormap(colormap_id, t)' (0<t<1)", bullet=True, indent=20)
           dpg.add_text("Colormaps can be sampled by index with 'get_colormap_color(colormap_id, index)'", bullet=True, indent=20)
           dpg.add_colormap([[0, 0, 0, 255], [255, 255, 255, 255]], False, tag="__demo_colormap_1", parent="__demo_colormap_registry", label="Demo 1")
           dpg.add_colormap([[255, 0, 0], [0, 255, 0], [0, 0, 255]], True, tag="__demo_colormap_2", parent="__demo_colormap_registry", label="Demo 2")
           dpg.add_colormap_button(label="Colormap Button 1")
           dpg.bind_colormap(dpg.last_item(), "__demo_colormap_1")
           dpg.add_colormap_button(label="Colormap Button 2")
           dpg.bind_colormap(dpg.last_item(), "__demo_colormap_2")
           dpg.add_colormap_slider(label="Colormap Slider 1", default_value=0.5)
           dpg.bind_colormap(dpg.last_item(), "__demo_colormap_1")
           dpg.add_colormap_slider(label="Colormap Slider 2")
           dpg.bind_colormap(dpg.last_item(), "__demo_colormap_2")
           with dpg.group(horizontal=True):
               dpg.add_colormap_scale(label="Colormap Slider 1")
               dpg.bind_colormap(dpg.last_item(), "__demo_colormap_1")
               dpg.add_colormap_scale(label="Colormap Slider 2")
               dpg.bind_colormap(dpg.last_item(), "__demo_colormap_2")
               dpg.add_colormap_scale(label="Colormap Spectral", min_scale=-100, max_scale=150)
               dpg.bind_colormap(dpg.last_item(), dpg.mvPlotColormap_Spectral)

       with dpg.tree_node(label="List Boxes"):
           items = ("A","B","C","D","E","F","G","H","I","J","K","L","M" "O","P","Q","R","S","T","U","V","W","X","Y","Z")
           listbox_1 = dpg.add_listbox(items, label="listbox 1 (full)")
           listbox_2 = dpg.add_listbox(items, label="listbox 2", width=200)
           dpg.add_input_int(label="num_items",callback=_config, user_data=[listbox_1, listbox_2], before = listbox_1)
           dpg.add_slider_int(label="width", default_value=200, callback=_config, user_data=listbox_2, before = listbox_1, max_value=500)
   
       with dpg.tree_node(label="Selectables"):
           
           with dpg.tree_node(label="Basic"):
               dpg.add_selectable(label="1. I am selectable")
               dpg.add_text("2. I am not selectable")

           with dpg.tree_node(label="Selection State: Single"):

               def _selection(sender, app_data, user_data):
                   for item in user_data:
                       if item != sender:
                          dpg.set_value(item, False)
               items = (
                   dpg.add_selectable(label="1. I am selectable"),
                   dpg.add_selectable(label="2. I am selectable"),
                   dpg.add_selectable(label="3. I am selectable"),
                   dpg.add_selectable(label="4. I am selectable"),
                   dpg.add_selectable(label="5. I am selectable"),
                   )

               for item in items:
                   dpg.configure_item(item, callback=_selection, user_data=items)

       with dpg.tree_node(label="Bullets"):

           dpg.add_text("Bullet point 1", bullet=True)
           dpg.add_text("Bullet point 2\nbullet text can be\nOn multiple lines", bullet=True)
           with dpg.tree_node(label="Tree node"):
               dpg.add_text("Another bullet point", bullet=True)
           
           with dpg.group(horizontal=True):
               dpg.add_text("1", bullet=True)
               dpg.add_button(label="Button", small=True)

       with dpg.tree_node(label="Text"):

           with dpg.tree_node(label="Colored Text"):
           
               dpg.add_text("Pink", color=(255, 0, 255))
               dpg.add_text("Yellow", color=(255, 255, 0))

           with dpg.tree_node(label="Word Wrapping"):

               paragraph1 = 'This text should automatically wrap on the edge of the window.The current implementation for the text wrapping follows simple rules suited for English and possibly other languages'
               paragraph2 = 'The lazy dong is a good dog. This paragraph should fit within the child. Testing a 1 character word. The quick brown fox jumps over the lazy dog.'

               dpg.add_text(paragraph1, wrap=0)
               widget_id = dpg.add_slider_int(label="wrap width", default_value=500, max_value=1000, 
                                  callback=lambda s, a, u: dpg.configure_item(u, wrap=a))
               dpg.add_text(paragraph2, wrap=500)
               dpg.configure_item(widget_id, user_data=dpg.last_item())

       with dpg.tree_node(label="Text Input"):

           with dpg.tree_node(label="Multi-line Text Input"):

               paragraph = """/*\n
                   The Pentium F00F bug, shorthand for F0 0F C7 C8,\n
                   the hexadecimal encoding of one offending instruction,\n
                   more formally, the invalid operand with locked CMPXCHG8B\n
                   instruction bug, is a design flaw in the majority of\n
                   Intel Pentium, Pentium MMX, and Pentium OverDrive\n
                   processors (all in the P5 microarchitecture).\n
                   */\n\n
                   label:\n
                   \tlock cmpxchg8b eax\n"""

               dpg.add_input_text(label="input text", multiline=True, default_value=paragraph, height=300, callback=_log, tab_input=True)

               _add_config_options(dpg.last_item(), 1, 
                       "readonly", "on_enter")

           with dpg.tree_node(label="Filtered Text Input"):

               dpg.add_input_text(callback=_log, label="default")
               dpg.add_input_text(callback=_log, label="decimal", decimal=True)
               dpg.add_input_text(callback=_log, label="no blank", no_spaces=True)
               dpg.add_input_text(callback=_log, label="uppercase", uppercase=True)
               dpg.add_input_text(callback=_log, label="scientific", scientific=True)
               dpg.add_input_text(callback=_log, label="hexdecimal", hexadecimal=True)
       
           with dpg.tree_node(label="Password Input"):

               password = dpg.add_input_text(label="password", password=True, callback=_log)
               dpg.add_input_text(label="password (w/ hint)", password=True, hint="<password>", source=password, callback=_log)
               dpg.add_input_text(label="password (clear)", source=password, callback=_log)

       with dpg.tree_node(label="Simple Plots"):

           data = (0.6, 0.1, 1.0, 0.5, 0.92, 0.1, 0.2)
           dpg.add_simple_plot(label="Frame Times", default_value=data)
           dpg.add_simple_plot(label="Histogram", default_value=data, height=80, histogram=True, min_scale=0.0)

           data1 = []
           for i in range(70):
               data1.append(cos(3.14*6*i/180))

           dpg.add_simple_plot(label="Lines", default_value=data1, height=80)
           dpg.add_simple_plot(label="Histogram", default_value=data1, height=80, histogram=True)
           with dpg.group(horizontal=True):
               dpg.add_progress_bar(label="Progress Bar", default_value=0.78, overlay="78%")
               dpg.add_text("Progress Bar")
           with dpg.theme(tag="__demo_theme_progressbar"):
               with dpg.theme_component(dpg.mvProgressBar):
                   dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (255,0,0, 255))
           dpg.add_progress_bar(default_value=0.78, overlay="1367/1753")
           dpg.bind_item_theme(dpg.last_item(), "__demo_theme_progressbar")

       with dpg.tree_node(label="Multi-component Widgets"):

           for i in range(2, 5):

               with dpg.group():
                   float_source = dpg.add_input_floatx(label=f"input float {i}", min_value=0.0, max_value=100.0, size=i)
                   dpg.add_drag_floatx(label=f"drag float {i}", source=float_source, size=i)
                   dpg.add_slider_floatx(label=f"slider float {i}", source=float_source, size=i)

               with dpg.group():
                   double_source = dpg.add_input_doublex(label=f"input double {i}", min_value=0.0, max_value=100.0, size=i)
                   dpg.add_drag_doublex(label=f"drag double {i}", source=double_source, size=i)
                   dpg.add_slider_doublex(label=f"slider double {i}", source=double_source, size=i)

               with dpg.group():

                   int_source = dpg.add_input_intx(label=f"input int {i}", min_value=0, max_value=100, size=i)
                   dpg.add_drag_intx(label=f"drag int {i}", source=int_source, size=i)
                   dpg.add_slider_intx(label=f"slider int {i}", source=int_source, size=i)
       
               dpg.add_spacer(height=10)

       with dpg.tree_node(label="Vertical Sliders"):

           with dpg.group(horizontal=True):
               dpg.add_slider_int(label=" ", default_value=1, vertical=True, max_value=5, height=160)
               dpg.add_slider_double(label=" ", default_value=1.0, vertical=True, max_value=5.0, height=160)

               with dpg.group(horizontal=True):

                   with dpg.group(horizontal=True):

                       values = [ 0.0, 0.60, 0.35, 0.9, 0.70, 0.20, 0.0 ]

                       for i in range(7):

                           with dpg.theme(tag="__demo_theme2_"+str(i)):
                               with dpg.theme_component(0):
                                   dpg.add_theme_color(dpg.mvThemeCol_FrameBg, _hsv_to_rgb(i/7.0, 0.5, 0.5))
                                   dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, _hsv_to_rgb(i/7.0, 0.9, 0.9))
                                   dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, _hsv_to_rgb(i/7.0, 0.7, 0.5))
                                   dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, _hsv_to_rgb(i/7.0, 0.6, 0.5))

                           dpg.add_slider_float(label=" ", default_value=values[i], vertical=True, max_value=1.0, height=160)
                           dpg.bind_item_theme(dpg.last_item(), "__demo_theme2_"+str(i))

                   with dpg.group():
                       for i in range(3):
                           with dpg.group(horizontal=True):
                               values = [ 0.20, 0.80, 0.40, 0.25 ]
                               for j in range(4):
                                   dpg.add_slider_float(label=" ", default_value=values[j], vertical=True, max_value=1.0, height=50)

                   with dpg.group(horizontal=True):
                       dpg.add_slider_float(label=" ", vertical=True, max_value=1.0, height=160, width=40)
                       dpg.add_slider_float(label=" ", vertical=True, max_value=1.0, height=160, width=40)
                       dpg.add_slider_float(label=" ", vertical=True, max_value=1.0, height=160, width=40)
                       dpg.add_slider_float(label=" ", vertical=True, max_value=1.0, height=160, width=40)

       with dpg.tree_node(label="Time/Date Widgets"):

           dpg.add_time_picker(default_value={'hour': 14, 'min': 32, 'sec': 23})
           dpg.add_separator()
       
           with dpg.table(header_row=False):

               dpg.add_table_column()
               dpg.add_table_column()
               dpg.add_table_column()

               with dpg.table_row():
                   dpg.add_date_picker(level=dpg.mvDatePickerLevel_Day, default_value={'month_day': 8, 'year':93, 'month':5})
                   dpg.add_date_picker(level=dpg.mvDatePickerLevel_Month, default_value={'month_day': 8, 'year':93, 'month':5})
                   dpg.add_date_picker(level=dpg.mvDatePickerLevel_Year, default_value={'month_day': 8, 'year':93, 'month':5})

       with dpg.tree_node(label="Loading Indicators"):

           with dpg.group(horizontal=True):
               dpg.add_loading_indicator()
               dpg.add_loading_indicator(style=1)

       with dpg.tree_node(label="Knobs"):

           with dpg.group(horizontal=True):

               dpg.add_knob_float(label="K1")
               dpg.add_knob_float(label="K2", default_value=25.0)
               dpg.add_knob_float(label="K3", default_value=50.0)

       with dpg.tree_node(label="2D/3D Sliders"):

           dpg.add_3d_slider(label="3D Slider", scale=0.5)
