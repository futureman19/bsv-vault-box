"""Preserve all approved GLB records/binary bytes; append new moss only.
Blender modifier reevaluation can differ at float-bit level after source reopen.
Never replace the approved non-moss payload with that reevaluated export.
"""
from pathlib import Path
import json,struct,copy
R=Path(__file__).resolve().parent
def read(path):
 b=path.read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);return j,b[28+n:]
g,base=read(R/'approved-v6.glb');h,addition=read(R/'iceland.glb');binary=bytearray(base);viewmap={};accmap={};matmap={};meshmap={}
def view(i):
 if i not in viewmap:
  v=copy.deepcopy(h['bufferViews'][i]);s=v.get('byteOffset',0)
  while len(binary)%4:binary.append(0)
  v['byteOffset']=len(binary);v['buffer']=0;binary.extend(addition[s:s+v['byteLength']]);viewmap[i]=len(g['bufferViews']);g['bufferViews'].append(v)
 return viewmap[i]
def accessor(i):
 if i not in accmap:
  a=copy.deepcopy(h['accessors'][i]);assert 'sparse' not in a;a['bufferView']=view(a['bufferView']);accmap[i]=len(g['accessors']);g['accessors'].append(a)
 return accmap[i]
def material(i):
 if i not in matmap:
  m=copy.deepcopy(h['materials'][i]);assert m['name'].startswith('Moss v7 /');matmap[i]=len(g['materials']);g['materials'].append(m)
 return matmap[i]
newnames=[]
for n in h['nodes']:
 if not n.get('name','').startswith('Sheltered moss v7'):continue
 n=copy.deepcopy(n);idx=n['mesh']
 if idx not in meshmap:
  m=copy.deepcopy(h['meshes'][idx])
  for p in m['primitives']:
   p['attributes']={k:accessor(i) for k,i in p['attributes'].items()}
   if 'indices' in p:p['indices']=accessor(p['indices'])
   p['material']=material(p['material'])
  meshmap[idx]=len(g['meshes']);g['meshes'].append(m)
 n['mesh']=meshmap[idx];assert 'children' not in n;g['scenes'][g.get('scene',0)]['nodes'].append(len(g['nodes']));g['nodes'].append(n);newnames.append(n['name'])
assert len(newnames)==16
g['buffers'][0]['byteLength']=len(binary)
while len(binary)%4:binary.append(0)
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
out=struct.pack('<III',0x46546c67,2,28+len(j)+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary
(R/'iceland.glb').write_bytes(out)
print('APPENDED_MOSS_ONLY',len(newnames),'PRESERVED_BASE_BINARY_BYTES',len(base),'FINAL_GLB_BYTES',len(out))
