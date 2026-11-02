from pathlib import Path
import struct,json
R=Path(__file__).resolve().parent
b=(R/'morocco.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);names=[x.get('name','') for x in g['nodes']]
assert any(x.startswith('Atlas ridge') for x in names),'Missing real Atlas ridge'
assert sum(x.startswith('Ceramic tessera') for x in names)>=150,'Missing individual geometric tessellation'
assert not any(any(bad in x.lower() for bad in ['glacier','river','moss','tree','foliage','granite','finger']) for x in names),'Stale theme geometry'
assert any(x.startswith('Rose stone') for x in names)
assert len(g.get('images',[]))>=3
(R/'theme-check.json').write_text(json.dumps({'individual_tessera_nodes':sum(x.startswith('Ceramic tessera') for x in names),'no_stale_theme':True,'portable_images':len(g['images'])},indent=2));print('THEME PASS')
