"""Independently reopen saved source; geometry tests and real negative control."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'saint-kitts-and-nevis.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,expected in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-expected[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];a=bpy.data.objects['Terrain / Saint Kitts crater'];b=bpy.data.objects['Terrain / Nevis peak']
def ancestry(o):
 while o.parent:
  o=o.parent
  if o==lid:return True
 return False
assert ancestry(a) and ancestry(b)
b.parent=None
try:
 assert ancestry(b)
except AssertionError:negative=True
else:negative=False
b.parent=lid
assert negative,'Detached ornament negative control not detected'
# Restore reopened source to avoid altering any transform during negative control.
bpy.ops.wm.open_mainfile(filepath=str(R/'saint-kitts-and-nevis.blend'),use_scripts=False);bpy.context.view_layer.update()
a=bpy.data.objects['Terrain / Saint Kitts crater'];b=bpy.data.objects['Terrain / Nevis peak']
def vertices(o):return [o.matrix_world@v.co for v in o.data.vertices]
def bounds(o):
 v=vertices(o);return {'min':[min(p[i] for p in v) for i in range(3)],'max':[max(p[i] for p in v) for i in range(3)]}
A=bounds(a);B=bounds(b);gap=B['min'][0]-A['max'][0];assert gap>=.15
for q in [A,B]:
 assert q['min'][0]>=-1.65 and q['max'][0]<=1.65 and q['min'][1]>=-.95 and q['max'][1]<=.95
 assert 1.977<=q['min'][2]<=2.002 and .3<=q['max'][2]-1.978<=.95
# Center depression must be below a surrounding annulus; true surface vertices not labels.
v=vertices(a);center=v[0].z;ring=[v[1+6*72+j].z for j in range(72)];assert min(ring)-center>.1
# Nevis center is a peak above its outer slopes.
v=vertices(b);assert v[0].z-max(p.z for p in v[1+18*72:])>.3
assert all(i.packed_file for i in bpy.data.images if i.name.startswith('volcanic-'))
assert len([o for o in bpy.data.objects if o.name.startswith('Terrain /')])==2
out={'status':'PASS','pivot_baseline_exact':True,'two_lid_owned_islands':True,'detached_ornament_negative_control_rejected':negative,'island_bounds':{'Saint Kitts':A,'Nevis':B},'minimum_X_channel_gap':gap,'crater_center_z':center,'minimum_ring_z':min(ring),'crater_depression':min(ring)-center,'peak_above_outer_slopes':True,'procedural_maps_packed':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
