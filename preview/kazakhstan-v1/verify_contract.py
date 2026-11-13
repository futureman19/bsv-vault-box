"""Independent saved-source design/pivot assertions; not a visual likeness test."""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'kazakhstan.blend'),use_scripts=False)
O=bpy.data.objects; slab=O['Lid / polished slab'];bpy.context.view_layer.update()
assert max(abs(a-b) for a,b in zip(slab.dimensions,(3.72,2.38,.30)))<1e-5
for o in O:
 if o.name.startswith(('Lid scroll','Lid medallion','Lid felt')):assert o.parent==O['Lid_Hinge']
 if o.name.startswith('Seam /'):assert o.dimensions.z<=.100001
 for word in ['Cedar tree','Terrain / granite','glacier']:
  assert not o.name.startswith(word)
med=[o for o in O if o.name.startswith('Lid medallion')]
z=[(o.matrix_world@v.co).z for o in med for v in o.data.vertices];assert max(z)-1.993<=.20
pivots={n:{'location':list(O[n].location),'rotation':list(O[n].rotation_euler),'parent':O[n].parent.name if O[n].parent else None} for n in ['Lid_Hinge','Latch_Pivot']}
assert len([o for o in O if o.name.startswith('Felt body')])==4
assert all(i.packed_file for i in bpy.data.images if i.name.endswith('.png'))
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
for n,v in pivots.items():
 o=bpy.data.objects[n]
 assert list(o.location)==v['location'] and list(o.rotation_euler)==v['rotation']
 assert (o.parent.name if o.parent else None)==v['parent']
out={'status':'PASS','slab_dimensions':[3.72,2.38,.30],'seam_height_max':.10,'ornament_relief_max_observed':max(z)-1.993,'pivots_exactly_equal_frozen_mechanism':pivots,'all_lid_ornament_parented':True,'maps_packed':True}
(R/'contract-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
