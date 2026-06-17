########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def on_select_swap_material_b(self, context):
    if not self.material_swap:
        return
    materials_to_swap = [m for m in bpy.data.materials if m.blrendertools.is_selected]
    if not materials_to_swap:
        return
    objects_with_materials = [o for o in bpy.data.objects if hasattr(o, 'material_slots')]
    for ob in objects_with_materials:
        for slot in [
            s for s in ob.material_slots if s.material in materials_to_swap and not s.material == self.material_swap
        ]:
            original_name = slot.material.name
            slot.material = self.material_swap
            print(f'Swapped {original_name} for {self.material_swap.name} on {ob.name}')
    for m in materials_to_swap:
        bpy.data.materials.remove(material=m)
    self.material_swap = None


########################################################################################################################
# Classes
########################################################################################################################


class MaterialsMaterialProperties(bpy.types.PropertyGroup):
    is_panel_open: bpy.props.BoolProperty(default=False)
    is_selected: bpy.props.BoolProperty(name='Select', default=False)


class MaterialsSceneProperties(bpy.types.PropertyGroup):
    material_swap: bpy.props.PointerProperty(
        name='Replace Selected With',
        type=bpy.types.Material,
        update=on_select_swap_material_b,
    )


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        MaterialsMaterialProperties,
        MaterialsSceneProperties,
    ]
)
