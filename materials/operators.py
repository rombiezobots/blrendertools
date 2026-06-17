########################################################################################################################
# Imports
########################################################################################################################


import bpy
from .. import utils


########################################################################################################################
# Globals
########################################################################################################################


########################################################################################################################
# Operators
########################################################################################################################


class BLRENDERTOOLS_OT_create_material(bpy.types.Operator):
    '''Create a new material'''

    bl_idname = 'blrendertools.create_material'
    bl_label = 'Create New Material'
    bl_options = {'BLOCKING'}

    material_name: bpy.props.StringProperty(name='Name', default='myAwesomeMaterial')
    material_color: bpy.props.FloatVectorProperty(name='Color', subtype='COLOR', size=4, default=[0.8, 0.8, 0.8, 1])
    material_metallic: bpy.props.FloatProperty(name='Metallic', min=0, max=1, default=0)
    material_roughness: bpy.props.FloatProperty(name='Roughness', min=0, max=1, default=0.5)
    material_count: bpy.props.IntProperty(name='Number of Materials', min=1, default=1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        name_keyword = self.material_name.split('.')[0]
        for i in range(self.material_count):
            mat = bpy.data.materials.new(name=f'{name_keyword}.MAT.001')
            mat.diffuse_color = self.material_color
            mat.metallic = self.material_metallic
            mat.roughness = self.material_roughness
            mat.use_nodes = True
            principled_bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
            principled_bsdf.inputs[0].default_value = self.material_color
            principled_bsdf.inputs[1].default_value = self.material_metallic
            principled_bsdf.inputs[2].default_value = self.material_roughness
        return {'FINISHED'}


class BLRENDERTOOLS_OT_assign_material(bpy.types.Operator):
    '''Overwrite any materials on all selected objects with this material'''

    bl_idname = 'blrendertools.assign_material'
    bl_label = 'Assign Material to Selected'
    bl_options = {'BLOCKING'}

    material_name: bpy.props.StringProperty()

    def execute(self, context):
        selected_objects = [
            ob
            for ob in context.selected_objects
            if ob.type in ['MESH', 'CURVE'] and not utils.is_datablock_linked(datablock=ob.data)
        ]
        for ob in selected_objects:
            ob.data.materials.clear()
            ob.data.materials.append(bpy.data.materials[self.material_name])
        return {'FINISHED'}


class BLRENDERTOOLS_OT_reveal_material_users(bpy.types.Operator):
    '''Print the names of all data-blocks using this material'''

    bl_idname = 'blrendertools.reveal_material_users'
    bl_label = 'Reveal Material Users'
    bl_options = {'BLOCKING'}

    material_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        objects = [ob for ob in bpy.data.objects if hasattr(ob, 'material_slots')]
        names = []
        for ob in objects:
            for slot in ob.material_slots:
                if slot.material == bpy.data.materials[self.material_name]:
                    names.append(ob.name)
        print(f'Material users for {self.material_name}:', names)
        return {'FINISHED'}


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLRENDERTOOLS_OT_assign_material,
        BLRENDERTOOLS_OT_create_material,
        BLRENDERTOOLS_OT_reveal_material_users,
    ]
)
