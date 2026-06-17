########################################################################################################################
# Imports
########################################################################################################################


import bpy
from .. import utils


########################################################################################################################
# Globals
########################################################################################################################


SUBSURF_MODIFIER_PROPERTIES = [
    'boundary_smooth',
    'levels',
    'name',
    'remove',
    'render_levels',
    'show_in_editmode',
    'show_on_cage',
    'show_only_control_edges',
    'show_render',
    'show_viewport',
    'subdivision_type',
    'uv_smooth',
]


########################################################################################################################
# Operators
########################################################################################################################


class BLRENDERTOOLS_OT_manage_subdivision(bpy.types.Operator):
    '''Manage Subdivision Surface modifiers'''

    bl_idname = 'blrendertools.manage_subdivision'
    bl_label = 'Subdivision Manager'
    bl_options = {'BLOCKING'}

    collection_index: bpy.props.IntProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        lay.use_property_decorate = False

        row_active_collection = lay.row()
        row_active_collection.prop(context.scene.blrendertools.subdivision, 'active_collection')
        collection = context.scene.blrendertools.subdivision.active_collection
        if not collection:
            return
        row_active_collection.separator()
        row_active_collection.prop(collection.blrendertools.subdivision, 'enable')
        if not collection.blrendertools.subdivision.enable:
            return
        row_active_collection.operator('blrendertools.update_subdiv', text='', icon='FILE_REFRESH')

        box_collection_props = lay.box()

        row_header = box_collection_props.row()
        row_align = row_header.row(align=True)
        row_align.prop(collection.blrendertools.subdivision, 'name', text='')
        row_align.prop(collection.blrendertools.subdivision, 'show_on_cage', text='', icon='MESH_DATA')
        row_align.prop(collection.blrendertools.subdivision, 'show_in_editmode', text='', icon='EDITMODE_HLT')
        row_align.prop(collection.blrendertools.subdivision, 'show_viewport', text='', icon='RESTRICT_VIEW_OFF')
        row_align.prop(collection.blrendertools.subdivision, 'show_render', text='', icon='RESTRICT_RENDER_OFF')
        row_header.prop(collection.blrendertools.subdivision, 'remove', text='', icon='X')

        row_subdiv_type = box_collection_props.row(align=True)
        row_subdiv_type.use_property_split = False
        row_subdiv_type.prop(collection.blrendertools.subdivision, 'subdivision_type', expand=True)

        col_body = box_collection_props.column()

        col_levels = col_body.column(align=True)
        col_levels.prop(collection.blrendertools.subdivision, 'levels')
        col_levels.prop(collection.blrendertools.subdivision, 'render_levels')

        col_body.prop(collection.blrendertools.subdivision, 'show_only_control_edges')
        col_body.prop(collection.blrendertools.subdivision, 'uv_smooth')
        col_body.prop(collection.blrendertools.subdivision, 'boundary_smooth')
        col_body.prop(collection.blrendertools.subdivision, 'force_modifier')

    def execute(self, context):
        # Iterate over all collections in the file that Subdivision Manager has been enabled for.
        collections = [
            c
            for c in bpy.data.collections
            if c.blrendertools.subdivision.enable and not utils.is_datablock_linked(datablock=c)
        ]
        for collection in collections:
            settings = collection.blrendertools.subdivision
            # Iterate over all meshes and curves in the collection.
            for ob in [
                o
                for o in collection.objects
                if o.type in ['MESH', 'CURVE'] and not utils.is_datablock_linked(datablock=o)
            ]:
                # Find the first Subdivision Surface modifier in the stack. If there is none, and settings.force_modifier is enabled, create one. If not, continue.
                modifier = next((m for m in ob.modifiers if m.type == 'SUBSURF'), None)
                if not modifier and settings.force_modifier:
                    modifier = ob.modifiers.new(name='Subdivision', type='SUBSURF')
                if not modifier:
                    continue
                # Iterate over the property names in the list. For each match, transfer the setting's value to the modifier.
                for key in SUBSURF_MODIFIER_PROPERTIES:
                    if hasattr(modifier, key):
                        setattr(modifier, key, getattr(settings, key))
        return {'FINISHED'}


class BLRENDERTOOLS_OT_update_subdiv(bpy.types.Operator):
    '''Update subdivision settings for objects inside this Collection'''

    bl_idname = 'blrendertools.update_subdiv'
    bl_label = 'Update Subdivision In Collection'
    bl_options = {'BLOCKING'}

    def execute(self, context):
        return {'FINISHED'}


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLRENDERTOOLS_OT_manage_subdivision,
        BLRENDERTOOLS_OT_update_subdiv,
    ]
)
