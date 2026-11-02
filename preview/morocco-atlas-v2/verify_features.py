import bpy,json,os
from pathlib import Path
R=Path(__file__).resolve().parent
source=Path(os.environ.get('MOROCCO_SOURCE',str(R/'morocco.blend')))
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);bpy.context.view_layer.update()
checks={};details={}
meshes=[o for o in bpy.data.objects if o.type=='MESH']
tiles=[o for o in meshes if o.name.startswith('Ceramic tessera')]
counts=[]
for o in tiles:
 parent=list(range(len(o.data.vertices)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for e in o.data.edges:
  a,b=e.vertices;parent[root(a)]=root(b)
 counts.append(len({root(i) for i in range(len(parent))}))
checks['dense_individual_prisms']=sum(counts)==1080;details['ceramic_connected_components']=counts
checks['all_tiles_lid_parent']=all(o.parent.name=='Lid_Hinge' for o in tiles)
ring=bpy.data.objects['Side ring / hanging brass'];checks['ring_low_front_left']=ring.location.x<-1 and ring.location.y<-1.4 and ring.location.z<.4
hasp=bpy.data.objects['Latch / lifting hasp'];z=[(hasp.matrix_world@v.co).z for v in hasp.data.vertices];details['hasp_height']=max(z)-min(z);checks['compact_hasp']=details['hasp_height']<.34
ridge=bpy.data.objects['Atlas ridge / rear centre eroded massif'];vs=[ridge.matrix_world@v.co for v in ridge.data.vertices];details['ridge_height']=max(v.z for v in vs)-min(v.z for v in vs);checks['enlarged_eroded_ridge']=details['ridge_height']>.65 and ridge.parent.name=='Lid_Hinge'
checks['packed_normal_and_roughness']=all(bpy.data.images.get(n) and bpy.data.images[n].packed_file for n in ['stone-normal.png','stone-roughness.png'])
result=dict(source=str(source),checks=checks,details=details,passed=all(checks.values()),method='Post-implementation regression gate; v1 negative control, not test-first TDD')
name='feature-negative-control.json' if source.parent!=R else 'feature-check.json';(R/name).write_text(json.dumps(result,indent=2));print(json.dumps(result));assert result['passed']
