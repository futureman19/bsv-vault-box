"""Material-only successor: reopen approved v5; preserve every geometry/UV record."""
import bpy
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline-v5.blend'),use_scripts=False)
wall=bpy.data.images.get('flag-wall.png')
wall.unpack(method='REMOVE');wall.filepath=str(R/'maps/flag-wall.png');wall.reload();wall.pack()
red=bpy.data.materials.new('Flag / red feet');red.use_nodes=True
bs=red.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.83077,.00243,.006995,1);bs.inputs['Roughness'].default_value=.27
red.diffuse_color=(.83077,.00243,.006995,1)
for o in bpy.data.objects:
 if 'stone foot' in o.name:o.data.materials.clear();o.data.materials.append(red)
scene=bpy.context.scene
scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'united-states.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge']
bpy.ops.export_scene.gltf(filepath=str(R/'united-states.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'blender-source-no-fx.png');bpy.ops.render.render(write_still=True)
print('V6 material-only source saved/exported/rendered')
