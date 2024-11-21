########################################################################################################################
# Imports
########################################################################################################################


if 'bpy' in locals():
    import importlib

    operators = importlib.reload(operators)
    panels = importlib.reload(panels)
    properties = importlib.reload(properties)
    uilists = importlib.reload(uilists)
    menus = importlib.reload(menus)

else:
    import bpy
    from . import operators
    from . import panels
    from . import properties
    from . import uilists
    from . import menus


########################################################################################################################
# Add-on information
########################################################################################################################


bl_info = {
    'author': 'rombiezobots',
    'blender': (4, 2, 0),
    'category': 'Render',
    'name': 'blrendertools',
    'wiki_url': 'https://rombiezobots.com/',
}


########################################################################################################################
# Registration
########################################################################################################################


modules = [
    properties,
    uilists,
    operators,
    panels,
    menus,
]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()


if __name__ == '__main__':
    register()
