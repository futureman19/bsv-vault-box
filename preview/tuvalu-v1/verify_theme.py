import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'tuvalu.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in base.items():assert max(abs(v-bpy.data.objects[n].matrix_world[i][j]) for i,row in enumerate(m) for j,v in enumerate(row))<1e-7
lid=bpy.data.objects['Lid_Hinge'];sand=bpy.data.objects['Island / coral sand footprint'];water=bpy.data.objects['Lagoon / contained turquoise inset']
def own(o):assert o.parent==lid,'Missing lid ownership'
for o in [sand,water]:own(o)
old=water.parent;water.parent=None
try:
 own(water);raise RuntimeError('Negative failed to reject')
except AssertionError:negative=True
water.parent=old
outer=[(sand.matrix_world@v.co) for v in sand.data.vertices[:72]]
def inside(x,y):
 c=False
 for a,b in zip(outer,outer[1:]+outer[:1]):
  if (a.y>y)!=(b.y>y) and x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x:c=not c
 return c
points=[water.matrix_world@v.co for v in water.data.vertices]
assert all(inside(p.x,p.y) for p in points)
assert not inside(10,10)
height=max((o.matrix_world@v.co).z for o in [sand,water] for v in o.data.vertices)-1.978
assert 0<height<=.32
assert all('Cedar tree' not in o.name for o in bpy.data.objects)
images={i.name:i for i in bpy.data.images if i.packed_file}
assert {'weave-color.png','weave-roughness.png','weave-normal.png'}<=set(images)
variation={n:max(i.pixels[::4])-min(i.pixels[::4]) for n,i in images.items()}
assert variation['weave-color.png']>.1 and variation['weave-roughness.png']>.01
r=dict(status='PASS',inherited_pivots_equal=True,lagoon_vertices_contained=len(points),relief_height=height,detached_lid_negative_rejected=negative,outside_point_negative_rejected=True,packed_map_variation=variation)
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r));print('THEME PASS')
