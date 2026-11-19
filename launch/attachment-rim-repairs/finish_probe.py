import bpy,json
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish'
for row in json.loads((D/'targets.json').read_text()):
 root=R/row['root']; sources=[root/'original'/(row['id']+'.blend')];assert sources[0].is_file(),sources
 bpy.ops.wm.open_mainfile(filepath=str(sources[0]),use_scripts=False);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 trees={};rows=[]
 for o in bpy.data.objects:
  if o.type!='MESH' or o.name.startswith('Studio'):continue
  ev=o.evaluated_get(dg);m=ev.to_mesh();v=[o.matrix_world@v.co for v in m.vertices]
  trees[o.name]=BVHTree.FromPolygons(v,[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear()
  rows.append({'name':o.name,'bounds':[[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]],'parent':o.parent.name if o.parent else None})
 contacts={n:[other for other in trees if other!=n and trees[n].overlap(trees[other])] for n in trees if any(w in n.lower() for w in ['seam','rim','hinge','tree','canopy','trunk'])}
 (root/'baseline-probe.json').write_text(json.dumps({'source':sources[0].name,'objects':rows,'contacts':contacts},indent=2));print(row['id'],len(rows),flush=True)
