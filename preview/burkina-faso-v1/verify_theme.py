"""Independent saved-source visual-contract assertions, not name-only acceptance."""
import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'burkina-faso.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert tuple(round(v,6) for v in lid.location)==(0,1.32,1.668),tuple(lid.location)
assert latch.parent==lid
objects=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
ornaments=[o for o in objects if o.name.startswith('Courtyard /')]
volumes=[o for o in ornaments if o.name.startswith('Courtyard / volume')]
assert len(volumes)==3 and len(ornaments)>=14
assert all(o.parent==lid for o in ornaments)
verts=[o.matrix_world@v.co for o in ornaments for v in o.data.vertices]
assert max(abs(v.x) for v in verts)<=1.55 and max(abs(v.y) for v in verts)<=.9
assert min(v.z for v in verts)>=1.976 and max(v.z for v in verts)<=2.56
assert all(.18<=o.dimensions.z<=.55 for o in volumes)
assert not any(any(word in o.name.lower() for word in ['cedar','moss','glacier','finger','tree']) for o in objects)
assert all(o.dimensions.z<=.12 for o in objects if o.name.startswith('Seam /'))
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
m=bpy.data.materials['Earth / fine plaster'];bsdf=m.node_tree.nodes.get('Principled BSDF');assert bsdf.inputs['Normal'].is_linked and bsdf.inputs['Roughness'].is_linked and bsdf.inputs['Base Color'].is_linked
images=[i for i in bpy.data.images if i.packed_file];assert len(images)==3 and all(tuple(i.size)==(256,256) for i in images)
# Every mesh under either articulated ancestor must be covered by the collision harness's direct-parent set.
for o in objects:
 p=o.parent
 while p:
  if p in [lid,latch]:assert o.parent in [lid,latch],o.name
  p=p.parent
out={'status':'PASS','theme':'Earthen Courtyard','ornaments':len(ornaments),'volumes':len(volumes),'lid_parentage':True,'ornament_bounds':[[min(v[i] for v in verts),max(v[i] for v in verts)] for i in range(3)],'source_packed_maps':[i.name for i in images],'no_foreign_theme_meshes':True,'body_width':slab.dimensions.x,'body_depth':slab.dimensions.y,'pivots_preserved':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
