import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'south-sudan.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; stems=[o for o in bpy.data.objects if o.name.startswith('Papyrus / stem')]; banks=[o for o in bpy.data.objects if o.name.startswith('Wetland / bank')];ornaments=[o for o in bpy.data.objects if o.name.startswith(('Wetland /','Papyrus /'))]
if '--negative' in sys.argv:stems[0].parent=None
assert len(stems)==21 and len(banks)==3
assert all(o.parent==lid for o in ornaments),'Detached wetland ornament'
verts=[o.matrix_world@v.co for o in ornaments for v in o.data.vertices]
assert max(v.z for v in verts)<2.65
assert max(abs(v.x) for v in verts)<1.65 and max(abs(v.y) for v in verts)<.94
water=bpy.data.objects['Wetland / water']; dep=bpy.context.evaluated_depsgraph_get()
# Exposed channel samples between separated banks, not hydrology proof.
hits=[]
for x,y in [(-.43,-.3),(.55,-.4),(0,-.65)]:
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(dep,Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and o==water,(x,y,o.name);hits.append([x,y,loc.z])
result={'status':'PASS','stems':len(stems),'banks':len(banks),'lid_owned_ornaments':len(ornaments),'max_z':max(v.z for v in verts),'exposed_water_rays':hits,'negative_control':'--negative detaches one stem and must fail'}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(result)
