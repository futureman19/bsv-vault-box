import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'grenada.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def check_ornaments():
 groups={prefix:[o for o in bpy.data.objects if o.name.startswith(prefix) and not (prefix=='Botanical / leaf ' and o.name.startswith('Botanical / leaf vein'))] for prefix in ['Nutmeg / seed','Mace / open curling rib','Fruit / split cheek','Botanical / leaf ','Botanical / branch']}
 assert [len(v) for v in groups.values()]==[1,9,2,4,1]
 for objects in groups.values():
  for o in objects:
   assert o.parent==lid,('detached',o.name)
   for v in o.data.vertices:
    p=o.matrix_world@v.co
    assert abs(p.x)<1.8 and abs(p.y)<1.19 and 1.94<p.z<2.978,(o.name,tuple(p))
    if o.name.startswith('Mace /'):assert p.z>1.978,('mace below lid top',o.name,p.z)
 return {k:len(v) for k,v in groups.items()}
counts=check_ornaments()
seed=bpy.data.objects['Nutmeg / seed'];old=seed.parent;seed.parent=None
try:
 check_ornaments()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached ornament was incorrectly accepted')
seed.parent=old
# Independent baseline pivot comparison through saved scenes, not unevaluated appended objects.
current={o.name:list(o.matrix_local) for o in [lid,latch]}
current={k:[list(row) for row in v] for k,v in current.items()}
palette={n:list(bpy.data.materials[n].diffuse_color) for n in ['Mace / scarlet aril','Leaves / deep green','Fruit / golden split husk']}
assert palette['Mace / scarlet aril'][0]>palette['Mace / scarlet aril'][1]*4
assert palette['Leaves / deep green'][1]>palette['Leaves / deep green'][0]*2
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(current[n][i][j]-bpy.data.objects[n].matrix_local[i][j]) for n in current for i in range(4) for j in range(4));assert error<1e-7
out={'status':'PASS','counts':counts,'lid_ancestry_and_bounds':True,'palette':palette,'independent_pivot_max_error':error,'negative_control':{'mutation':'detach seed from lid in memory only','rejected':negative}}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));print('THEME PASS')
