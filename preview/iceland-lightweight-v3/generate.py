"""Material-only portable refinement. Preserve original binary prefix and transforms."""
from pathlib import Path
from PIL import Image, ImageFilter
import random, math, struct, json, shutil
R=Path(__file__).resolve().parent
V=R/'original';V.mkdir(exist_ok=True)
for name in ['iceland.glb','iceland.blend','author.py']:
 if not (V/name).exists():shutil.copyfile(R.parent/'iceland-pilot'/name,V/name)
T=R/'textures';T.mkdir(exist_ok=True)
r=random.Random(732);s=256
h=Image.new('L',(s,s));h.putdata([r.randrange(90,166) for _ in range(s*s)]);h=h.filter(ImageFilter.GaussianBlur(.7));px=h.load()
base=Image.new('RGB',(s,s));rough=base.copy();normal=base.copy()
for y in range(s):
 for x in range(s):
  v=px[x,y];c=round(246+(v-128)*.22);base.putpixel((x,y),(c,c,c))
  rough.putpixel((x,y),(255,round(243+(v-128)*.15),255))
  dx=(px[(x+1)%s,y]-px[(x-1)%s,y])*.0015;dy=(px[x,(y+1)%s]-px[x,(y-1)%s])*.0015
  z=1/math.sqrt(1+dx*dx+dy*dy);normal.putpixel((x,y),(round(127.5*(1-dx*z)),round(127.5*(1+dy*z)),round(127.5*(1+z))))
base.save(T/'basalt-color.jpg',quality=88,subsampling=0);rough.save(T/'basalt-orm.jpg',quality=90,subsampling=0);normal.save(T/'basalt-normal.png',optimize=True)
b=(V/'iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);blob=bytearray(b[28+n:])
def append(data):
 while len(blob)%4:blob.append(0)
 idx=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(blob),'byteLength':len(data)});blob.extend(data);return idx
# Original exporter has no basalt UVs. Add planar face UVs only, not positions or normals.
for mesh in g['meshes']:
 for p in mesh['primitives']:
  if not g['materials'][p['material']]['name'].startswith('Basalt /'):continue
  attrs=p['attributes'];a=g['accessors'][attrs['POSITION']];nv=g['accessors'][attrs['NORMAL']]
  av=g['bufferViews'][a['bufferView']];vv=g['bufferViews'][nv['bufferView']];uv=[]
  for i in range(a['count']):
   x,y,z=struct.unpack_from('<3f',blob,av.get('byteOffset',0)+a.get('byteOffset',0)+i*av.get('byteStride',12));nx,ny,nz=struct.unpack_from('<3f',blob,vv.get('byteOffset',0)+nv.get('byteOffset',0)+i*vv.get('byteStride',12))
   u,v=(z,y) if abs(nx)>abs(nz) else (x,y)
   if abs(ny)>max(abs(nx),abs(nz)):u,v=x,z
   uv.extend([u*2,v*2])
  vi=append(struct.pack('<%sf'%len(uv),*uv));attrs['TEXCOORD_0']=len(g['accessors']);g['accessors'].append({'bufferView':vi,'componentType':5126,'count':a['count'],'type':'VEC2'})
g['images']=[];g['textures']=[];g['samplers']=[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}]
for name,mime in [('basalt-color.jpg','image/jpeg'),('basalt-orm.jpg','image/jpeg'),('basalt-normal.png','image/png')]:
 g['images'].append({'bufferView':append((T/name).read_bytes()),'mimeType':mime,'name':name});g['textures'].append({'source':len(g['images'])-1,'sampler':0})
for m in g['materials']:
 if m['name'].startswith('Basalt /'):
  m['pbrMetallicRoughness']['baseColorTexture']={'index':0};m['pbrMetallicRoughness']['metallicRoughnessTexture']={'index':1};m['normalTexture']={'index':2,'scale':.35}
while len(blob)%4:blob.append(0)
g['buffers'][0]['byteLength']=len(blob);j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
(R/'iceland.glb').write_bytes(struct.pack('<III',0x46546c67,2,28+len(j)+len(blob))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(blob),0x004e4942)+blob)
print('GLB bytes', (R/'iceland.glb').stat().st_size)
