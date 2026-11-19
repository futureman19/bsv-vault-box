"""Bounded pass one: close measured rim joints, leave landmarks/mechanics intact."""
import bpy,json,sys
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];slug=sys.argv[sys.argv.index('--')+1];root=R/'preview'/f'{slug}-repair-v2'
bpy.ops.wm.open_mainfile(filepath=str(root/'historical-v1'/f'{slug}.blend'),use_scripts=False);bpy.context.view_layer.update()
def bounds(o):
 v=[o.matrix_world@v.co for v in o.data.vertices];return [[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')];before={o.name:bounds(o) for o in meshes};changes=[];pairs=[];negative=[]
side_prefix={'lithuania':'Seam / end','malta':'Seam / side','mozambique':'Tidal seam / side','tonga':'Seam / side','venezuela':'Weathered seam / side'}.get(slug,'Mineral seam / side')
sides=[bpy.data.objects[side_prefix+s] for s in ['', '.001']]
if slug!='tonga':
 for o in sides:
  corners=[c for c in meshes if '/ rim' in c.name and c.location.x*o.location.x>0 and 'Medallion' not in c.name]
  assert len(corners)==2
  for c in corners:
   a=before[o.name];b=before[c.name];gap=max(b[0][1]-a[1][1],a[0][1]-b[1][1]);assert .024<gap<.026;assert not tree(o).overlap(tree(c));negative.append({'pair':[o.name,c.name],'axis_gap':gap});pairs.append([o.name,c.name])
  for v in o.data.vertices:v.co.y*=2.13/2.05;v.co.z-=.004
  changes.append({'name':o.name,'axes':['Y','Z'],'reason':'Close demonstrated 0.025-unit gaps; lower top 0.004 to avoid coincident corner top faces.'})
else:
 longs=[bpy.data.objects['Seam / long'+s] for s in ['', '.001']]
 for a in longs:
  for b in sides:
   assert not tree(a).overlap(tree(b));negative.append({'pair':[a.name,b.name],'axis_gap':max(max(before[b.name][0][i]-before[a.name][1][i],before[a.name][0][i]-before[b.name][1][i],0) for i in range(3))});pairs.append([a.name,b.name])
 for o in longs+sides:
  for v in o.data.vertices:
   if o in longs:v.co.x*=3.40/3.28
   else:v.co.y*=2.30/2.05;v.co.z-=.004
  changes.append({'name':o.name,'axes':['X'] if o in longs else ['Y','Z'],'reason':'Close disconnected corner joins with distinct top planes.'})
bpy.context.view_layer.update()
for a,b in pairs:assert tree(bpy.data.objects[a]).overlap(tree(bpy.data.objects[b])),(a,b)
after={o.name:bounds(o) for o in meshes};changed={c['name'] for c in changes};assert all(before[n]==after[n] for n in before if n not in changed)
report={'correction_passes':1,'changed_objects':changes,'baseline_disconnected_pairs':negative,'repaired_surface_intersections':pairs,'before':{n:before[n] for n in changed},'after':{n:after[n] for n in changed},'untargeted_bounds_exact':True,'limitations':'Surface intersections, not welded engineering certification. All original artistic holds remain separate.'}
(root/'repair-check.json').write_text(json.dumps(report,indent=2))
s=bpy.context.scene;s.render.threads_mode='FIXED';s.render.threads=4;s.cycles.use_denoising=False;s.render.use_compositing=False
bpy.ops.wm.save_as_mainfile(filepath=str(root/f'{slug}.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Lid_Hinge'];bpy.ops.export_scene.gltf(filepath=str(root/f'{slug}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(root/'poster.png');bpy.ops.render.render(write_still=True)
print(json.dumps(report))
