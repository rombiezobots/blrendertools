########################################################################################################################
# Imports
########################################################################################################################


if 'bpy' in locals():
    import importlib

else:
    import bpy


########################################################################################################################
# Functions
########################################################################################################################


def on_select_swap_material_b(self, context):
    materials_to_swap = [m for m in bpy.data.materials if m.blrendertools.is_selected]
    if not (materials_to_swap or self.material_swap):
        return
    for ob in [o for o in bpy.data.objects if hasattr(o, 'material_slots')]:
        for slot in [s for s in ob.material_slots if s.material in materials_to_swap]:
            original_name = slot.material.name
            slot.material = self.material_swap
            print(f'Swapped {original_name} for {self.material_swap.name} on {ob.name}')
    for m in materials_to_swap:
        bpy.data.materials.remove(material=m)
    self.material_swap = None


########################################################################################################################
# Classes
########################################################################################################################


class SubdivisionSettings(bpy.types.PropertyGroup):

    enable: bpy.props.BoolProperty(name='Manage Subdivs', default=False)
    force_modifier: bpy.props.BoolProperty(name='Add Modifier If Not Present', default=False)

    name: bpy.props.StringProperty(name='Name', default='Subdivision')
    show_on_cage: bpy.props.BoolProperty(name='On Cage', default=False)
    show_in_editmode: bpy.props.BoolProperty(name='Edit Mode', default=True)
    show_viewport: bpy.props.BoolProperty(name='Realtime', default=True)
    show_render: bpy.props.BoolProperty(name='Render', default=True)
    remove: bpy.props.BoolProperty(name='Remove', default=False)
    subdivision_type: bpy.props.EnumProperty(
        name='Select type of subdivision algorithm',
        items=[
            ('CATMULL_CLARK', 'Catmull-Clark', 'CATMULL_CLARK'),
            ('SIMPLE', 'Simple', 'SIMPLE'),
        ],
        default='CATMULL_CLARK',
    )
    levels: bpy.props.IntProperty(name='Levels Viewport', default=1)
    render_levels: bpy.props.IntProperty(name='Render', default=2)
    show_only_control_edges: bpy.props.BoolProperty(name='Optimal Display', default=True)
    uv_smooth: bpy.props.EnumProperty(
        name='UV Smooth',
        items=[
            ('NONE', 'None', 'NONE'),
            ('PRESERVE_CORNERS', 'Keep Corners', 'PRESERVE_CORNERS'),
            ('PRESERVE_CORNERS_AND_JUNCTIONS', 'Keep Corners, Junctions', 'PRESERVE_CORNERS_AND_JUNCTIONS'),
            (
                'PRESERVE_CORNERS_JUNCTIONS_AND_CONCAVE',
                'Keep Corners, Junctions, Concave',
                'PRESERVE_CORNERS_JUNCTIONS_AND_CONCAVE',
            ),
            ('PRESERVE_BOUNDARIES', 'Keep Boundaries', 'PRESERVE_BOUNDARIES'),
            ('SMOOTH_ALL', 'All', 'SMOOTH_ALL'),
        ],
        default='PRESERVE_BOUNDARIES',
    )
    boundary_smooth: bpy.props.EnumProperty(
        name='Boundary Smooth',
        items=[
            ('ALL', 'All', 'ALL'),
            ('PRESERVE_CORNERS', 'Keep Corners', 'PRESERVE_CORNERS'),
        ],
        default='PRESERVE_CORNERS',
    )


class BlrendertoolsImageProperties(bpy.types.PropertyGroup):

    frame_start: bpy.props.IntProperty(name='Start')
    frame_end: bpy.props.IntProperty(name='End')
    frame_entry: bpy.props.IntProperty(name='Entry')


class BlrendertoolsMaterialProperties(bpy.types.PropertyGroup):

    is_panel_open: bpy.props.BoolProperty(default=False)
    is_selected: bpy.props.BoolProperty(name='Select', default=False)


class BlrendertoolsCollectionProperties(bpy.types.PropertyGroup):

    subdivision: bpy.props.PointerProperty(name='Subdivision Settings', type=SubdivisionSettings)


class BlrendertoolsSceneProperties(bpy.types.PropertyGroup):

    active_collection_subdiv: bpy.props.PointerProperty(name='Collection', type=bpy.types.Collection)
    material_swap: bpy.props.PointerProperty(
        name='Replace Selected With', type=bpy.types.Material, update=on_select_swap_material_b
    )


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    SubdivisionSettings,
    BlrendertoolsMaterialProperties,
    BlrendertoolsCollectionProperties,
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


def unregister():
    del bpy.types.Image.blrendertools
    del bpy.types.Material.blrendertools
    del bpy.types.Collection.blrendertools
    del bpy.types.Scene.blrendertools
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
