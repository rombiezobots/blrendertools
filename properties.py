########################################################################################################################
# Imports
########################################################################################################################


import bpy
from . import images, materials, subdivision, view_layers


########################################################################################################################
# Functions
########################################################################################################################


########################################################################################################################
# Classes
########################################################################################################################


class BlrendertoolsImageProperties(bpy.types.PropertyGroup):
    images: bpy.props.PointerProperty(name='Images', type=images.properties.ImagesImageProperties)


class BlrendertoolsMaterialProperties(bpy.types.PropertyGroup):
    materials: bpy.props.PointerProperty(name='Materials', type=materials.properties.MaterialsMaterialProperties)


class BlrendertoolsCollectionProperties(bpy.types.PropertyGroup):
    subdivision: bpy.props.PointerProperty(
        name='Subdivision', type=subdivision.properties.SubdivisionCollectionProperties
    )


class BlrendertoolsSceneProperties(bpy.types.PropertyGroup):
    subdivision: bpy.props.PointerProperty(name='Subdivision', type=subdivision.properties.SubdivisionSceneProperties)
    materials: bpy.props.PointerProperty(name='Materials', type=materials.properties.MaterialsSceneProperties)


class BlrendertoolsViewLayerProperties(bpy.types.PropertyGroup):
    view_layers: bpy.props.PointerProperty(
        name='Subdivision', type=view_layers.properties.ViewLayersViewLayerProperties
    )


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    BlrendertoolsMaterialProperties,
    BlrendertoolsCollectionProperties,
    BlrendertoolsSceneProperties,
    BlrendertoolsImageProperties,
    BlrendertoolsViewLayerProperties,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.blrendertools = bpy.props.PointerProperty(
        type=BlrendertoolsSceneProperties,
        name='blrendertools',
    )
    bpy.types.Collection.blrendertools = bpy.props.PointerProperty(
        type=BlrendertoolsCollectionProperties,
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
    bpy.types.ViewLayer.blrendertools = bpy.props.PointerProperty(
        type=BlrendertoolsViewLayerProperties,
        name='blrendertools',
    )


def unregister():
    del bpy.types.ViewLayer.blrendertools
    del bpy.types.Image.blrendertools
    del bpy.types.Material.blrendertools
    del bpy.types.Collection.blrendertools
    del bpy.types.Scene.blrendertools
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
