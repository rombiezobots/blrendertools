########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Globals
########################################################################################################################


########################################################################################################################
# Operators
########################################################################################################################


class BLRENDERTOOLS_OT_delete_view_layer(bpy.types.Operator):
    '''Delete the selected View Layer'''

    bl_idname = 'blrendertools.delete_view_layer'
    bl_label = 'Delete View Layer'
    bl_options = {'BLOCKING'}

    layer_name: bpy.props.StringProperty()

    def execute(self, context):
        if len(context.scene.view_layers) > 1:
            context.scene.view_layers.remove(context.scene.view_layers[self.layer_name])
        return {'FINISHED'}


class BLRENDERTOOLS_OT_manage_layer_collections(bpy.types.Operator):
    '''Manage View Layer Collections'''

    bl_idname = 'blrendertools.manage_layer_collections'
    bl_label = 'Layer Collection Manager'
    bl_options = {'BLOCKING'}

    layer_name: bpy.props.StringProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        lay = self.layout

    def execute(self, context):
        return {'FINISHED'}


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLRENDERTOOLS_OT_delete_view_layer,
        BLRENDERTOOLS_OT_manage_layer_collections,
    ]
)
