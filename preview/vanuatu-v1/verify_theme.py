"""Independent saved-source geometry/ancestry gates with genuine negative controls."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'vanuatu.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,expected in pivots.items():
 assert max(abs(bpy.data.objects[n].matrix_world[i][j]-expected[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];crater=bpy.data.objects['Terrain / Yasur recessed crater'];ember=bpy.data.objects['Terrain / Ember basin']
def check_parent():assert crater.parent==lid and ember.parent==lid,'terrain detached from lid'
def check_depth():
 verts=[crater.matrix_world@v.co for v in crater.data.vertices];z=max(v.z for v in verts)
 assert 2.55<z<2.71 and z-ember.matrix_world.translation.z-ember.data.vertices[0].co.z>.40,'crater depth lost'
 return z
check_parent();summit=check_depth()
negative=[]
ember.parent=None
try:check_parent()
except AssertionError as e:negative.append(str(e))
else:raise AssertionError('ancestry negative control accepted')
ember.parent=lid;bpy.context.view_layer.update()
# Do not save mutations; restore exact matrix from reopened source for second control.
bpy.ops.wm.open_mainfile(filepath=str(R/'vanuatu.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];crater=bpy.data.objects['Terrain / Yasur recessed crater'];ember=bpy.data.objects['Terrain / Ember basin']
ember.location.z+=.6;bpy.context.view_layer.update()
try:check_depth()
except AssertionError as e:negative.append(str(e))
else:raise AssertionError('depth negative control accepted')
bpy.ops.wm.open_mainfile(filepath=str(R/'vanuatu.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];crater=bpy.data.objects['Terrain / Yasur recessed crater'];ember=bpy.data.objects['Terrain / Ember basin']
check_parent();check_depth()
# Source ray proves actual depressed ember center and elevated rim, not just names.
dep=bpy.context.evaluated_depsgraph_get()
def down(x,y):
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(dep,Vector((x,y,4)),Vector((0,0,-1)));assert hit;return o.name,loc.z
center=down(0,.12);rim=down(.74,.12)
assert center[0]==ember.name and rim[0]==crater.name and rim[1]-center[1]>.40
# Actual ember boundary stays within the crater crown in XY (ray crossing).
ring=[crater.matrix_world@v.co for v in list(crater.data.vertices)[288:384]]
def inside(v):
 crossings=0
 for a,b in zip(ring,ring[1:]+ring[:1]):
  if (a.y>v.y)!=(b.y>v.y) and v.x<(b.x-a.x)*(v.y-a.y)/(b.y-a.y)+a.x:crossings+=1
 return crossings%2==1
assert all(inside(ember.matrix_world@v.co) for v in ember.data.vertices)
# Dimensions and maps are read from source, not generator constants.
slab=bpy.data.objects['Lid / polished slab'];assert max(abs(a-b) for a,b in zip(slab.dimensions,(3.72,2.38,.30)))<1e-5
assert len([o for o in bpy.data.objects if o.name.startswith('Volcanic foot')])==4
assert all(max(i.size)<=512 for i in bpy.data.images if i.packed_file)
r={'status':'PASS','pivot_identity':True,'lid_dimensions':list(slab.dimensions),'summit_z':summit,'center_ray':center,'rim_ray':rim,'depth':rim[1]-center[1],'terrain_ancestry':True,'negative_controls_rejected':negative,'limitations':'No geographic exactness; negative controls post-authoring, not test-first evidence.'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
