import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'myanmar.blend'),use_scripts=False)
bpy.context.view_layer.update()
def check():
 lid=bpy.data.objects['Lid_Hinge'];orn=[o for o in bpy.data.objects if o.name.startswith('Ornament /')]
 assert len(orn)==4
 assert all(o.parent==lid for o in orn),'Detached lid ornament'
 assert all(1.97<(o.matrix_world@v.co).z<2.07 for o in orn for v in o.data.vertices)
 slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
 skins=[o for o in bpy.data.objects if o.name.startswith('Lacquer /') and 'skin' in o.name];assert len(skins)==4
 assert len([i for i in bpy.data.images if i.packed_file])>=3
 assert bpy.data.materials['Lacquer / black vermilion yun-inspired'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].is_linked
 return {'ornaments':len(orn),'skins':len(skins),'lid_ancestry':True,'ornament_z_bounds':[1.97,2.07],'status':'PASS'}
out=check();o=bpy.data.objects['Ornament / brass oval 0'];old=o.parent;o.parent=None
try:check()
except AssertionError as e:out['detached_negative_control']={'status':'EXPECTED FAIL','message':str(e)}
else:raise AssertionError('Negative control failed to reject')
o.parent=old;check()
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
