import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'afghanistan.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,v in pivots.items():assert (bpy.data.objects[n].matrix_world.translation-Vector(v)).length<1e-7
ridge=bpy.data.objects['Terrain / Hindu Kush three peaks'];lid=bpy.data.objects['Lid_Hinge']
def owned(o):assert o.parent==lid,'Relief detached from lid'
owned(ridge);ridge.parent=None
try:owned(ridge)
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached terrain negative control accepted')
verts=[ridge.matrix_world@v.co for v in ridge.data.vertices]
# Restore original scene rather than retain mutated probe transforms.
bpy.ops.wm.open_mainfile(filepath=str(R/'afghanistan.blend'),use_scripts=False);bpy.context.view_layer.update();ridge=bpy.data.objects['Terrain / Hindu Kush three peaks'];verts=[ridge.matrix_world@v.co for v in ridge.data.vertices]
assert max(abs(v.x) for v in verts)<=1.35 and max(abs(v.y) for v in verts)<=.75
height=max(v.z for v in verts)-1.978;assert .25<=height<=.70
assert abs(min(v.z for v in verts)-1.970)<1e-5
# Three ridge summit neighborhoods, separated by lower saddles.
peaks=[]
for lo,hi in [(-1.1,-.5),(-.3,.3),(.5,1.1)]:peaks.append(max(v.z for v in verts if lo<v.x<hi))
assert min(peaks)>2.25 and peaks[1]>peaks[0] and peaks[1]>peaks[2]
assert not any('Cedar' in o.name or 'moss' in o.name.lower() for o in bpy.data.objects)
r=dict(status='PASS',negative_control=negative,pivots=pivots,pivot_parity=True,terrain_height=height,peak_heights=peaks,terrain_owned_by_lid=True,seated_bottom_z=min(v.z for v in verts),interpretation='Invented mountain relief; not surveyed terrain')
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
