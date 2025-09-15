########################################################################################################################
# Imports
########################################################################################################################


import bpy
from operator import attrgetter
from . import common


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
            row.prop(layer, 'use', text='')
            row.prop(layer, 'name', text='')
            man = row.operator('blrendertools.manage_layer_collections', icon='OUTLINER_COLLECTION', text='')
            man.layer_name = layer.name
            delete_view_layer = row.operator('blrendertools.delete_view_layer', icon='X', text='')
            delete_view_layer.layer_name = layer.name
            row = col.row(align=True)
            row.prop(layer, 'samples')
            row.prop(layer, 'material_override', text='')
            row.prop(layer, 'world_override', text='')


class PROPERTIES_PT_material_manager(bpy.types.Panel):
    bl_context = 'material'
    bl_label = 'blrendertools'
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'

    def draw(self, context):
        lay = self.layout
        lay.operator('blrendertools.create_material', icon='ADD')

        mats = [
            m
            for m in sorted(bpy.data.materials, key=attrgetter('name'))
            if not common.is_datablock_linked(datablock=m) and not m.grease_pencil
        ]

        # First create a dict to not lose the panel references.
        panels = {}
        for mat in mats:
            panels[mat.name] = lay.panel_prop(mat.blrendertools, 'is_panel_open')

            # Top row. Toggle collapse, isolate shot, shot name, and the assigned camera.
            row_header = panels[mat.name][0].row(align=True)
            split_name_color = row_header.split(factor=0.65, align=True)
            split_name_color.prop(mat, 'name', text='')
            split_name_color.prop(mat, 'diffuse_color', text='')
            reveal_material_users = row_header.operator('blrendertools.reveal_material_users', text='', icon='USER')
            reveal_material_users.material_name = mat.name
            assign_material = row_header.operator('blrendertools.assign_material', text='', icon='MATERIAL_DATA')
            assign_material.material_name = mat.name

            # Shot notes / description.
            if panels[mat.name][1]:
                col_body = panels[mat.name][1].column(align=True)
                col_body.prop(mat, 'metallic')
                col_body.prop(mat, 'roughness')
                col_body.template_list(
                    listtype_name='BLRENDERTOOLS_UL_material_tags',
                    list_id='',
                    dataptr=mat.blrendertools,
                    propname='tags',
                    active_dataptr=mat.blrendertools,
                    active_propname='tag_index',
                    rows=5,
                )


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        PROPERTIES_PT_layer_manager,
        PROPERTIES_PT_material_manager,
    ]
)
