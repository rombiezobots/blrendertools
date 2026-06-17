########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


########################################################################################################################
# Classes
########################################################################################################################


class SubdivisionCollectionProperties(bpy.types.PropertyGroup):
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


class SubdivisionSceneProperties(bpy.types.PropertyGroup):
    active_collection: bpy.props.PointerProperty(name='Collection', type=bpy.types.Collection)


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        SubdivisionCollectionProperties,
        SubdivisionSceneProperties,
    ]
)
