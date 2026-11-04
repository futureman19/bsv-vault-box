import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'guatemala.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
terrain=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Terrain /')]
peaks=[o for o in terrain if 'volcano' in o.name]
def bounds(o):
 v=[o.matrix_world@v.co for v in o.data.vertices];return [[min(p[i] for p in v),max(p[i] for p in v)] for i in range(3)]
def ownership():assert len(terrain)==4 and all(o.parent==lid for o in terrain),'Detached or missing landscape'
ownership();assert len(peaks)==3
negative=False;old=peaks[0].parent;peaks[0].parent=None
try:ownership()
except AssertionError:negative=True
finally:peaks[0].parent=old
assert negative
pb=[bounds(o) for o in peaks];assert all(.30<b[2][1]-1.978<.75 and b[1][0]>0 for b in pb)
lake=bpy.data.objects['Terrain / contiguous lake'];lb=bounds(lake);assert lb[0][1]-lb[0][0]>1.3 and lb[1][1]-lb[1][0]>.6
# Downward exposed-water rays test actual surface, not name alone.
hits=[]
for x in [-.8,-.4,0,.4,.8]:
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,-.22,4)),Vector((0,0,-1)));assert hit and o==lake;hits.append([x,loc.z])
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
current={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
# Independently open the inherited mechanism to compare evaluated pivot matrices.
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
errors=[abs(current[name][i][j]-bpy.data.objects[name].matrix_world[i][j]) for name in current for i in range(4) for j in range(4)]
assert max(errors)<1e-7
out=dict(status='PASS',landscape_meshes=len(terrain),volcano_bounds=pb,lake_bounds=lb,exposed_lake_rays=hits,detached_landscape_negative_control_rejected=negative,pivot_matrix_max_error=max(errors),slab_dimensions=[3.72,2.38,.30],limits='Stylized peaks, no geographic accuracy; sampled surface rays only')
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS',json.dumps(out))
