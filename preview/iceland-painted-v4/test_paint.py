"""Acceptance written before painter: spatial paint, payload and immutable geometry."""
from pathlib import Path
import json,struct,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent

def glb(p):
 b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+n]),b[28+n:]

def run():
 g,b=glb(R/'iceland.glb');old,ob=glb(R.parent/'iceland-lightweight-v3/original/iceland.glb')
 assert b[:len(ob)]==ob,'original geometry binary changed'
 assert g['nodes']==old['nodes'] and g['scenes']==old['scenes']
 for m,om in zip(g['meshes'],old['meshes']):
  for p,op in zip(m['primitives'],om['primitives']):
   assert p['indices']==op['indices']
   assert {k:v for k,v in p['attributes'].items() if k!='TEXCOORD_0'}=={k:v for k,v in op['attributes'].items() if k!='TEXCOORD_0'}
   if p['material']<=5:
    a=g['accessors'][p['attributes']['TEXCOORD_0']];bv=g['bufferViews'][a['bufferView']];uv=np.frombuffer(b,dtype='<f4',count=a['count']*2,offset=bv['byteOffset']);assert np.isfinite(uv).all() and uv.min()>=0 and uv.max()<=1
 assert g['materials'][8]==old['materials'][8],'approved lid changed'
 color=np.asarray(Image.open(R/'textures/paint-color.jpg')).astype(float)
 masks=np.asarray(Image.open(R/'textures/paint-masks.png'))
 moss=masks[:,:,1]>0;shelter=masks[:,:,0]>0
 assert moss.sum()>1000 and (moss & ~shelter).sum()==0
 assert moss.mean()<.09 and color[moss,1].mean()>color[moss,0].mean()*1.12
 assert color[:768].std()>18,'paint too uniform'
 assert (masks[:,:,2]>0).sum()>1000,'fissure/chip paint missing'
 assert (R/'iceland-painted-v4.html').stat().st_size<=5_000_000
 for name in ['viewer.js','viewer.bundle.js','motion.mjs']:
  assert (R/name).read_bytes()==(R.parent/'iceland-lightweight-v3'/name).read_bytes()
 for name,h in json.loads((R/'preserved-inputs.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==h
 result={'geometry_binary_prefix_unchanged':True,'nodes_pivots_unchanged':True,'runtime_and_motion_byte_identical':True,'uv_finite_in_atlas':True,'moss_pixels':int(moss.sum()),'moss_outside_shelter':0,'color_std':float(color[:768].std()),'html_bytes':(R/'iceland-painted-v4.html').stat().st_size,'glb_bytes':(R/'iceland.glb').stat().st_size,'source_inputs_hashes_preserved':True}
 (R/'paint-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':run()
