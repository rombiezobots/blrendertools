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
            row.prop(img.blrendertools.images, 'frame_start')
            row.prop(img.blrendertools.images, 'frame_end')
            row.prop(img.blrendertools.images, 'frame_entry')

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
            first_node = next(
                (n for n in context.scene.compositing_node_group.nodes if n.type == 'IMAGE' and n.image == img), None
            )
            if first_node:
                img.blrendertools.images.frame_start = first_node.frame_start
                img.blrendertools.images.frame_end = first_node.frame_start + first_node.frame_duration - 1
                img.blrendertools.images.frame_entry = 2 * first_node.frame_start - first_node.frame_offset - 1
        return {'FINISHED'}


class BLRENDERTOOLS_OT_update_image_sequence_nodes(bpy.types.Operator):
    '''Update Image Sequence node start and end frames'''

    bl_idname = 'blrendertools.update_image_sequence_nodes'
    bl_label = 'Update Nodes'
    bl_options = {'BLOCKING'}

    def execute(self, context):
        images = [img for img in bpy.data.images if img.source == 'SEQUENCE']
        for img in images:
            nodes = [n for n in context.scene.compositing_node_group.nodes if n.type == 'IMAGE' and n.image == img]
            for node in nodes:
                node.frame_duration = img.blrendertools.images.frame_end - img.blrendertools.images.frame_start + 1
                node.frame_start = img.blrendertools.images.frame_start
                node.frame_offset = img.blrendertools.images.frame_entry - 1
        return {'FINISHED'}


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLRENDERTOOLS_OT_guess_frame_range,
        BLRENDERTOOLS_OT_manage_image_sequences,
        BLRENDERTOOLS_OT_update_image_sequence_nodes,
    ]
)
