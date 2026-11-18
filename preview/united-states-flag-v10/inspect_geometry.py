import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline-v7.blend'),use_scripts=False);bpy.context.view_layer.update()
a=[]
for o in bpy.data.objects:
 if o.type!='MESH' or o.name.startswith('Studio'):continue
 v=[o.matrix_world@x.co for x in o.data.vertices]
 a.append(dict(name=o.name,bounds=[[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]],materials=[m.name for m in o.data.materials]))
(R/'geometry-inspection.json').write_text(json.dumps(a,indent=2));print(json.dumps(a))
