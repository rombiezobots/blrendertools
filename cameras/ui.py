########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def draw_viewport_header(self, context):
    lay = self.layout
    lay.separator_spacer()
    lay.label(text='blrendertools')
    lay.separator()
    if not context.scene.camera:
        return
    if not context.scene.camera.data.show_background_images or len(context.scene.camera.data.background_images) == 0:
        return
    image = next((i for i in context.scene.camera.data.background_images if i.show_background_image), None)
    if not image:
        return
    lay.prop(image, 'alpha', text='Image Opacity')


########################################################################################################################
# Classes
########################################################################################################################


########################################################################################################################
# Registration
########################################################################################################################


def register():
    bpy.types.VIEW3D_HT_header.append(draw_viewport_header)


def unregister():
    bpy.types.VIEW3D_HT_header.remove(draw_viewport_header)
