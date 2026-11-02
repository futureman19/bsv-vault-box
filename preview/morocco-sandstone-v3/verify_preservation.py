from glb_tools import *
import sys,hashlib
old,ob=load(R/'baseline/morocco.glb');new,nb=load(Path(sys.argv[1]) if len(sys.argv)>1 else R/'morocco.glb')
assert old['nodes']==new['nodes'] and old['meshes']==new['meshes'],'geometry graph changed'
assert old['materials'][:7]==new['materials'][:7],'non-body material changed'
bodyuv=set();errors=[]
for node in new['nodes']:
 if not node.get('name','').startswith('Rose stone'):continue
 for p in new['meshes'][node['mesh']]['primitives']:
  a=p['attributes'];bodyuv.add(a['TEXCOORD_0']);xyz=accessor(new,nb,a['POSITION'])*np.array(node.get('scale',[1,1,1]))+np.array(node.get('translation',[0,0,0]))
  expected=uv(xyz[:,0],-xyz[:,2],xyz[:,1],'rear' in node['name']);expected[:,1]=1-expected[:,1]
  errors.append(float(np.max(np.abs(expected-accessor(new,nb,a['TEXCOORD_0'])))))
for i in range(len(old['accessors'])):
 if i not in bodyuv:assert np.array_equal(accessor(old,ob,i),accessor(new,nb,i)),('accessor changed',i)
for i in range(3):
 assert view(old,ob,old['images'][i]['bufferView'])==view(new,nb,new['images'][i]['bufferView'])
assert max(errors)<2e-6,('corner-continuous object-coordinate UV mismatch',max(errors))
assert new['materials'][7]['normalTexture']['scale']>=.6,'inadequate portable relief'
assert new['materials'][7]!=old['materials'][7]
for i in range(3,6):assert view(old,ob,old['images'][i]['bufferView'])!=view(new,nb,new['images'][i]['bufferView'])
result={'exact_nodes_meshes':True,'exact_nonbody_materials_images':True,'exact_all_nonUV_accessor_values':True,'body_UV_max_error':max(errors),'body_material_changed':True,'mapping':'one continuous angular world-XY coordinate, physical Z height; rear seam periodic','corners':[uv(x,y,.84).tolist() for x,y in [(-1.86,-1.44),(1.86,-1.44),(-1.86,1.44),(1.86,1.44)]]}
(R/'preservation-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
