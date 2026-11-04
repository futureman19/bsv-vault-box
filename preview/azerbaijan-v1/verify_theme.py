import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'azerbaijan.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[o for o in bpy.data.objects if o.name.startswith('Ornament')];leaves=[o for o in orn if 'leaf' in o.name];rings=[o for o in orn if 'ring' in o.name]
def check(items):
 assert len([o for o in items if 'leaf' in o.name])==8,'Eight leaves required'
 assert all(o.parent==lid for o in items),'All relief lid-owned'
check(orn)
negative=False
try:check([o for o in orn if o!=leaves[0]])
except AssertionError:negative=True
assert negative and len(rings)==2
coords=[o.matrix_world@v.co for o in orn for v in o.data.vertices];zmin=min(v.z for v in coords);zmax=max(v.z for v in coords);assert 1.978-1e-5<=zmin and zmax<=1.978+.22
med=bpy.data.objects['Ornament / medallion'];assert .65<=med.dimensions.x/2<=.85
# Real separated co-moving leaf volume envelopes, not only moving/static tests.
def tree(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
assert not any(tree(a).overlap(tree(b)) for i,a in enumerate(leaves) for b in leaves[i+1:])
assert all(not any(s in o.name for s in ['Cedar','Terrain','Moss','Granite']) for o in bpy.data.objects)
mat=bpy.data.materials['Lahij / hammered copper'];bs=mat.node_tree.nodes.get('Principled BSDF');assert bs.inputs['Metallic'].default_value>.7 and bs.inputs['Normal'].is_linked
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
report={'status':'PASS','leaf_count':len(leaves),'rings':len(rings),'ornament_count':len(orn),'ornament_z':[zmin,zmax],'medallion_radius':med.dimensions.x/2,'all_lid_owned':True,'leaf_separation':True,'missing_leaf_negative_control_rejected':negative}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(bpy.data.objects[n].matrix_world[i][j]-a[i][j]) for n,a in pivots.items() for i in range(4) for j in range(4));assert error<1e-7;report['baseline_pivot_max_error']=error
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
