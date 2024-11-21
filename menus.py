########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def draw_main_menu(self, context):
    lay = self.layout
    lay.menu(TOPBAR_MT_blrendertools.bl_idname)


########################################################################################################################
# Classes
########################################################################################################################


class TOPBAR_MT_blrendertools(bpy.types.Menu):
    bl_label = 'blrendertools'
    bl_idname = 'TOPBAR_MT_blrendertools'

    def draw(self, context):
        lay = self.layout
        lay.label(text='Materials')
        lay.operator('blrendertools.create_material')
        lay.label(text='Images')
        lay.operator('blrendertools.manage_image_sequences')


########################################################################################################################
# Registration
########################################################################################################################


def register():
    bpy.utils.register_class(TOPBAR_MT_blrendertools)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_main_menu)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_main_menu)
    bpy.utils.unregister_class(TOPBAR_MT_blrendertools)
