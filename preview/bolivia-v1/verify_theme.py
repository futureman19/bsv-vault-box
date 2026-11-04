import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'bolivia.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[o for o in bpy.data.objects if o.name.startswith('Uyuni /')]
def ownership():
 assert len(orn)>=17
 assert all(o.parent==lid for o in orn),'Detached lid ornament'
ownership();peak=bpy.data.objects['Uyuni / Tunupa relief'];mw=peak.matrix_world.copy();peak.parent=None
try:ownership();raise RuntimeError('Negative control was accepted')
except AssertionError as e:negative=str(e)
peak.parent=lid;peak.matrix_world=mw;ownership();bpy.context.view_layer.update()
vs=[peak.matrix_world@v.co for v in peak.data.vertices];assert min(v.x for v in vs)>0 and min(v.y for v in vs)>0
assert max(v.z for v in vs)<2.65 and min(v.z for v in vs)<2.006
assert len(peak.data.polygons)>100
polys=[o for o in orn if o.name.startswith('Uyuni / salt polygon')];assert len(polys)>=15
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5
actual={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(a-b) for n,mat in actual.items() for ar,br in zip(mat,bpy.data.objects[n].matrix_world) for a,b in zip(ar,br));assert error<1e-7
out={'status':'PASS','salt_polygon_count':len(polys),'ornaments_lid_owned':len(orn),'peak_vertices':len(vs),'peak_min':[min(v[i] for v in vs) for i in range(3)],'peak_max':[max(v[i] for v in vs) for i in range(3)],'original_pivot_max_error':error,'negative_control_rejected':negative,'scope':'Authored relief, not a geographic survey'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
