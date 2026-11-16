from pathlib import Path
import json,struct,io
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
raw=(R/'united-states.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);binary=raw[28+n:]
def image(material):
 t=g['textures'][material['pbrMetallicRoughness']['baseColorTexture']['index']]
 v=g['bufferViews'][g['images'][t['source']]['bufferView']]
 return np.array(Image.open(io.BytesIO(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']])).convert('RGB'))
body=[];lid=[]
for node in g['nodes']:
 if 'mesh' not in node:continue
 name=node['name']
 for primitive in g['meshes'][node['mesh']]['primitives']:
  material=g['materials'][primitive['material']]
  if name.startswith(('Flag body','Flag /','Navy seam')):
   assert material['name']=='Flag / lacquer',(name,material['name'])
   a=image(material)
   assert np.all(a==a[:,0:1,:]),'No stars or other horizontal motifs permitted'
   assert set(map(tuple,a[:,0,:]))=={(183,23,43),(239,235,218)}
   body.append(name)
  if material['name']=='Flag / navy star canton lid':
   assert name=='Lid / polished slab',name
   lid.append(name)
assert len(body)==17 and len(lid)==1,(body,lid)
assert (R/'maps/flag-lid.png').read_bytes()==(R.parent/'united-states-flag-v3/maps/flag-lid.png').read_bytes()
out=dict(PASS=True,body_and_feet_and_exterior_seams_stripes_only=body,body_atlas_every_pixel_red_or_white=True,body_atlas_every_row_constant_no_stars=True,sole_star_material_owner=lid,lid_map_exact_v3=True)
(R/'body-material-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
