########################################################################################################################
# Imports
########################################################################################################################


import bpy
from operator import attrgetter
from .. import utils


########################################################################################################################
# Classes
########################################################################################################################


class PROPERTIES_PT_material_manager(bpy.types.Panel):
    bl_context = 'material'
    bl_label = 'blrendertools'
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'

    def draw(self, context):
        lay = self.layout

        box_buttons = lay.box()
        box_buttons.operator('blrendertools.create_material', icon='ADD')

        box_swap_materials = lay.box()
        box_swap_materials.use_property_split = True
        col = box_swap_materials.column(align=True)
        col.prop(context.scene.blrendertools.materials, 'material_swap')

        mats = [
            m
            for m in sorted(bpy.data.materials, key=attrgetter('name'))
            if not utils.is_datablock_linked(datablock=m) and not m.grease_pencil
        ]

        # First create a dict to not lose the panel references.
        panels = {}
        for mat in mats:
            panels[mat.name] = lay.panel_prop(mat.blrendertools.materials, 'is_panel_open')

            # Top row.
            row_header = panels[mat.name][0].row(align=True)
            split_name_color = row_header.split(factor=0.65, align=True)
            split_name_color.prop(mat, 'name', text='')
            split_name_color.prop(mat, 'diffuse_color', text='')
            reveal_material_users = row_header.operator('blrendertools.reveal_material_users', text='', icon='USER')
            reveal_material_users.material_name = mat.name
            assign_material = row_header.operator('blrendertools.assign_material', text='', icon='MATERIAL_DATA')
            assign_material.material_name = mat.name
            row_header.prop(
                mat,
                'use_fake_user',
                text='',
                icon='FAKE_USER_ON' if mat.use_fake_user else 'FAKE_USER_OFF',
            )
            row_header.prop(
                mat.blrendertools.materials,
                'is_selected',
                text='',
                icon='FILE_REFRESH',
            )

            # Extras.
            if panels[mat.name][1]:
                panel = panels[mat.name][1]
                panel.use_property_split = True
                col = panel.column(align=True)
                col.prop(mat, 'metallic')
                col.prop(mat, 'roughness')


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        PROPERTIES_PT_material_manager,
    ]
)
