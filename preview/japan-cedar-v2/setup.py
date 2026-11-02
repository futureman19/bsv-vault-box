from pathlib import Path
import shutil,json,hashlib,struct
R=Path(__file__).resolve().parent;B=R.parent/'japan-cedar-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
frozen={str(p):sha(p) for folder in [B,R.parent/'iceland-pilot'] for p in folder.rglob('*') if p.is_file() and 'node_modules' not in p.parts and '.git' not in p.parts}
ref=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-concepts/japan.png');frozen[str(ref)]=sha(ref)
(R/'frozen-inputs.json').write_text(json.dumps(frozen,indent=2))
for name in ['viewer.js','motion.mjs','template.html','build.py','verify_browser.py','verify_extended.py','verify_source.py','verify_parity.py','verify_reexport.py','render_review.py','package.json','THREE-LICENSE.txt','mechanism.blend','maps.py','.gitattributes']:
 p=B/name;d=R/name
 if p.suffix in ['.py','.html']:d.write_text(p.read_text(encoding='utf8').replace('japan-cedar-v1','japan-cedar-v2'),encoding='utf8')
 else:shutil.copy2(p,d)
shutil.copy2(B/'japan.blend',R/'baseline.blend')
for folder in ['maps','references']:shutil.copytree(B/folder,R/folder,dirs_exist_ok=True)
b=(B/'japan.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);parts=[]
for m in g['meshes']:
 total=0
 for p in m['primitives']:
  for a in list(p['attributes'].values())+[p['indices']]:total+=g['bufferViews'][g['accessors'][a]['bufferView']]['byteLength']
 parts.append({'name':m['name'],'accessor_bytes':total})
report={'HTML_bytes':(B/'japan-cedar-v1.html').stat().st_size,'GLB_bytes':len(b),'mesh_payloads_largest':sorted(parts,key=lambda x:-x['accessor_bytes'])[:12],'optimization':'Replace four-triangle five-vertex needle diamonds with folded two-triangle four-vertex lancelets; denser overlapping sprays with larger projected area. Keep maps, viewer, fallback quality unchanged.'}
(R/'baseline-budget.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
