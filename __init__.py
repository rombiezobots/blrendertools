########################################################################################################################
# Imports
########################################################################################################################


_needs_reload = 'bpy' in locals()
import bpy

from . import animation, images, materials, menus, properties, subdivision, view_layers

if _needs_reload:
    import importlib

    animation = importlib.reload(animation)
    images = importlib.reload(images)
    materials = importlib.reload(materials)
    subdivision = importlib.reload(subdivision)
    view_layers = importlib.reload(view_layers)
    # These two refer to the packages above, so they are reloaded after them
    properties = importlib.reload(properties)
    menus = importlib.reload(menus)


########################################################################################################################
# Registration
########################################################################################################################


def register():
    animation.register()
    images.register()
    materials.register()
    subdivision.register()
    view_layers.register()
    properties.register()
    menus.register()


def unregister():
    menus.unregister()
    properties.unregister()
    view_layers.unregister()
    subdivision.unregister()
    materials.unregister()
    images.unregister()
    animation.unregister()


if __name__ == '__main__':
    register()
