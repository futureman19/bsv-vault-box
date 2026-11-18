import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
slug=sys.argv[sys.argv.index('--')+1];root=R/'preview'/f'{slug}-repair-v2'
bpy.ops.wm.open_mainfile(filepath=str(root/'historical-v1'/f'{slug}.blend'),use_scripts=False);bpy.context.view_layer.update()
rows=[]
for o in bpy.data.objects:
 if o.type!='MESH' or not any(w in o.name.lower() for w in ['seam','rim','body','wall','hinge']):continue
 v=[o.matrix_world@v.co for v in o.data.vertices];rows.append({'name':o.name,'bounds':[[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]],'parent':o.parent.name if o.parent else None})
(root/'baseline-bounds.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
