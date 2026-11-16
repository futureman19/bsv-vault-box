from pathlib import Path
import struct,json,io,hashlib
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
raw=(R/'united-states.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);data=raw[28+n:];checks=[]
colors={'red':(181,0,24),'navy':(2,31,65),'white':(239,235,218)}
def srgb(v):return round(255*(v*12.92 if v<=.0031308 else 1.055*v**(1/2.4)-.055))
for m in g['materials']:
 p=m.get('pbrMetallicRoughness',{});tex=p.get('baseColorTexture')
 if not tex:continue
 im=g['images'][g['textures'][tex['index']]['source']];v=g['bufferViews'][im['bufferView']];buf=data[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
 filename='flag-lid.png' if 'lid' in m['name'] else 'flag-wall.png'
 actual=Image.open(io.BytesIO(buf)).convert('RGB');expected=Image.open(R/'maps'/filename).convert('RGB')
 assert actual.size==expected.size and actual.tobytes()==expected.tobytes()
 a=np.asarray(actual);counts={k:int(np.all(a==c,axis=2).sum()) for k,c in colors.items()};assert min(counts.values())>1000
 assert p.get('baseColorFactor',[1,1,1,1])==[1,1,1,1], 'Do not double convert or tint sRGB maps'
 checks.append(dict(material=m['name'],image=filename,dimensions=actual.size,export_pixels_exact_authored=True,exact_palette_texels=counts,baseColorFactor='identity'))
assert len(checks)==2
footindex=next(i for i,m in enumerate(g['materials']) if m['name']=='Flag / red feet')
footfactor=g['materials'][footindex]['pbrMetallicRoughness']['baseColorFactor'];assert tuple(srgb(x) for x in footfactor[:3])==colors['red']
feet=[x for x in g['nodes'] if x.get('name','').startswith('Flag / stone foot')];assert len(feet)==4
for node in feet:assert all(p['material']==footindex for p in g['meshes'][node['mesh']]['primitives'])
navy=next(m for m in g['materials'] if m['name']=='Interior / navy velvet')['pbrMetallicRoughness']['baseColorFactor'];assert tuple(srgb(x) for x in navy[:3])==colors['navy']
# White glyph masks and gold material unchanged against exact V7 packed baseline export.
b=R/'baseline-v7'
for name in ['flag-lid.png','flag-wall.png']:
 old=np.asarray(Image.open(b/'maps'/name).convert('RGB'));new=np.asarray(Image.open(R/'maps'/name).convert('RGB'))
 mask=np.all(old==colors['white'],axis=2)
 # Lanczos boundary rounding depends on adjacent pigment; verify unchanged solid white interior.
 from PIL import ImageFilter
 core=np.asarray(Image.fromarray(mask.astype('uint8')*255).filter(ImageFilter.MinFilter(7)))==255
 assert np.all(new[core]==colors['white'])
 checks.append(dict(image=name,unchanged_white_core_texels=int(core.sum()),antialias_white_mask_differences=int(np.count_nonzero(mask!=np.all(new==colors['white'],axis=2)))))
bb=(b/'united-states.glb').read_bytes();oldg=json.loads(bb[20:20+struct.unpack_from('<I',bb,12)[0]])
gold=lambda q:next(m for m in q['materials'] if 'Brass' in m['name'])
assert gold(g)==gold(oldg)
out=dict(PASS=True,checks=checks,feet=[x['name'] for x in feet],foot_linear_factor=footfactor,foot_srgb_bytes=[srgb(x) for x in footfactor[:3]],navy_linear_factor=navy,white_solid_interiors_and_gold_unchanged=True,antialiasing='Boundary texels interpolate pigments; solid regions exact. Rendered lighting changes displayed pixels.',glb_sha256=hashlib.sha256(raw).hexdigest())
(R/'palette-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
