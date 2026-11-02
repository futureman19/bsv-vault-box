"""Independent saved-source contract, including real negative control."""
import bpy,json,math
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'kyrgyzstan.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def verts(o):return [o.matrix_world@v.co for v in o.data.vertices]
def tree(o):return BVHTree.FromPolygons(verts(o),[list(p.vertices) for p in o.data.polygons])
def gate():
 horns=[o for o in bpy.data.objects if o.name.startswith('Shyrdak / lid horn')]
 assert len(horns)==8
 assert all(o.parent==lid for o in horns)
 panel=bpy.data.objects['Felt lid / inset'];pt=tree(panel)
 for o in horns:
  assert tree(o).overlap(pt),('Floating lid horn',o.name)
  for v in verts(o):assert abs(v.x)<1.65 and abs(v.y)<.985 and 1.99<v.z<2.168
 assert tree(bpy.data.objects['Stitches / lid']).overlap(pt)
 assert len([o for o in bpy.data.objects if o.name.startswith('Felt panel /')])==4
 assert len([o for o in bpy.data.objects if o.name.startswith('Foot / walnut')])==4
 p=bpy.data.materials['Felt / crimson wool'].node_tree.nodes.get('Principled BSDF')
 assert p.inputs['Roughness'].default_value>=.8 and p.inputs['Metallic'].default_value==0
 assert bpy.data.materials['Brass / antique satin'].node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value>=.65
 for o in bpy.data.objects:
  if o.name.startswith('Seam /'):assert o.dimensions.z<=.10
 assert latch.parent==lid
 assert tuple(round(x,3) for x in lid.location)==(0,1.32,1.668),tuple(lid.location)
 return {'lid_horns':len(horns),'lid_horn_panel_contacts':len(horns),'wall_panels':4,'feet':4,'felt_roughness':p.inputs['Roughness'].default_value,'all_lid_ornaments_parented':True}
result=gate()
# Deliberately break actual loaded source ancestry, require same gate to fail.
o=bpy.data.objects['Shyrdak / lid horn'];old=o.parent;o.parent=None
caught=False
try:gate()
except AssertionError:caught=True
finally:o.parent=old
assert caught,'Theme gate failed to reject detached ornament'
result['negative_detached_ornament_rejected']=caught;result['status']='PASS';gate()
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',json.dumps(result))
