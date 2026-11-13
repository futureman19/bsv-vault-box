import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'togo.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];orn=[o for o in bpy.data.objects if o.name.startswith('Compound /')]
def ancestry():
 assert all(o.parent==lid for o in orn),'detached ornament'
ancestry()
towers=[o for o in orn if o.name.startswith('Compound / tower')];caps=[o for o in orn if o.name.startswith('Compound / thatch cap')]
assert len(towers)==4 and len(caps)==2 and len(orn)==12
bounds={o.name:[min((o.matrix_world@v.co).z for v in o.data.vertices),max((o.matrix_world@v.co).z for v in o.data.vertices)] for o in orn}
assert all(abs(bounds[o.name][0]-1.978)<1e-5 for o in towers)
assert max(b[1] for b in bounds.values())<=3.15
hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((0,0,3.3)),Vector((0,0,-1)))
assert hit and obj.name=='Lid / polished slab' and abs(loc.z-1.978)<1e-5
# Deliberately detached in-memory ornament must be rejected. Never saved.
o=towers[0];o.parent=None
try:ancestry()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control did not fail')
o.parent=lid;ancestry()
report={'status':'PASS','towers':len(towers),'caps':len(caps),'lid_owned_ornaments':len(orn),'bounds':bounds,'open_court_ray':obj.name,'court_z':loc.z,'negative_control':{'detached_tower':'FAIL as intended','reason':negative},'scope':'stylized miniature, no ethnographic accuracy claim'}
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
