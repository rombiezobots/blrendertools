########################################################################################################################
# Imports
########################################################################################################################


if 'bpy' in locals():
    import importlib

    common = importlib.reload(common)
else:
    from . import common
    import bpy


########################################################################################################################
# Functions
########################################################################################################################


def tags():
    return [(tag.name, tag.name, tag.name) for tag in bpy.context.scene.blrendertools.material_tags]


########################################################################################################################
# Classes
########################################################################################################################


class BlrendertoolsImageProperties(bpy.types.PropertyGroup):

    frame_start: bpy.props.IntProperty(name='Start')
    frame_end: bpy.props.IntProperty(name='End')
    frame_entry: bpy.props.IntProperty(name='Entry')


class BlrendertoolsMaterialTag(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(default='Tag')


class BlrendertoolsMaterialProperties(bpy.types.PropertyGroup):

    is_panel_open: bpy.props.BoolProperty(default=False)
    tags: bpy.props.CollectionProperty(name='Tags', type=BlrendertoolsMaterialTag)
    tag_index: bpy.props.IntProperty(name='Tag')


class BlrendertoolsSceneProperties(bpy.types.PropertyGroup):

    material_tags: bpy.props.CollectionProperty(name='Tags', type=BlrendertoolsMaterialTag)


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    BlrendertoolsMaterialTag,
    BlrendertoolsMaterialProperties,
    BlrendertoolsSceneProperties,
    BlrendertoolsImageProperties,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.blrendertools = bpy.props.PointerProperty(
        type=BlrendertoolsSceneProperties,
        name='blrendertools',
    )
    bpy.types.Material.blrendertools = bpy.props.PointerProperty(
        type=BlrendertoolsMaterialProperties,
        name='blrendertools',
    )
    bpy.types.Image.blrendertools = bpy.props.PointerProperty(
        type=BlrendertoolsImageProperties,
        name='blrendertools',
    )


def unregister():
    del bpy.types.Image.blrendertools
    del bpy.types.Material.blrendertools
    del bpy.types.Scene.blrendertools
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
