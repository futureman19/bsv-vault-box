from pathlib import Path
import json,struct,copy
R=Path(__file__).resolve().parent
raw=(R/'cameroon.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n])
def validate(d):
 names=[x.get('name','') for x in d['nodes']]
 for prefix in ['Basalt','Fako','Rainforest','Side ring','Medallion','Lid_Hinge','Latch_Pivot']:
  assert any(x.startswith(prefix) for x in names),prefix
 assert not any(any(b in x.lower() for b in ['cedar','glacier','japan','iceland']) for x in names)
 assert len(d.get('images',[]))>=3
 for image in d['images']:assert 'bufferView' in image and 'uri' not in image
validate(d)
negative=copy.deepcopy(d)
for node in negative['nodes']:
 if node.get('name','').startswith('Fako'):node['name']='missing relief'
try:validate(negative)
except AssertionError as e:negative_reason=str(e)
else:raise AssertionError('Negative control wrongly passed')
assert (R/'cameroon-v1.html').stat().st_size<5_000_000
out={'status':'PASS','required_features':True,'portable_images':len(d['images']),'no_old_theme_nodes':True,'negative_control':{'removed_feature':'Fako','rejected':True,'reason':negative_reason},'negative_control_note':'Post-implementation mutation control, not test-first TDD'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS; missing Fako negative control rejected')
