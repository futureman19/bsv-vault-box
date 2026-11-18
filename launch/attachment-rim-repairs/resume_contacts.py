"""Independently reopen final source and validate repair contacts and coplanarity."""
import bpy,json,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];slug=sys.argv[sys.argv.index('--')+1];root=R/'preview'/f'{slug}-repair-v2'
bpy.ops.wm.open_mainfile(filepath=str(root/f'{slug}.blend'),use_scripts=False);bpy.context.view_layer.update()
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
pairs=json.loads((root/'repair-check.json').read_text())['repaired_surface_intersections']
for a,b in pairs:assert tree(bpy.data.objects[a]).overlap(tree(bpy.data.objects[b])),(a,b)
heights={}
if slug=='guyana':
 for n in ['Seam / long','Seam / long.001','Seam / side','Seam / side.001']:
  o=bpy.data.objects[n];heights[n]=max((o.matrix_world@v.co).z for v in o.data.vertices)
 for a in ['Seam / long','Seam / long.001']:
  for b in ['Seam / side','Seam / side.001']:assert .0039<heights[a]-heights[b]<.0041
report={'saved_source_reopened':True,'all_repair_contact_pairs_verified':pairs,'guyana_top_heights':heights,'scope':'BVH surface contact, not welded/manifold construction; distinct rim top planes where strips intersect'}
(root/'reopened-contacts.json').write_text(json.dumps(report,indent=2));print(report)
