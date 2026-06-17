########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def draw_menu_view3d(self, context):
    '''Draw the viewport's context menu'''
    lay = self.layout
    lay.separator()
    lay.menu('VIEW3D_MT_blrendertools')


def draw_menu_node_editor(self, context):
    '''Draw the node editor's context menu'''
    lay = self.layout
    lay.separator()
    lay.menu('NODE_MT_blrendertools')


########################################################################################################################
# Classes
########################################################################################################################


class VIEW3D_MT_blrendertools(bpy.types.Menu):
    bl_label = 'blrendertools'
    bl_idname = 'VIEW3D_MT_blrendertools'

    def draw(self, context):
        lay = self.layout
        lay.operator('blrendertools.manage_subdivision', icon='MOD_SUBSURF', text='Manage Subdivision...')
        lay.operator('blrendertools.create_material', text='Create New Material...')


class NODE_MT_blrendertools(bpy.types.Menu):
    bl_label = 'blrendertools'
    bl_idname = 'NODE_MT_blrendertools'

    def draw(self, context):
        lay = self.layout
        lay.operator('blrendertools.manage_image_sequences', text='Manage Image Sequences...')


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    VIEW3D_MT_blrendertools,
    NODE_MT_blrendertools,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_menu_view3d)
    bpy.types.NODE_MT_context_menu.append(draw_menu_node_editor)


def unregister():
    bpy.types.NODE_MT_context_menu.remove(draw_menu_node_editor)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu_view3d)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
