from pathlib import Path
import struct,json,io,hashlib
from PIL import Image
R=Path(__file__).resolve().parent
raw=(R/'united-states.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);data=raw[28+n:];checks=[]
for m in g['materials']:
 tex=m.get('pbrMetallicRoughness',{}).get('baseColorTexture')
 if not tex:continue
 im=g['images'][g['textures'][tex['index']]['source']];v=g['bufferViews'][im['bufferView']];buf=data[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
 filename='flag-lid.png' if 'lid' in m['name'] else 'flag-wall.png'
 actual=Image.open(io.BytesIO(buf)).convert('RGB');expected=Image.open(R/'maps'/filename).convert('RGB')
 assert actual.size==expected.size and actual.tobytes()==expected.tobytes()
 checks.append(dict(material=m['name'],image=filename,dimensions=actual.size,export_pixels_exact_authored=True))
assert len(checks)==2
out=dict(PASS=True,checks=checks,glb_sha256=hashlib.sha256(raw).hexdigest())
(R/'export-paint-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
