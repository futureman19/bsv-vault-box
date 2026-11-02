import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'morocco.blend'),use_scripts=False);bpy.context.view_layer.update()
o=bpy.data.objects['Atlas ridge / rear centre eroded massif'];v=[o.matrix_world@p.co for p in o.data.vertices];bounds=[[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
assert -.5<bounds[0][0]<0 and bounds[1][0]<.7 and bounds[0][1]>.7 and bounds[1][1]<1.4 and o.parent.name=='Lid_Hinge'
# Actual ridge is seated across both the wood field and rear mosaic bed.
assert abs(bounds[0][2]-2.17)<1e-5
(R/'placement-check.json').write_text(json.dumps({'ridge_world_bounds':bounds,'front':'-Y','back':'+Y','right':'+X','ridge_lid_child':True},indent=2))
cam=bpy.context.scene.camera;cam.location=(-5.6,-7.8,4.8);cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.render.filepath=str(R/'matched-reference.png');bpy.ops.render.render(write_still=True)
cam.location=(0,0,9);cam.rotation_euler=(0,0,0);cam.data.ortho_scale=4.7;bpy.context.scene.render.resolution_x=900;bpy.context.scene.render.resolution_y=900;bpy.context.scene.render.filepath=str(R/'top-down-source.png');bpy.ops.render.render(write_still=True)
