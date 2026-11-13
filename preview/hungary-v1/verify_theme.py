import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'hungary.blend'),use_scripts=False)
bpy.context.view_layer.update()
if '--negative' in sys.argv:bpy.data.objects['Rosette center / 0'].parent=None
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
orn=[o for o in meshes if o.name.startswith(('Rosette','Petal','Floral','Leaf'))]
counts={p:sum(o.name.startswith(p) for o in meshes) for p in ['Rosette','Petal','Leaf','Floral']}
assert counts=={'Rosette':5,'Petal':40,'Leaf':8,'Floral':4},counts
assert all(o.parent and o.parent.name=='Lid_Hinge' for o in orn),'Detached ornament'
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
bounds=[[min(v[i] for v in verts),max(v[i] for v in verts)] for i in range(3)]
assert bounds[0][0]>-1.6 and bounds[0][1]<1.6 and bounds[1][0]>-.9 and bounds[1][1]<.9 and bounds[2][0]>=1.97 and bounds[2][1]<=2.22,bounds
assert not any(o.name.startswith(('Cedar','Terrain','Finger','Lid finger')) for o in meshes)
# Original supplied source, independently opened, gives authoritative pivot transforms.
pivots={n:list(bpy.data.objects[n].matrix_local) for n in ['Lid_Hinge','Latch_Pivot']}
pivots={n:[list(row) for row in m] for n,m in pivots.items()}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-6
result={'status':'PASS','counts':counts,'ornament_bounds':bounds,'lid_parentage':True,'inherited_pivots_exact':True,'no_cedar_geometry':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
