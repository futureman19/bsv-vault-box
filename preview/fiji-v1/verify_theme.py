import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'fiji.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
def bounds(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box]
 return [[min(p[i] for p in v),max(p[i] for p in v)] for i in range(3)]
def contract():
 for n in ['Reef / sand perimeter','Lagoon / turquoise inset']+['Island / green '+str(i) for i in range(3)]:
  o=bpy.data.objects.get(n);assert o is not None,('Missing',n);assert o.parent==lid,('Detached',n)
  bb=bounds(o);assert bb[0][0]>-1.6 and bb[0][1]<1.6 and bb[1][0]>-.9 and bb[1][1]<.9 and bb[2][1]<2.43,(n,bb)
 assert not any('Cedar' in o.name or 'moss' in o.name.lower() for o in bpy.data.objects)
 assert all(abs(a-b)<1e-5 for a,b in zip(bpy.data.objects['Lid / polished slab'].dimensions,(3.72,2.38,.30)))
 # Test polygon containment, not just overlapping bounding boxes.
 reef=bpy.data.objects['Reef / sand perimeter'];lagoon=bpy.data.objects['Lagoon / turquoise inset']
 poly=[reef.matrix_world@v.co for v in list(reef.data.vertices)[:64]]
 def inside(p):
  c=False
  for a,b in zip(poly,poly[1:]+poly[:1]):
   if (a.y>p.y)!=(b.y>p.y) and p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x:c=not c
  return c
 assert all(inside(lagoon.matrix_world@v.co) for v in lagoon.data.vertices)
contract()
o=bpy.data.objects['Island / green 0'];saved=o.parent;o.parent=None
try:
 contract()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached ornament negative control did not fail')
o.parent=saved;bpy.context.view_layer.update();contract()
# Check original pivot matrices independently loaded from included baseline.
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
features={n:bounds(bpy.data.objects[n]) for n in ['Reef / sand perimeter','Lagoon / turquoise inset']+['Island / green '+str(i) for i in range(3)]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(pivots[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in pivots for i in range(4) for j in range(4));assert err<1e-7
result=dict(status='PASS',features=features,lagoon_boundary_contained=True,negative_control=negative,pivot_max_error=err,negative_control_kind='post-implementation mutation, not test-first history')
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
