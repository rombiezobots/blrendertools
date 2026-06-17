########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Classes
########################################################################################################################


class PROPERTIES_PT_layer_manager(bpy.types.Panel):
    bl_context = 'view_layer'
    bl_label = 'blrendertools'
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'

    def draw(self, context):
        lay = self.layout
        lay.use_property_decorate = False

        for layer in bpy.context.scene.view_layers:
            box = lay.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(layer, 'use', text='', icon='RESTRICT_RENDER_OFF' if layer.use else 'RESTRICT_RENDER_ON')
            row.prop(layer, 'name', text='')
            man = row.operator('blrendertools.manage_layer_collections', icon='OUTLINER_COLLECTION', text='')
            man.layer_name = layer.name
            delete_view_layer = row.operator('blrendertools.delete_view_layer', icon='X', text='')
            delete_view_layer.layer_name = layer.name
            row = col.row(align=True)
            row.prop(layer, 'samples')
            row.prop(layer, 'material_override', text='')
            row.prop(layer, 'world_override', text='')
            row = col.row(align=True)
            row.prop(layer.blrendertools.view_layers, 'notes', text='')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        PROPERTIES_PT_layer_manager,
    ]
)
