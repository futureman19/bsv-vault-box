"""Portable material/UV finalizer. All geometry/non-body buffer payloads byte-preserved."""
from glb_tools import *
j,b=load(R/'baseline/morocco.glb');chunks={i:bytearray(view(j,b,i)) for i in range(len(j['bufferViews']))}
for node in j['nodes']:
 if not node.get('name','').startswith('Rose stone'):continue
 for p in j['meshes'][node['mesh']]['primitives']:
  a=p['attributes'];xyz=accessor(j,b,a['POSITION'])*np.array(node.get('scale',[1,1,1]))+np.array(node.get('translation',[0,0,0]));v=uv(xyz[:,0],-xyz[:,2],xyz[:,1],'rear' in node['name']);v[:,1]=1-v[:,1]
  acc=j['accessors'][a['TEXCOORD_0']];idx=acc['bufferView'];bv=j['bufferViews'][idx]
  dest=np.ndarray(v.shape,dtype='<f4',buffer=chunks[idx],offset=acc.get('byteOffset',0),strides=(bv.get('byteStride',8),4));dest[:]=v
  if 'min' in acc:acc['min']=v.min(axis=0).tolist();acc['max']=v.max(axis=0).tolist()
for idx,name,mime in [(3,'sandstone-normal.png','image/png'),(4,'sandstone-color.jpg','image/jpeg'),(5,'sandstone-orm.jpg','image/jpeg')]:
 im=j['images'][idx];chunks[im['bufferView']]=bytearray((R/'maps'/name).read_bytes());im['name']=name;im['mimeType']=mime
m=j['materials'][7];m['name']='Sandstone / dusty mineral bedding and pores';m['normalTexture']['scale']=.8
out=bytearray()
for i,v in enumerate(j['bufferViews']):
 out+=b'\0'*((-len(out))%4);v['byteOffset']=len(out);v['byteLength']=len(chunks[i]);out+=chunks[i]
save(j,out,R/'morocco.glb');print('GLB_BYTES',(R/'morocco.glb').stat().st_size)
