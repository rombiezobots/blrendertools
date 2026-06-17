########################################################################################################################
# Imports
########################################################################################################################


_needs_reload = 'bpy' in locals()
import bpy
from . import animation
from . import cameras
from . import images
from . import materials
from . import subdivision
from . import view_layers
from . import properties
from . import menus


if _needs_reload:
    import importlib

    animation = importlib.reload(animation)
    cameras = importlib.reload(cameras)
    images = importlib.reload(images)
    materials = importlib.reload(materials)
    subdivision = importlib.reload(subdivision)
    view_layers = importlib.reload(view_layers)
    properties = importlib.reload(properties)
    menus = importlib.reload(menus)


########################################################################################################################
# Registration
########################################################################################################################


def register():
    animation.register()
    cameras.register()
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
    cameras.unregister()
    animation.unregister()


if __name__ == '__main__':
    register()
