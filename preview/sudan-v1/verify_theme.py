"""Independent saved-source theme checks plus deliberately mutated negative controls."""
import bpy,json,math
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'sudan.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
ps=sorted([o for o in bpy.data.objects if o.name.startswith('Pyramid /')],key=lambda o:o.name)
def bounds(o):
 v=[o.matrix_world@x.co for x in o.data.vertices]
 return [min(x[i] for x in v) for i in range(3)],[max(x[i] for x in v) for i in range(3)]
def tree(o):
 return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
def check_pyramids(objects):
 assert len(objects)==3,'Exactly three pyramids required'
 for o,h in zip(objects,[.55,1.05,.80]):
  assert o.parent==lid,'Pyramid must travel with lid'
  lo,hi=bounds(o);assert abs(hi[2]-lo[2]-h)<1e-5,'Pyramid height mismatch'
  assert o['courses']==12 and len(o.data.polygons)==72,'Real course geometry required'
  assert tree(o).overlap(tree(bpy.data.objects['Terrain / ochre dunes'])),'Pyramid is not seated in dune terrain: '+o.name
check_pyramids(ps)
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.3)))
assert abs(lid.location.y-1.32)<1e-5 and abs(lid.location.z-1.668)<1e-5
assert latch.parent==lid
assert not any('Cedar' in o.name or 'moss' in o.name.lower() for o in bpy.data.objects)
seams=[o for o in bpy.data.objects if o.name.startswith('Mineral seam')];assert seams and all(o.dimensions.z<.12 for o in seams)
assert len([o for o in bpy.data.objects if o.name.startswith('Sandstone foot')])==4
m=bpy.data.materials['Sandstone / ochre porous'];assert any(n.type=='NORMAL_MAP' for n in m.node_tree.nodes)
neg=[]
def reject(name,fn):
 try:fn()
 except AssertionError as e:neg.append({'control':name,'rejected':True,'reason':str(e)})
 else:raise AssertionError('Negative control incorrectly passed: '+name)
reject('missing pyramid',lambda:check_pyramids(ps[:2]))
ps[0].parent=None
reject('detached pyramid',lambda:check_pyramids(ps))
ps[0].parent=lid
out={'status':'PASS','theme':'Meroë / Desert Gold','pyramids':[{ 'name':o.name,'height':o['height_contract'],'courses':o['courses']} for o in ps],'lid_dimensions':list(slab.dimensions),'seam_max_height':max(o.dimensions.z for o in seams),'pyramids_seated':True,'negative_controls':neg,'scope':'Saved-source shape/pivot/material contract, not archaeological accuracy'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
