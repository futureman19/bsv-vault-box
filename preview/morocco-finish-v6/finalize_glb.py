"""Graft only finish UV/material primitives, retaining approved scene and all geometry."""
from pathlib import Path
import copy,json
from glb_tools import load,save,view
R=Path(__file__).resolve().parent
j,b=load(R/'baseline/morocco.glb');t,tb=load(R/'target-export.glb');b=bytearray(b)
cache={}
def appendview(i):
 if i not in cache:
  b.extend(b'\0'*((-len(b))%4));v=copy.deepcopy(t['bufferViews'][i]);v.update(buffer=0,byteOffset=len(b));b.extend(view(t,tb,i));cache[i]=len(j['bufferViews']);j['bufferViews'].append(v)
 return cache[i]
ac={}
def acc(i):
 if i not in ac:
  a=copy.deepcopy(t['accessors'][i]);a['bufferView']=appendview(a['bufferView']);ac[i]=len(j['accessors']);j['accessors'].append(a)
 return ac[i]
def tex(i):
 x=copy.deepcopy(t['textures'][i]);im=copy.deepcopy(t['images'][x['source']]);im['bufferView']=appendview(im['bufferView']);x['source']=len(j['images']);j['images'].append(im)
 if 'sampler' in x:
  sam=t['samplers'][x['sampler']]
  if sam not in j['samplers']:j['samplers'].append(sam)
  x['sampler']=j['samplers'].index(sam)
 j['textures'].append(x);return len(j['textures'])-1
mc={}
for i,m in enumerate(t['materials']):
 old=next((k for k,x in enumerate(j['materials']) if x['name']==m['name']),None)
 if old is not None:mc[i]=old;continue
 m=copy.deepcopy(m)
 for key,value in m['pbrMetallicRoughness'].items():
  if isinstance(value,dict) and 'index' in value:value['index']=tex(value['index'])
 mc[i]=len(j['materials']);j['materials'].append(m)
for n in t['nodes']:
 if 'mesh' not in n:continue
 old=next(x for x in j['nodes'] if x['name']==n['name']);mesh=copy.deepcopy(t['meshes'][n['mesh']])
 for p in mesh['primitives']:
  p['attributes']={k:acc(v) for k,v in p['attributes'].items()};p['indices']=acc(p['indices']);p['material']=mc[p['material']]
 j['meshes'][old['mesh']]=mesh
j['materials'][7]['pbrMetallicRoughness']['baseColorFactor']=[.90,.90,.90,1]
# Drop orphaned target accessors/views so new UV streams replace, not duplicate, payload.
used=sorted({a for m in j['meshes'] for p in m['primitives'] for a in [p['indices'],*p['attributes'].values()]});am={a:i for i,a in enumerate(used)}
for m in j['meshes']:
 for p in m['primitives']:p['indices']=am[p['indices']];p['attributes']={k:am[a] for k,a in p['attributes'].items()}
j['accessors']=[j['accessors'][i] for i in used]
usedv=sorted({a['bufferView'] for a in j['accessors']}|{im['bufferView'] for im in j['images']});vm={v:i for i,v in enumerate(usedv)};out=bytearray();views=[]
for i in usedv:
 out.extend(b'\0'*((-len(out))%4));v=copy.deepcopy(j['bufferViews'][i]);payload=view(j,b,i);v['byteOffset']=len(out);out.extend(payload);views.append(v)
for a in j['accessors']:a['bufferView']=vm[a['bufferView']]
for im in j['images']:im['bufferView']=vm[im['bufferView']]
j['bufferViews']=views;save(j,out,R/'morocco.glb');print('GLB_BYTES',(R/'morocco.glb').stat().st_size)
