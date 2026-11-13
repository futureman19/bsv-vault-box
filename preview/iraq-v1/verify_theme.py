import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'iraq.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def validate():
 tiers=[o for o in bpy.data.objects if o.name.startswith('Babylon tier')]
 assert len(tiers)==3,'three architectural tiers required'
 assert all(o.parent==lid for o in tiers),'tiers must travel with lid'
 assert all(o.parent==lid for o in bpy.data.objects if o.name.startswith(('Rosette','Lid border')))
 assert not any(o.name.startswith(('Cedar','Terrain / moss','Granite')) for o in bpy.data.objects)
 assert (lid.location-Vector((0,1.32,1.668))).length<1e-5
 slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5
 assert len([o for o in bpy.data.objects if o.name.startswith('Glazed brick')])>100
 return tiers
tiers=validate();old=tiers[0].parent;tiers[0].parent=None
try:validate()
except AssertionError as e:negative=str(e)
else:raise AssertionError('negative ancestry control did not fail')
tiers[0].parent=old;validate()
r={'status':'PASS','three_tiers':True,'ornaments_lid_borne':True,'cobalt_brick_count':len([o for o in bpy.data.objects if o.name.startswith('Glazed brick')]),'negative_control_detected':negative}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
