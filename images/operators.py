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
        images = [img for img in bpy.data.images if img.source == 'SEQUENCE']
        for img in images:
            first_node = next(
                (n for n in context.scene.compositing_node_group.nodes if n.type == 'IMAGE' and n.image == img), None
            )
            if first_node:
                img.blrendertools.images.frame_start = first_node.frame_start
                img.blrendertools.images.frame_end = first_node.frame_start + first_node.frame_duration - 1
                img.blrendertools.images.frame_entry = 2 * first_node.frame_start - first_node.frame_offset - 1
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        lay = self.layout
        images = [img for img in bpy.data.images if img.source == 'SEQUENCE']
        box = lay.box()
        for img in images:
            col = box.column(align=True)
            name_and_filepath = col.row(align=True)
            name_and_filepath.prop(img, 'name', text='')
            name_and_filepath.prop(img, 'filepath', text='')
            frame_range = col.row(align=True)
            frame_range.prop(img.blrendertools.images, 'frame_start')
            frame_range.prop(img.blrendertools.images, 'frame_end')
            frame_range.prop(img.blrendertools.images, 'frame_entry')

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
        BLRENDERTOOLS_OT_manage_image_sequences,
    ]
)
