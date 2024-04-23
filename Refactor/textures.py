import dearpygui.dearpygui as dpg
from GUIhelp import _help, _config, _add_config_options, _hsv_to_rgb, _create_static_textures, _create_dynamic_textures, _update_dynamic_textures, _log

def show():
    with dpg.collapsing_header(label="Textures & Images"):
    
        with dpg.tree_node(label="Help"):

            dpg.add_separator()
            dpg.add_text("ABOUT TEXTURES:")
            dpg.add_text("Textures are buffers of RGBA data.", bullet=True, indent=20)
            dpg.add_text("Textures are used by 'image based' widgets:", bullet=True, indent=20)
            dpg.add_text("add_image", bullet=True, indent=50)
            dpg.add_text("add_image_button", bullet=True, indent=50)
            dpg.add_text("draw_image", bullet=True, indent=50)
            dpg.add_text("add_image_series", bullet=True, indent=50)
            dpg.add_text("Textures are themselves widgets.", bullet=True, indent=20)
            dpg.add_text("Textures must be a child of a texture container widget.", bullet=True, indent=20)
            dpg.add_text("Textures can be either static or dynamic (see following sections).", bullet=True, indent=20)

            dpg.add_separator()
            dpg.add_text("PROGRAMMER GUIDE:")
            dpg.add_text("'image based' widgets hold a reference to a texture widget.", bullet=True, indent=20)
            dpg.add_text("Deleting the texture widget will not affect widget's using it.", bullet=True, indent=50)
            dpg.add_text("Textures are only free'd from the GPU when the reference count reaches 0.", bullet=True, indent=50)
            dpg.add_text("The texture container widget is a root (has no parent).", bullet=True, indent=20)
            dpg.add_text("The texture container widget is hidden by default.", bullet=True, indent=20)
            with dpg.group(horizontal=True):
                dpg.add_text("'Showing' it, opens a manager to inspect the textures within.", bullet=True, indent=50)
                dpg.add_button(label="Press Here", small=True, callback=lambda:dpg.configure_item("__demo_texture_container", show=True))
            dpg.add_separator()

        with dpg.tree_node(label="Static Textures"):

            dpg.add_separator()
            dpg.add_text("ABOUT STATIC TEXTURES:")
            dpg.add_text("Can NOT be modified after creation.", bullet=True, indent=20)
            dpg.add_text("Can be loaded from a file using the 'file' keyword.", bullet=True, indent=20)
            dpg.add_separator()

            with dpg.group(horizontal=True):

                with dpg.group():
                    dpg.add_text("Image Button")
                    dpg.add_image_button("__demo_static_texture_1")

                with dpg.group():
                    dpg.add_text("Image")
                    dpg.add_image("__demo_static_texture_2")

                with dpg.group():
                    dpg.add_text("Image (texture size)")
                    dpg.add_image("__demo_static_texture_3")

                with dpg.group():
                    dpg.add_text("Image (2x texture size)")
                    dpg.add_image("__demo_static_texture_3", width=200, height=200)

            dpg.add_image(dpg.mvFontAtlas)

        with dpg.tree_node(label="Dynamic Textures"):

            dpg.add_separator()
            dpg.add_text("ABOUT DYNAMIC TEXTURES:")
            dpg.add_text("Can be modified after creation with 'set_value'.", bullet=True, indent=20)
            dpg.add_text("New data must be the same dimensions as the original", bullet=True, indent=20)
            dpg.add_separator()

            with dpg.group(horizontal=True):

                with dpg.group():
                    dpg.add_color_picker((255, 0, 255, 255), label="Texture 1", 
                            no_side_preview=True, alpha_bar=True, width=200,
                            callback=_update_dynamic_textures, user_data=1)
                    dpg.add_text("Image Button")
                    dpg.add_image_button("__demo_dynamic_texture_1", width=100, height=100)


                with dpg.group():
                    dpg.add_color_picker((255, 255, 0, 255), label="Texture 2", 
                                         no_side_preview=True, alpha_bar=True, width=200,
                                         callback=_update_dynamic_textures, user_data=2)
                    dpg.add_text("Image")
                    dpg.add_image("__demo_dynamic_texture_2")

        with dpg.tree_node(label="Image Series (plots)"):

            with dpg.plot(label="Image Plot", height=400, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x axis")
                with dpg.plot_axis(dpg.mvYAxis, label="y axis"):
                    dpg.add_image_series(dpg.mvFontAtlas, [300, 300], [400, 400], label="font atlas")
                    dpg.add_image_series("__demo_static_texture_1", [0, 0], [100, 100], label="static 1")
                    dpg.add_image_series("__demo_static_texture_2", [150, 150], [200, 200], label="static 2")
                    dpg.add_image_series("__demo_static_texture_3", [200, -150], [300, -50], label="static 3")
                    dpg.add_image_series("__demo_dynamic_texture_1", [-200, 100], [-100, 200], label="dynamic 1")
                    dpg.add_image_series("__demo_dynamic_texture_2", [-200, -100], [-150, -50], label="dynamic 2")

        with dpg.tree_node(label="Drawlists"):

            with dpg.drawlist(width=400, height=300):
                dpg.draw_rectangle((0, 0), (400, 300), color=(100, 100, 100, 250), thickness=2)
                dpg.draw_image("__demo_static_texture_3", [0, 0], [100, 100])
                dpg.draw_image("__demo_dynamic_texture_1", [200, 100], [300, 200])
