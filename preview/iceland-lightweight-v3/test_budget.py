"""Literal payload and portable materials contract; can test prior versions."""
import json, struct, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT
html=next(path.glob('iceland-*.html'))
b=(path/'iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n])
checks={'html_budget':html.stat().st_size<=5_000_000,'glb_budget':len(b)<=1_200_000}
lid=next(m for m in g['materials'] if m['name']=='Polished blue-black lid')
checks['clear_original_glossy_lid']=lid['pbrMetallicRoughness'].get('roughnessFactor',1)<=.30 and 'baseColorTexture' not in lid['pbrMetallicRoughness'] and 'normalTexture' not in lid
stones=[m for m in g['materials'] if m['name'].startswith('Basalt /')]
checks['portable_basalt_maps']=len(stones)==5 and all('baseColorTexture' in m['pbrMetallicRoughness'] and 'metallicRoughnessTexture' in m['pbrMetallicRoughness'] and 'normalTexture' in m for m in stones)
checks['embedded_images']=bool(g.get('images')) and all('bufferView' in i and 'uri' not in i for i in g.get('images',[]))
print(json.dumps({'path':str(path),'html_bytes':html.stat().st_size,'glb_bytes':len(b),'checks':checks},indent=2));assert all(checks.values()),checks
