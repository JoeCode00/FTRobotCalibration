import dearpygui.dearpygui as dpg
from GUIhelp import _help, _config, _add_config_options, _hsv_to_rgb, _create_static_textures, _create_dynamic_textures, _update_dynamic_textures, _log


def show():
    with dpg.collapsing_header(label="Layout & Scrolling"):
    
        with dpg.tree_node(label="Widgets Width"):
            
            dpg.add_text("Width=100")
            dpg.add_drag_float(label="float", width=100)
    
            dpg.add_text("Width=-100")
            dpg.add_drag_float(label="float", width=-100)
    
            dpg.add_text("Width=-1")
            dpg.add_drag_float(label="float", width=-1)
    
            dpg.add_text("group with width=75")
            with dpg.group(width=75):
                dpg.add_drag_float(label="float")
                dpg.add_drag_float(label="float")
                dpg.add_drag_float(label="float")
    
        with dpg.tree_node(label="Basic Horizontal Layout"):
    
            dpg.add_text("(Use groups with horizontal set to True to keep adding items to the right of the preceding item)", bullet=True)
            with dpg.group(horizontal=True):
                dpg.add_text("Normal buttons")
                dpg.add_button(label="Banana")
                dpg.add_button(label="Apple")
                dpg.add_button(label="Corniflower")
    
            with dpg.group(horizontal=True):
                dpg.add_text("Small buttons")
                dpg.add_button(label="Like this one", small=True)
                dpg.add_text("can fit within a text block")
    
            with dpg.group(horizontal=True, xoffset=150):
                dpg.add_text("Aligned")
                dpg.add_text("x=150")
                dpg.add_text("x=300")
    
            with dpg.group(horizontal=True, xoffset=150):
                dpg.add_text(default_value="Aligned")
                dpg.add_button(label="x=150", small=True)
                dpg.add_button(label="x=300", small=True)
    
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="My")
                dpg.add_checkbox(label="Tailor")
                dpg.add_checkbox(label="is")
                dpg.add_checkbox(label="rich")
    
            dpg.add_text("Lists:")
            with dpg.group(horizontal=True):
                dpg.add_listbox(("AAAA", "BBBB", "CCCC", "DDDD"), default_value="AAAA", width=100, label="")
                dpg.add_listbox(("AAAA", "BBBB", "CCCC", "DDDD"), default_value="BBBB", width=100, label="")
                dpg.add_listbox(("AAAA", "BBBB", "CCCC", "DDDD"), default_value="CCCC", width=100, label="")
                dpg.add_listbox(("AAAA", "BBBB", "CCCC", "DDDD"), default_value="DDDD", width=100, label="")
            
            dpg.add_text("Spacing(100):")
            with dpg.group(horizontal=True, horizontal_spacing=100):
                dpg.add_button(label="A", width=50, height=50)
                dpg.add_button(label="B", width=50, height=50)
    
        with dpg.tree_node(label="Ordered pack style"):
            dpg.add_button(label="Button 1")
            dpg.add_button(label="Button 2")
            dpg.add_button(label="Button 3")
    
        with dpg.tree_node(label="Absolute Position Placement"):
            dpg.add_button(label="Set Button 2 Pos", callback=lambda: dpg.set_item_pos(B2, (50, 125)))
            dpg.add_button(label="Reset Button 2 Pos", callback=lambda: dpg.reset_pos(B2))
            dpg.add_button(label="Button 1", pos=[50,50], width=75, height=75)
            B2 = dpg.add_button(label="Button 2", width=75, height=75)
            dpg.add_button(label="Button 3")
    
        with dpg.tree_node(label="Grid Layout using Table API"):
            layout_demo_table = dpg.generate_uuid()
            dpg.add_text("Tables can be used to layout items in an equally spaced grid pattern.")
            dpg.add_text("See tables section for more detail on tables.")
            dpg.add_checkbox(label="resizable", callback=_config, user_data=layout_demo_table)
            dpg.add_checkbox(label="borders_innerH", callback=_config, user_data=layout_demo_table, default_value=True)
            dpg.add_checkbox(label="borders_outerH", callback=_config, user_data=layout_demo_table, default_value=True)
            dpg.add_checkbox(label="borders_innerV", callback=_config, user_data=layout_demo_table, default_value=True)
            dpg.add_checkbox(label="borders_outerV", callback=_config, user_data=layout_demo_table, default_value=True)
            with dpg.table(tag=layout_demo_table, header_row=False, borders_innerH=True, 
                           borders_outerH=True, borders_innerV=True, borders_outerV=True):
                
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
    
                with dpg.table_row():
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                
                with dpg.table_row():
                    dpg.add_table_cell()
                    dpg.add_button(label="Button 4")
                    dpg.add_button(label="Button 5")
    
        with dpg.tree_node(label="Containers"):
    
            with dpg.tree_node(label="Tree Nodes"):
                with dpg.tree_node(label="Tree Node (selectable)", selectable=True):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.tree_node(label="Tree Node (bullet)", bullet=True):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
            
            with dpg.tree_node(label="Groups"):
                dpg.add_text("Groups are used to control child items placement, width, and provide a hit box for things like is the set of items are hovered, ect...")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.group(width=150):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.group():
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
            
            with dpg.tree_node(label="Child windows"):
                demo_layout_child = dpg.generate_uuid()
                dpg.add_text("Child windows are basically embedded windows and provide much more structure and control of the containing items than groups.")
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="autosize_x", callback=_config, user_data=demo_layout_child)
                    dpg.add_checkbox(label="autosize_y", callback=_config, user_data=demo_layout_child)
                    dpg.add_checkbox(label="menubar", callback=_config, user_data=demo_layout_child)
                    dpg.add_checkbox(label="no_scrollbar", callback=_config, user_data=demo_layout_child)
                    dpg.add_checkbox(label="horizontal_scrollbar", callback=_config, user_data=demo_layout_child)
                    dpg.add_checkbox(label="border", default_value=True, callback=_config, user_data=demo_layout_child)
                with dpg.child_window(tag=demo_layout_child, width=200, height=200):
                    with dpg.menu_bar():
                        with dpg.menu(label="Menu"):
                            pass
                    for i in range(20):
                        dpg.add_text(default_value="A pretty long sentence if you really think about it. It's also pointless. we need this to be even longer")
                with dpg.child_window(autosize_x=True, height=130, menubar=True):
                    with dpg.menu_bar():
                        dpg.add_menu(label="Menu Options")
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=100, height=150, horizontal_scrollbar=True):
                        dpg.add_button(label="Button 1")
                        dpg.add_button(label="Button 2")
                        dpg.add_button(label="Button 3")
                        dpg.add_button(label="Button 4", width=150)
                        dpg.add_button(label="Button 5")
                        dpg.add_button(label="Button 6")
                    with dpg.child_window(width=100, height=110):
                        dpg.add_button(label="Button 1")
                        dpg.add_button(label="Button 2")
                        dpg.add_button(label="Button 3")
            
            with dpg.tree_node(label="Collapsing Headers"):
                with dpg.collapsing_header(label="Collapsing Header"):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.collapsing_header(label="Collapsing Header (close)", closable=True):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.collapsing_header(label="Collapsing Header (bullet)", bullet=True):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.collapsing_header(label="Collapsing Header (leaf)", leaf=True):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
            
            with dpg.tree_node(label="Tabs"):
    
                with dpg.tree_node(label="Basic"):
    
                    with dpg.tab_bar():
                        
                        with dpg.tab(label="Avocado"):
                            dpg.add_text("This is the avocado tab!")
                        
                        with dpg.tab(label="Broccoli"):
                            dpg.add_text("This is the broccoli tab!")
    
                        with dpg.tab(label="Cucumber"):
                            dpg.add_text("This is the cucumber tab!")
    
                with dpg.tree_node(label="Advanced"):
    
                    with dpg.tab_bar() as tb:
    
                        with dpg.tab(label="tab 1"):
                            dpg.add_text("This is the tab 1!")
    
                        with dpg.tab(label="tab 2") as t2:
                            dpg.add_text("This is the tab 2!")
    
                        with dpg.tab(label="tab 3"):
                            dpg.add_text("This is the tab 3!")
    
                        with dpg.tab(label="tab 4"):
                            dpg.add_text("This is the tab 4!")
    
                        tbb = dpg.add_tab_button(label="+")
                        dpg.add_tab_button(label="?")
    
                        #dpg.add_checkbox(before=tb, label="tab bar reorderable", user_data=tb, callback=lambda s, a, u: dpg.configure_item(u, reorderable=dpg.get_value(s)))
                        #dpg.add_checkbox(before=tb, label="tab 2 no_reorder", user_data=t2, callback=lambda s, a, u: dpg.configure_item(u, no_reorder=dpg.get_value(s)))
                        #dpg.add_checkbox(before=tb, label="tab 2 leading", user_data=t2, callback=lambda s, a, u: dpg.configure_item(u, leading=dpg.get_value(s)))
                        #dpg.add_checkbox(before=tb, label="tab 2 trailing", user_data=t2, callback=lambda s, a, u: dpg.configure_item(u, trailing=dpg.get_value(s)))
                        #dpg.add_checkbox(before=tb, label="tab button trailing", user_data=tbb, callback=lambda s, a, u: dpg.configure_item(u, trailing=dpg.get_value(s)))
                        #dpg.add_checkbox(before=tb, label="tab button leading", user_data=tbb, callback=lambda s, a, u: dpg.configure_item(u, leading=dpg.get_value(s)))
    
        with dpg.tree_node(label="Simple Layouts"):
            dpg.add_text("Containers can be nested for advanced layout options")
            with dpg.child_window(width=500, height=320, menubar=True):
                with dpg.menu_bar():
                    dpg.add_menu(label="Menu Options")
                with dpg.child_window(autosize_x=True, height=95):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Header 1", width=75, height=75)
                        dpg.add_button(label="Header 2", width=75, height=75)
                        dpg.add_button(label="Header 3", width=75, height=75)
                with dpg.child_window(autosize_x=True, height=175):
                    with dpg.group(horizontal=True, width=0):
                        with dpg.child_window(width=102, height=150):
                            with dpg.tree_node(label="Nav 1"):
                                dpg.add_button(label="Button 1")
                            with dpg.tree_node(label="Nav 2"):
                                dpg.add_button(label="Button 2")
                            with dpg.tree_node(label="Nav 3"):
                                dpg.add_button(label="Button 3")
                        with dpg.child_window(width=300, height=150):
                            dpg.add_button(label="Button 1")
                            dpg.add_button(label="Button 2")
                            dpg.add_button(label="Button 3")
                        with dpg.child_window(width=50, height=150):
                            dpg.add_button(label="B1", width=25, height=25)
                            dpg.add_button(label="B2", width=25, height=25)
                            dpg.add_button(label="B3", width=25, height=25)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Footer 1", width=175)
                    dpg.add_text("Footer 2")
                    dpg.add_button(label="Footer 3", width=175)
    
        with dpg.tree_node(label="Scrolling"):
    
            def _update_xscroll_info(sender, app_data, user_data):
                
                with dpg.mutex():
                    x_scroll = dpg.get_x_scroll(user_data[1])
                    max_scroll = dpg.get_x_scroll_max(user_data[1])
                    dpg.set_value(user_data[0], str(x_scroll) + "/" + str(max_scroll))
    
            def _update_yscroll_info(sender, app_data, user_data):
                
                with dpg.mutex():
                    y_scroll = dpg.get_y_scroll(user_data[1])
                    max_scroll = dpg.get_y_scroll_max(user_data[1])
                    dpg.set_value(user_data[0], str(y_scroll) + "/" + str(max_scroll))
    
            with dpg.table(header_row=False):
    
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
    
                children = []
                text_items = ("Top", "25%", "Center", "75%", "Bottom")
                track_items = (0.0, 0.25, 0.5, 0.75, 1.0)
    
                with dpg.table_row():
                    for i in range(5):
                        with dpg.table_cell():
                            dpg.add_text(text_items[i])
                            with dpg.child_window(height=200, delay_search=True) as _child_id:
                                for j in range(25):
                                    if j == 13:
                                        dpg.add_text("Item " + str(j), color=(255, 255, 0), tracked=True, track_offset=track_items[i])
                                    else:
                                        dpg.add_text("Item " + str(j))
                    
                            _text_id = dpg.add_text("0/0")
                            with dpg.item_handler_registry(tag="__demo_item_reg1_"+str(i)):
                                dpg.add_item_visible_handler(user_data=[_text_id, _child_id], callback=_update_yscroll_info)
                            dpg.bind_item_handler_registry(_text_id, dpg.last_container())
    
            for i in range(5):
                dpg.add_text(text_items[i])
                with dpg.group(horizontal=True):
                    with dpg.child_window(height=50, horizontal_scrollbar=True, width=-200, delay_search=True) as _child_id:
                        with dpg.group(horizontal=True):
                            for j in range(25):
                                if j == 13:
                                    dpg.add_text("Item " + str(j), color=(255, 255, 0), tracked=True, track_offset=track_items[i])
                                else:
                                    dpg.add_text("Item " + str(j))
                    _text_id = dpg.add_text("0/0")
                    with dpg.item_handler_registry(tag="__demo_item_reg2_"+str(i)):
                        dpg.add_item_visible_handler(user_data=[_text_id, _child_id], callback=_update_xscroll_info)
                    dpg.bind_item_handler_registry(_text_id, dpg.last_container())
    
            with dpg.child_window(height=50, horizontal_scrollbar=True, width=-200) as _child_id:
                with dpg.group(horizontal=True):
                    for j in range(25):
                        dpg.add_text("Item " + str(j))
    
            def _scroll_programmatically(sender, app_data, user_data):
    
                with dpg.mutex():
                    x_scroll = dpg.get_x_scroll(user_data[1])
                    max_scroll = dpg.get_x_scroll_max(user_data[1])
                    if user_data[0] == "left" and x_scroll > 10:
                        dpg.set_x_scroll(user_data[1], x_scroll-10)
                    elif user_data[0] == "left":
                        dpg.set_x_scroll(user_data[1], 0)
    
                    if user_data[0] == "right" and x_scroll < max_scroll-10:
                        dpg.set_x_scroll(user_data[1], x_scroll+10)
                    elif user_data[0] == "right":
                        dpg.set_x_scroll(user_data[1], max_scroll)
    
            with dpg.group(horizontal=True):
                dpg.add_button(label="<<", small=True, user_data=["left", _child_id], callback=_scroll_programmatically)
                dpg.add_text("Scroll from code")
                dpg.add_button(label=">>", small=True, user_data=["right", _child_id], callback=_scroll_programmatically)
                _text_id = dpg.add_text("0/0")
            with dpg.item_handler_registry(tag="__demo_item_reg3"):
                dpg.add_item_visible_handler(user_data=[_text_id, _child_id], callback=_update_xscroll_info)
            dpg.bind_item_handler_registry(_text_id, dpg.last_container())
