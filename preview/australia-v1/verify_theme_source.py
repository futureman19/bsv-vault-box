import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'australia.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(bpy.data.objects[n].matrix_local[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-8
lid=bpy.data.objects['Lid_Hinge'];domes=[o for o in bpy.data.objects if o.name.startswith('Dome /')];assert len(domes)==5
bounds=[]
for o in domes:
 assert o.parent==lid
 vs=[o.matrix_world@v.co for v in o.data.vertices]
 lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
 assert 1.96<lo[2]<1.98 and 2.3<hi[2]<=2.90
 assert lo[0]>-1.5 and hi[0]<1.5 and lo[1]>-.75 and hi[1]<.91
 bounds.append({'name':o.name,'min':lo,'max':hi})
# Each dome footprint is separated in XY from each other dome (AABB sufficient here).
for i,a in enumerate(bounds):
 for b in bounds[i+1:]:assert any(a['max'][k]<b['min'][k] or b['max'][k]<a['min'][k] for k in [0,1]),(a,b)
# Prove ownership gate rejects a detached ornament, without writing mutated source.
def owned():return all(o.parent==lid for o in domes)
domes[0].parent=None;assert not owned();domes[0].parent=lid
images=[i for i in bpy.data.images if i.packed_file];assert len(images)==3
assert all(tuple(i.size)==(512,512) for i in images)
assert not any(any(w in o.name.lower() for w in ['cedar','moss','granite','glacier']) for o in bpy.data.objects)
result={'status':'PASS','same_mechanism_pivots':True,'dome_count':len(domes),'dome_bounds':bounds,'separated_domes':True,'detached_ornament_negative_control':'REJECTED as required','packed_maps':[i.name for i in images]}
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
