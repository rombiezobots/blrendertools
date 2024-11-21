########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Classes
########################################################################################################################


class BLRENDERTOOLS_UL_view_layers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        layout.use_property_decorate = False
        row = layout.row()
        row.prop(item, 'use', text='')
        row.label(text=item.name)


class BLRENDERTOOLS_UL_material_tags(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        layout.use_property_decorate = False
        row = layout.row()
        row.label(text=item.name)


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLRENDERTOOLS_UL_view_layers,
        BLRENDERTOOLS_UL_material_tags,
    ]
)
