import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'japan.blend'),use_scripts=False)
trunk=bpy.data.objects['Cedar tree / trunk'];bpy.context.view_layer.update();v=[trunk.matrix_world@p.co for p in trunk.data.vertices];bounds=[[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
assert bounds[0][0]>.4 and bounds[0][1]>.6 and bounds[1][0]<.9 and bounds[1][1]<1
assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in bpy.data.objects if o.name.startswith(('Cedar tree','Terrain /')))
(R/'placement-check.json').write_text(json.dumps({'trunk_world_bounds':bounds,'front':'-Y','back':'+Y','right':'+X','all_tree_terrain_parented_to_lid':True},indent=2))
cam=bpy.context.scene.camera;cam.location=(-5.6,-7.8,3.3);cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.render.filepath=str(R/'matched-reference.png');bpy.ops.render.render(write_still=True)
cam.location=(0,0,9);cam.rotation_euler=(0,0,0);cam.data.ortho_scale=4.7;bpy.context.scene.render.resolution_x=900;bpy.context.scene.render.resolution_y=900;bpy.context.scene.render.filepath=str(R/'top-down-source.png');bpy.ops.render.render(write_still=True)
