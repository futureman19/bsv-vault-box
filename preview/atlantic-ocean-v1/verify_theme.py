import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'atlantic.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
def check():
 for n in ['Ridge / east','Ridge / west','Rift / continuous channel']:
  assert bpy.data.objects[n].parent==lid,n
check()
o=bpy.data.objects['Ridge / east'];o.parent=None
try:check()
except AssertionError:negative=True
else:negative=False
assert negative;o.parent=lid
# Read original source again after deliberately detaching without saving.
bpy.ops.wm.open_mainfile(filepath=str(R/'atlantic.blend'),use_scripts=False);bpy.context.view_layer.update()
def verts(n):
 o=bpy.data.objects[n];return [o.matrix_world@v.co for v in o.data.vertices]
e=verts('Ridge / east');w=verts('Ridge / west');r=verts('Rift / continuous channel')
gaps=[e[j*7].x-w[j*7].x for j in range(25)]
assert min(gaps)>.12
assert 2.08<max(v.z for v in e+w)<2.40
assert max(v.y for v in e)-min(v.y for v in e)>1.6
# Every sampled center channel ray must hit the inlay, not an occluding ridge.
for j in range(24):
 c=(r[j*2]+r[j*2+1]+r[j*2+2]+r[j*2+3])/4
 hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((c.x,c.y,3)),Vector((0,0,-1)))
 assert hit and obj.name=='Rift / continuous channel',(j,obj.name)
actual={n:list(bpy.data.objects[n].matrix_world) for n in ['Lid_Hinge','Latch_Pivot']}
actual={n:[[float(x) for x in row] for row in m] for n,m in actual.items()}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in actual.items():
 assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out=dict(status='PASS',detached_ornament_negative_rejected=negative,ridge_gap_min=min(gaps),channel_visible_downward_rays=24,inherited_pivot_matrices_equal=True,relief_top=max(v.z for v in e+w))
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(out)
