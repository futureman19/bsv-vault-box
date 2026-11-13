"""Independent saved-source visual contract and adversarial ancestry check."""
import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
pivots={n:tuple(tuple(v for v in row) for row in bpy.data.objects[n].matrix_local) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'lesotho.blend'),use_scripts=False)
def check():
 lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];assert latch.parent==lid
 for n,mat in pivots.items():assert max(abs(bpy.data.objects[n].matrix_local[i][j]-mat[i][j]) for i in range(4) for j in range(4))<1e-7
 ridge=bpy.data.objects['Maloti / three peak ridge'];panel=bpy.data.objects['Lid / woven indigo inset']
 ornaments=[o for o in bpy.data.objects if o.name.startswith(('Maloti /','Highland /','Lid / woven'))]
 assert len(ornaments)==21 and all(o.parent==lid for o in ornaments),'All ornaments must travel with lid'
 v=[ridge.matrix_world@v.co for v in ridge.data.vertices]
 assert min(p.x for p in v)>=-1.45 and max(p.x for p in v)<=1.45
 assert min(p.y for p in v)>=-.90 and max(p.y for p in v)<=.90
 top=max(p.z for p in v);assert .35<=top-1.978<=.70,top
 # Project maximum top elevation per X slice; separate 3 substantial crests.
 profile=[]
 for x in sorted(set(round(p.x,4) for p in v)):profile.append((x,max(p.z for p in v if abs(p.x-x)<.0001)))
 peaks=[profile[i] for i in range(1,len(profile)-1) if profile[i][1]>profile[i-1][1] and profile[i][1]>profile[i+1][1] and profile[i][1]>2.18]
 assert len(peaks)==3,peaks
 for o in bpy.data.objects:
  if o.name.startswith('Seam /'):assert o.dimensions.z<=.09
 slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
 images=[i for i in bpy.data.images if i.packed_file];assert len(images)==3
 for i in images:
  assert max(i.size)<=512 and min(i.size)>0
  p=list(i.pixels)[::4];assert max(p)-min(p)>.01
 assert panel.data.materials[0].name.startswith('Textile /')
 return {'status':'PASS','peak_count':len(peaks),'peaks':peaks,'ridge_top_z':top,'ornament_count':len(ornaments),'exact_inherited_pivots':True,'packed_maps':[i.name for i in images]}
bpy.context.view_layer.update();result=check()
# Real in-memory mutation; no saved source edits. Must be rejected.
ridge=bpy.data.objects['Maloti / three peak ridge'];original=ridge.parent;ridge.parent=None
try:check()
except AssertionError as e:result['negative_control']={'detached_ridge_rejected':True,'failure':str(e)}
else:raise AssertionError('Negative control was not rejected')
ridge.parent=original
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',json.dumps(result))
