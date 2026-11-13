"""Post-implementation negative controls, not a claim of test-first TDD."""
from pathlib import Path
import json,struct,subprocess,sys,hashlib
R=Path(__file__).resolve().parent
G=R/'laos.glb';H=R/'laos-v1.html';g=G.read_bytes();h=H.read_bytes();out=[]
def run(label):
 p=subprocess.run([sys.executable,str(R/'test_theme.py')],capture_output=True,text=True)
 assert p.returncode!=0,('negative control falsely passed',label)
 out.append({'case':label,'exit_code':p.returncode,'stderr':p.stderr})
try:
 n=struct.unpack_from('<I',g,12)[0];d=json.loads(g[20:20+n])
 node=next(x for x in d['nodes'] if x.get('name','').startswith('Karst / peak'))
 node['name']='Removed feature'
 j=json.dumps(d,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
 rest=g[20+n:];bad=struct.pack('<4sII',b'glTF',2,20+len(j)+len(rest))+struct.pack('<II',len(j),0x4e4f534a)+j+rest
 G.write_bytes(bad);run('one required karst peak removed');G.write_bytes(g)
 H.write_bytes(h+b' '*(5_000_000-len(h)));run('HTML exactly 5000000 bytes rejected')
finally:G.write_bytes(g);H.write_bytes(h)
assert G.read_bytes()==g and H.read_bytes()==h
p=subprocess.run([sys.executable,str(R/'test_theme.py')],capture_output=True,text=True);assert p.returncode==0,p.stderr
report={'status':'PASS','controls':out,'restored_final_theme_exit_code':p.returncode,'restored_glb_sha256':hashlib.sha256(g).hexdigest(),'restored_html_sha256':hashlib.sha256(h).hexdigest(),'label':'deliberate post-implementation negatives; not accidental failures or TDD'}
(R/'negative-check.json').write_text(json.dumps(report,indent=2));print('NEGATIVE CONTROLS PASS',json.dumps(report))
