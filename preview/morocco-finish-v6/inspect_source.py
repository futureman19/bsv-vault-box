import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline/morocco.blend'),use_scripts=False)
out={}
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith(('Lid /','Ceramic tessera','Tile bed'))):
  v=[o.matrix_world@x.co for x in o.data.vertices];out[o.name]={'bounds':[[min(x[i] for x in v),max(x[i] for x in v)] for i in range(3)],'materials':[m.name for m in o.data.materials],'uv':[(l.name,len(l.data)) for l in o.data.uv_layers],'matrix':[list(r) for r in o.matrix_world]}
(R/'source-inspection.json').write_text(json.dumps(out,indent=2));print(out)
