import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline-v7.blend'))
bpy.context.view_layer.update()
out={}
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  out[o.name]=dict(parent=o.parent.name if o.parent else None,bounds=[[min(v[i] for v in vs),max(v[i] for v in vs)] for i in range(3)],materials=[m.name for m in o.data.materials])
(R/'geometry-probe.json').write_text(json.dumps(out,indent=2))
