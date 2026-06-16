########################################################################################################################
# Imports
########################################################################################################################


_needs_reload = 'bpy' in locals()
import bpy
from . import operators
from . import panels
from . import properties
from . import uilists
from . import menus
from . import ui

if _needs_reload:
    import importlib

    operators = importlib.reload(operators)
    panels = importlib.reload(panels)
    properties = importlib.reload(properties)
    uilists = importlib.reload(uilists)
    menus = importlib.reload(menus)
    ui = importlib.reload(ui)


########################################################################################################################
# Add-on information
########################################################################################################################


bl_info = {
    'author': 'rombiezobots',
    'blender': (5, 0, 0),
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
    ui,
]


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()


if __name__ == '__main__':
    register()
