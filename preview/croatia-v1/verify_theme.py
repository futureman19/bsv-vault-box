import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'croatia.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
def check():
 lakes=[o for o in bpy.data.objects if o.name.startswith('Lake /')];terraces=[o for o in bpy.data.objects if o.name.startswith('Terrace /')];cascades=[o for o in bpy.data.objects if o.name.startswith('Cascade /')]
 assert len(lakes)==len(terraces)==3 and len(cascades)==2
 ornaments=lakes+terraces+cascades+[o for o in bpy.data.objects if o.name.startswith('Bank moss')]
 assert all(o.parent==lid for o in ornaments),'detached ornament'
 vertices=[o.matrix_world@v.co for o in ornaments for v in o.data.vertices]
 assert max(v.z for v in vertices)<2.65 and min(v.z for v in vertices)>=1.96
 levels=sorted(max((o.matrix_world@v.co).z for v in o.data.vertices) for o in lakes)
 assert all(.17<b-a<.19 for a,b in zip(levels,levels[1:]))
 assert max(v.x for v in vertices)<1.5 and min(v.x for v in vertices)>-1.5
 # Cascade face centers must be visible from directly above, not inside a stone wall.
 hits=[]
 for o in cascades:
  for f in o.data.polygons:
   p=o.matrix_world@f.center
   hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((p.x,p.y,3)),Vector((0,0,-1)))
   assert hit and obj.name==o.name,('occluded cascade',o.name,obj.name if hit else None)
   hits.append(obj.name)
 variations={}
 for image in bpy.data.images:
  if image.packed_file and image.name in ['tufa-color.png','tufa-roughness.png','stone-foot.png']:
   pixels=list(image.pixels);v=max(pixels[0::4])-min(pixels[0::4]);assert v>.03;variations[image.name]=v
 assert len(variations)==3
 assert tuple(round(v,3) for v in lid.location)==(0,1.32,1.668)
 return {'PASS':True,'water_levels':levels,'ornaments':len(ornaments),'exposed_cascade_face_rays':hits,'map_variations':variations,'max_ornament_z':max(v.z for v in vertices)}
r=check()
obj=bpy.data.objects['Lake / 0'];obj.parent=None
try:check()
except AssertionError as e:negative={'PASS':True,'rejected_detached_lake':str(e)}
else:raise AssertionError('negative control incorrectly passed')
(R/'negative-control.json').write_text(json.dumps(negative,indent=2))
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r));print('NEGATIVE CONTROL PASS',negative)
