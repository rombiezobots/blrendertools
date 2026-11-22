########################################################################################################################
# Imports
########################################################################################################################


import importlib

import bpy


########################################################################################################################
# Functions
########################################################################################################################


def is_datablock_linked(datablock: bpy.types.ID) -> bool:
    return datablock.library or datablock.override_library


def register_submodule_factory(module_name: str, submodule_names: list):
    '''Like bpy.utils.register_submodule_factory, but unregistering leaves the submodules imported. Blender's removes
    them from their package and from sys.modules, so reloading or enabling the add-on again breaks modules that still
    refer to them, such as the add-on-wide properties.py.'''

    def submodules() -> list:
        return [importlib.import_module(f'{module_name}.{name}') for name in submodule_names]

    def register():
        for submodule in submodules():
            submodule.register()

    def unregister():
        for submodule in reversed(submodules()):
            submodule.unregister()

    return register, unregister
