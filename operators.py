########################################################################################################################
# Imports
########################################################################################################################


if 'bpy' in locals():
    import importlib

    common = importlib.reload(common)
else:
    from . import common
    import bpy
    import pprint


########################################################################################################################
# Operators
########################################################################################################################


class BLRENDERTOOLS_OT_create_material(bpy.types.Operator):
    '''Create a new material'''

    bl_idname = 'blrendertools.create_material'
    bl_label = 'Create New Material'
    bl_options = {'BLOCKING'}

    material_name: bpy.props.StringProperty(name='Name', default='myAwesomeMaterial')
    material_color: bpy.props.FloatVectorProperty(name='Color', subtype='COLOR', size=4, default=[0.8, 0.8, 0.8, 1])
    material_metallic: bpy.props.FloatProperty(name='Metallic', min=0, max=1, default=0)
    material_roughness: bpy.props.FloatProperty(name='Roughness', min=0, max=1, default=0.5)
    material_count: bpy.props.IntProperty(name='Number of Materials', min=1, default=1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        name_keyword = self.material_name.split('.')[0]
        for i in range(self.material_count):
            mat = bpy.data.materials.new(name=f'{name_keyword}.MAT.001')
            mat.diffuse_color = self.material_color
            mat.metallic = self.material_metallic
            mat.roughness = self.material_roughness
            mat.use_nodes = True
            principled_bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
            principled_bsdf.inputs[0].default_value = self.material_color
            principled_bsdf.inputs[1].default_value = self.material_metallic
            principled_bsdf.inputs[2].default_value = self.material_roughness
        return {'FINISHED'}


class BLRENDERTOOLS_OT_assign_material(bpy.types.Operator):
    '''Overwrite any materials on all selected objects with this material'''

    bl_idname = 'blrendertools.assign_material'
    bl_label = 'Assign Material to Selected'
    bl_options = {'BLOCKING'}

    material_name: bpy.props.StringProperty()

    def execute(self, context):
        selected_objects = [
            ob
            for ob in context.selected_objects
            if ob.type in ['MESH', 'CURVE'] and not common.is_datablock_linked(datablock=ob.data)
        ]
        for ob in selected_objects:
            ob.data.materials.clear()
            ob.data.materials.append(bpy.data.materials[self.material_name])
        return {'FINISHED'}


class BLRENDERTOOLS_OT_reveal_material_users(bpy.types.Operator):
    '''Print the names of all data-blocks using this material'''

    bl_idname = 'blrendertools.reveal_material_users'
    bl_label = 'Reveal Material Users'
    bl_options = {'BLOCKING'}

    material_name: bpy.props.StringProperty()

    def execute(self, context):
        names = []
        for ob in bpy.data.objects:
            if 'material_slots' in ob.keys():
                for slot in ob.material_slots:
                    if slot.material == bpy.data.materials[self.material_name]:
                        names.append(ob.name)
        pprint.pprint(names)
        return {'FINISHED'}


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


class BLRENDERTOOLS_OT_manage_image_sequences(bpy.types.Operator):
    '''Manage Image Sequences'''

    bl_idname = 'blrendertools.manage_image_sequences'
    bl_label = 'Image Sequence Manager'
    bl_options = {'BLOCKING'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        lay = self.layout
        images = [img for img in bpy.data.images if img.source == 'SEQUENCE']
        row = lay.row(align=True)
        row.operator('blrendertools.guess_frame_range', icon='RIGHTARROW')
        row.operator('blrendertools.update_image_sequence_nodes', icon='NODE')
        box = lay.box()
        for img in images:
            row = box.row(align=True)
            row.prop(img, 'name', text='')
            row.prop(img.blrendertools, 'frame_start')
            row.prop(img.blrendertools, 'frame_end')
            row.prop(img.blrendertools, 'frame_entry')

    def execute(self, context):
        return {'FINISHED'}


class BLRENDERTOOLS_OT_guess_frame_range(bpy.types.Operator):
    '''Guess image sequence start and end frames'''

    bl_idname = 'blrendertools.guess_frame_range'
    bl_label = 'Guess Frame Ranges'
    bl_options = {'BLOCKING'}

    def execute(self, context):
        images = [img for img in bpy.data.images if img.source == 'SEQUENCE']
        for img in images:
            first_node = next((n for n in context.scene.node_tree.nodes if n.type == 'IMAGE' and n.image == img), None)
            if first_node:
                img.blrendertools.frame_start = first_node.frame_start
                img.blrendertools.frame_end = first_node.frame_start + first_node.frame_duration - 1
                img.blrendertools.frame_entry = 2 * first_node.frame_start - first_node.frame_offset - 1
        return {'FINISHED'}


class BLRENDERTOOLS_OT_update_image_sequence_nodes(bpy.types.Operator):
    '''Update Image Sequence node start and end frames'''

    bl_idname = 'blrendertools.update_image_sequence_nodes'
    bl_label = 'Update Nodes'
    bl_options = {'BLOCKING'}

    def execute(self, context):
        images = [img for img in bpy.data.images if img.source == 'SEQUENCE']
        for img in images:
            nodes = [n for n in context.scene.node_tree.nodes if n.type == 'IMAGE' and n.image == img]
            for node in nodes:
                node.frame_duration = img.blrendertools.frame_end - img.blrendertools.frame_start + 1
                node.frame_start = img.blrendertools.frame_start
                node.frame_offset = img.blrendertools.frame_entry - 1
        return {'FINISHED'}


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLRENDERTOOLS_OT_assign_material,
        BLRENDERTOOLS_OT_create_material,
        BLRENDERTOOLS_OT_delete_view_layer,
        BLRENDERTOOLS_OT_guess_frame_range,
        BLRENDERTOOLS_OT_manage_image_sequences,
        BLRENDERTOOLS_OT_manage_layer_collections,
        BLRENDERTOOLS_OT_reveal_material_users,
        BLRENDERTOOLS_OT_update_image_sequence_nodes,
    ]
)
