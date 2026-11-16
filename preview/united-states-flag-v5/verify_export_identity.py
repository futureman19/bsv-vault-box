from pathlib import Path
import struct,json,hashlib,io
from PIL import Image
R=Path(__file__).resolve().parent
OLD=R.parent/'united-states-flag-v4'
def load(p):
 a=p.read_bytes();n=struct.unpack_from('<I',a,12)[0];return json.loads(a[20:20+n]),a[28+n:]
def view(g,b,i):
 v=g['bufferViews'][i];return b[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
a,ab=load(OLD/'united-states.glb');b,bb=load(R/'united-states.glb')
assert a['nodes']==b['nodes'];assert len(a['meshes'])==len(b['meshes'])
count=0;uvchanged=0
for am,bm in zip(a['meshes'],b['meshes']):
 assert am['name']==bm['name']
 for ap,bp in zip(am['primitives'],bm['primitives']):
  for key,ai in dict(ap['attributes'],indices=ap['indices']).items():
   bi=bp['indices'] if key=='indices' else bp['attributes'][key]
   av=a['accessors'][ai];bv=b['accessors'][bi]
   equal=view(a,ab,av['bufferView'])==view(b,bb,bv['bufferView'])
   if key.startswith('TEXCOORD'):uvchanged+=not equal
   else:assert equal,(am['name'],key);count+=1
images=[]
for m in b['materials']:
 tex=m.get('pbrMetallicRoughness',{}).get('baseColorTexture')
 if not tex:continue
 image=b['images'][b['textures'][tex['index']]['source']];data=view(b,bb,image['bufferView']);im=Image.open(io.BytesIO(data)).convert('RGB')
 fname='flag-lid.png' if 'lid' in m['name'] else 'flag-wall.png'
 expected=Image.open(R/'maps'/fname).convert('RGB');assert im.size==expected.size and im.tobytes()==expected.tobytes();images.append(fname)
out={'PASS':True,'exact_non_uv_accessor_views':count,'changed_uv_views':uvchanged,'all_nodes_exact_v4':True,'exported_basecolor_pixels_exact_authored_maps':images}
(R/'export-identity-check.json').write_text(json.dumps(out,indent=2));print(out)
