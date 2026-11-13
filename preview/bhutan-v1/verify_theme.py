import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
reference={n:[[float(x) for x in row] for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'bhutan.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];ridge=bpy.data.objects['Mountain / asymmetric relief']
if '--negative-control' in sys.argv:ridge.parent=None
for n,m in reference.items():
 actual=bpy.data.objects[n].matrix_world
 assert max(abs(actual[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7,('pivot',n)
assert bpy.data.objects['Latch_Pivot'].parent==lid
features={}
for prefix,minimum in [('Earth / body',4),('Timber / upright',8),('Cornice /',8),('Painted border /',44),('Mountain /',1)]:
 objects=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(prefix)];features[prefix]=len(objects);assert len(objects)>=minimum,(prefix,len(objects))
 if prefix in ['Cornice /','Painted border /','Mountain /']:
  assert all(o.parent==lid for o in objects),('lid ancestry',prefix)
assert not any(o.name.startswith(('Cedar tree','Terrain / moss')) for o in bpy.data.objects)
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
coords=[ridge.matrix_world@v.co for v in ridge.data.vertices]
span=[max(v[i] for v in coords)-min(v[i] for v in coords) for i in range(3)]
assert abs(span[0]-2.2)<.01 and abs(span[1]-1)<.01 and span[2]<.60
assert all(o.parent in [None,lid,bpy.data.objects['Latch_Pivot']] for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio'))
for name,target in [('Paint / oxblood',(.178,.027,.020)),('Paint / subdued teal',(.041,.162,.145)),('Paint / golden ochre',(.552,.323,.067))]:
 c=bpy.data.materials[name].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value
 assert max(abs(c[i]-target[i]) for i in range(3))<1e-5
images=[i for i in bpy.data.images if i.packed_file];assert len(images)==4 and all(max(i.size)<=512 for i in images)
r={'status':'PASS','features':features,'ridge_span':span,'pivots_match_trimmed_mechanism':True,'moving_theme_parentage':True,'collision_harness_parent_coverage':True,'palette_linear_values_verified':True,'packed_maps':[i.name for i in images]}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',json.dumps(r))
