import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
def snapshot():
 bpy.context.view_layer.update();out={}
 for o in bpy.data.objects:
  if o.name.startswith('Studio') or o.type not in ['MESH','EMPTY']:continue
  out[o.name]={'matrix':[list(r) for r in o.matrix_world],'parent':o.parent.name if o.parent else None,'verts':[list(v.co) for v in o.data.vertices] if o.type=='MESH' else []}
 return out
original=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(R/'united-states.blend'),use_scripts=False);current=snapshot()
for n,a in original.items():assert current[n]==a,n
r={'unchanged_mechanism_objects':list(original),'preserved_raw_geometry_transforms_parentage':True,'mechanism_sha256':hashlib.sha256((R/'mechanism.blend').read_bytes()).hexdigest(),'material_changes_allowed':True}
(R/'mechanism-check.json').write_text(json.dumps(r,indent=2));print(r)
