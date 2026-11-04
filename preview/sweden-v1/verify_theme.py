import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:list(sum((list(row) for row in bpy.data.objects[n].matrix_world),[])) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'sweden.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,v in baseline.items():assert max(abs(a-b) for a,b in zip(v,sum((list(row) for row in bpy.data.objects[n].matrix_world),[])))<1e-8
lid=bpy.data.objects['Lid_Hinge'];ornaments=[o for o in bpy.data.objects if o.name.startswith('Kurbits /')]
def validate():
 assert len(ornaments)==51,len(ornaments)
 assert all(o.parent==lid for o in ornaments),'ornament detached from lid'
 for prefix,count in [('Kurbits / flower petal',24),('Kurbits / red flower heart',3),('Kurbits / green leaf',10),('Kurbits / ivory leaf',10)]:assert len([o for o in ornaments if o.name.startswith(prefix)])==count
validate()
o=ornaments[0];o.parent=None
try:validate()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached ornament negative control was not rejected')
o.parent=lid;validate()
slab=bpy.data.objects['Lid / polished slab'];assert max(abs(a-b) for a,b in zip(slab.dimensions,(3.72,2.38,.30)))<1e-5
relief=[o for o in ornaments if 'blue inset' not in o.name];points=[o.matrix_world@v.co for o in relief for v in o.data.vertices]
bounds=[[min(v[i] for v in points),max(v[i] for v in points)] for i in range(3)]
assert bounds[0][0]>-1.4 and bounds[0][1]<1.4 and bounds[1][0]>-.78 and bounds[1][1]<.78
assert bounds[2][0]>2.02 and bounds[2][1]<2.22
assert not any(o.name.startswith(('Cedar tree','Terrain')) for o in bpy.data.objects)
r={'status':'PASS','ornaments':len(ornaments),'flower_rosettes':3,'petals':24,'leaves':20,'relief_bounds_xyz':bounds,'slab_dimensions':list(slab.dimensions),'inherited_pivots_exact':True,'negative_control_rejected':negative,'no_inherited_tree_or_terrain':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
