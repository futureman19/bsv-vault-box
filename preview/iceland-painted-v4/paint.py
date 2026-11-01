"""Synthesized bitmap-brush atlas. No image projection, displacement or invented scans.
36 unique column tiles; seam masks are at each column's lateral joins. Shared brass tile.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
import random,math,json,struct
R=Path(__file__).resolve().parent;T=R/'textures';T.mkdir(exist_ok=True)
s=1024;tile=128;r=random.Random(405)
color=Image.new('RGB',(s,s),(40,45,49));orm=Image.new('RGB',(s,s),(255,210,255));height=Image.new('L',(s,s),128);masks=Image.new('RGB',(s,s))
b=(R/'original/iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);blob=bytearray(b[28+n:])
stone=[m for m in g['meshes'] if m['name'].startswith('Basalt column')]
layout={}
for idx,m in enumerate(stone):
 x0=idx%8*tile;y0=idx//8*tile
 base=r.randrange(34,92);a=np.zeros((tile,tile,3),dtype=np.uint8);hh=np.zeros((tile,tile),dtype=np.uint8)+128;mm=np.zeros_like(a)
 # UV U corresponds to the lateral column span; damp deposit only near side joins.
 for y in range(tile):
  for x in range(tile):
   u=(x-4)/120;v=(y-4)/120;edge=min(u,1-u)
   grain=r.gauss(0,1.8);strata=4*math.sin(v*31+idx)+3*math.sin(u*13+v*24)
   recess=max(0,1-edge/.18)
   val=base+grain+strata-22*recess
   a[y,x]=np.clip([val*.92,val,val*1.07],0,255)
   hh[y,x]=int(max(0,min(255,128+grain*1.3-10*recess)))
   sheltered=edge<.17 and .12<v<.88
   if sheltered:mm[y,x,0]=255
   patch=(math.sin(v*23+idx*2)+math.sin(v*47+idx)+math.sin(u*43+v*15))
   if sheltered and (idx%3==0 or idx%7==0) and patch>.85 and r.random()<.80:
    a[y,x]=[r.randrange(40,56),r.randrange(58,73),r.randrange(30,41)];mm[y,x,1]=255;hh[y,x]=r.randrange(130,139)
    if r.random()<.09:a[y,x]=[112,116,91]
 c=Image.fromarray(a);h=Image.fromarray(hh);mask=Image.fromarray(mm);dc=ImageDraw.Draw(c);dh=ImageDraw.Draw(h);dm=ImageDraw.Draw(mask)
 # Deliberately broken, slanting mineral seams, not repeated cloudy noise.
 for k in range(r.randrange(2,5)):
  x=r.randrange(12,110);y=r.randrange(18,108);pts=[(x,y)]
  for j in range(r.randrange(2,5)):
   x=max(6,min(121,x+r.randrange(-15,18)));y=max(6,min(121,y+r.randrange(1,4)));pts.append((x,y))
  dc.line(pts,fill=(25,29,32),width=2);dh.line(pts,fill=105,width=2);dm.line(pts,fill=(0,0,255),width=2)
  dc.line([(px+2,py-1) for px,py in pts],fill=(base+14,base+17,base+19),width=1)
 for k in range(22):
  x=r.randrange(7,121);y=r.randrange(7,121)
  if r.random()<.5:dc.line([(x,y),(x+2,y-1)],fill=(base+24,base+26,base+24),width=1)
 # UV islands are inset four pixels; surrounding painted pixels form a mip gutter.
 color.paste(c,(x0,y0));height.paste(h,(x0,y0));masks.paste(mask,(x0,y0))
 layout[m['name']]={'tile':idx,'kind':'basalt','shelter':'lateral u<0.17 or u>0.83, middle height only'}
# Brass uses a localized edge wear and narrow tarnish border, never stone noise.
idx=40;x0=0;y0=5*tile
for y in range(tile):
 for x in range(tile):
  u=(x-4)/120;v=(y-4)/120;e=min(u,1-u,v,1-v);noise=r.gauss(0,1.8)
  patina=math.exp(-((e-.075)/.035)**2)*.23;wear=max(0,1-e/.035)*.10
  color.putpixel((x0+x,y0+y),tuple(int(max(0,min(255,k*(1-patina+wear)+noise))) for k in (168,134,82)))
  orm.putpixel((x0+x,y0+y),(255,int(82+patina*160-wear*120),220))
# Normal map uses painted chips, not lighting. Keep modest tangent relief.
ha=np.asarray(height).astype(float);dy,dx=np.gradient(ha);nn=np.dstack((-dx*.016,dy*.016,np.ones_like(dx)));nn/=np.linalg.norm(nn,axis=2)[:,:,None]
normal=Image.fromarray(np.uint8(np.clip((nn*.5+.5)*255,0,255)))
color.save(T/'paint-color.jpg',quality=91,subsampling=0,optimize=True);orm.save(T/'paint-orm.jpg',quality=92,subsampling=0,optimize=True);normal.save(T/'paint-normal.png',optimize=True);masks.save(T/'paint-masks.png',optimize=True)
preview=Image.new('RGB',(1024,560),(20,25,30));preview.paste(color.resize((512,512)),(0,32));preview.paste(masks.resize((512,512)),(512,32));d=ImageDraw.Draw(preview);d.text((10,10),'COLOR: unique stone columns + brass (row 6)',fill='white');d.text((522,10),'MASKS: red shelter / green growth / blue fractures',fill='white');preview.save(R/'texture-atlas-preview.jpg',quality=92)
def append(data):
 while len(blob)%4:blob.append(0)
 idx=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(blob),'byteLength':len(data)});blob.extend(data);return idx
def arr(ai):
 a=g['accessors'][ai];bv=g['bufferViews'][a['bufferView']];return np.array([struct.unpack_from('<3f',blob,bv.get('byteOffset',0)+a.get('byteOffset',0)+i*bv.get('byteStride',12)) for i in range(a['count'])])
for m in g['meshes']:
 selected=[p for p in m['primitives'] if p['material']<=5]
 if not selected:continue
 coords=np.concatenate([arr(p['attributes']['POSITION']) for p in selected]);lo=coords.min(0);hi=coords.max(0);span=np.maximum(hi-lo,1e-6)
 idx=layout[m['name']]['tile'] if m['name'] in layout else 40
 for p in selected:
  pos=arr(p['attributes']['POSITION']);nor=arr(p['attributes']['NORMAL']);uv=[]
  for co,no in zip(pos,nor):
   q=(co-lo)/span
   if m['name'] in layout:
    u=q[2] if ' / end ' in m['name'] else q[0];v=q[1]
   else:
    axis=int(np.argmax(abs(no)));u,v=(q[2],q[1]) if axis==0 else ((q[0],q[2]) if axis==1 else (q[0],q[1]))
   uv.extend([(idx%8*128+4+u*120)/1024,(idx//8*128+4+(1-v)*120)/1024])
  vi=append(struct.pack('<%sf'%len(uv),*uv));p['attributes']['TEXCOORD_0']=len(g['accessors']);g['accessors'].append({'bufferView':vi,'componentType':5126,'count':len(pos),'type':'VEC2'})
g['images']=[];g['textures']=[];g['samplers']=[{'magFilter':9729,'minFilter':9987,'wrapS':33071,'wrapT':33071}]
for name,mime in [('paint-color.jpg','image/jpeg'),('paint-orm.jpg','image/jpeg'),('paint-normal.png','image/png')]:
 g['images'].append({'bufferView':append((T/name).read_bytes()),'mimeType':mime,'name':name});g['textures'].append({'source':len(g['images'])-1,'sampler':0})
for i,m in enumerate(g['materials'][:6]):
 p=m['pbrMetallicRoughness'];p['baseColorFactor']=[1,1,1,1];p['baseColorTexture']={'index':0};p['metallicRoughnessTexture']={'index':1};p['roughnessFactor']=1;p['metallicFactor']=.04 if i<5 else .9
 if i<5:m['normalTexture']={'index':2,'scale':.35}
while len(blob)%4:blob.append(0)
g['buffers'][0]['byteLength']=len(blob);j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
(R/'iceland.glb').write_bytes(struct.pack('<III',0x46546c67,2,28+len(j)+len(blob))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(blob),0x004e4942)+blob)
(R/'atlas-layout.json').write_text(json.dumps(layout,indent=2));print('painted GLB', (R/'iceland.glb').stat().st_size)
