import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'romania.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,m in pivots.items():assert max(abs(v-bpy.data.objects[n].matrix_world[i][j]) for i,row in enumerate(m) for j,v in enumerate(row))<1e-7
objects=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
ornaments=[o for o in objects if o.name.startswith(('Roof','Spire','Border'))]
def theme(items):
 assert len([o for o in items if o.name.startswith('Roof shingle')])==100
 assert len([o for o in items if o.name.startswith('Border diamond')])==56
 assert len([o for o in items if o.name.startswith('Spire')])==3
 assert all(o.parent==lid for o in items)
 assert max((o.matrix_world@v.co).z for o in items for v in o.data.vertices)<=3.13
 assert not any('Cedar tree' in o.name or 'Terrain' in o.name for o in objects)
theme(ornaments)
# Real negative control: same validator, missing lid ownership.
probe=ornaments[0];old=probe.parent;probe.parent=None
try:theme(ornaments)
except AssertionError:negative=True
else:negative=False
probe.parent=old;assert negative
r={'status':'PASS','pivots_match_included_mechanism':True,'shingles':100,'diamond_segments':56,'spires':3,'ornaments':len(ornaments),'lid_parentage':True,'max_height':max((o.matrix_world@v.co).z for o in ornaments for v in o.data.vertices),'detached_ornament_negative_control_rejected':negative,'source':'Saved source independently reopened'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
