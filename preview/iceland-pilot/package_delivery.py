"""Allowlisted local-only packaging, hash readback and ZIP inventory verification."""
from pathlib import Path
import hashlib, json, zipfile, shutil
ROOT=Path(__file__).resolve().parent
OUT=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-pilot')
def sha(data):return hashlib.sha256(data).hexdigest()
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
asset=json.loads((ROOT/'browser-check.json').read_text())[0]['asset']
assert asset['bytes']==(ROOT/'iceland.glb').stat().st_size
proposal={'status':'PROPOSAL ONLY — NOT MINTED, SIGNED, UPLOADED OR ON-CHAIN','collectible':'Iceland / Basalt','role':'one inner collectible, not outer custody container','asset_version_id':'sha256:'+info(ROOT/'iceland.glb')['sha256'],'model':info(ROOT/'iceland.glb'),'poster':info(ROOT/'poster.png'),'source_blend':info(ROOT/'iceland.blend'),'reference_original':info(ROOT/'reference-original-basalt.png'),'storage_choice':'NOT YET IMPLEMENTED: off-chain IPFS model/poster with independent pinning and HTTPS archive mirrors; future issuance hash commitments only after admission/retrieval tests','current_storage':'Local files only; embedded local HTML; no CIDs or network storage','certificate':'None signed; any future certificate is a signed record, not another NFT','scarcity':'Proposed 201 one-of-one Boxes (195 countries, five oceans, Moon), identical edition scarcity; no issuance performed'}
(ROOT/'asset-identity-proposal.json').write_text(json.dumps(proposal,indent=2),encoding='utf8')
names='.gitattributes .gitignore README.md author.py build.py motion.mjs tests.mjs verify_source.py verify_browser.py package_delivery.py viewer.js viewer.bundle.js template.html package.json package-lock.json THREE-LICENSE.txt iceland.blend iceland.glb poster.png reference-original-basalt.png iceland-pilot.html desktop-closed.png desktop-open.png mobile-closed.png mobile-open.png mobile-fallback.png initial-open-clipped.png framing-debug.png source-check.json browser-check.json test-red.txt test-negative-zero-red.txt test-green.txt author-output.txt source-output.txt asset-identity-proposal.json'.split()
assert len(names)==len(set(names))
manifest={'schema':'boxsv-local-art-pilot/1','self_exclusion':'manifest and ZIP/delivery envelopes excluded to avoid circular hashes','model_metrics':asset,'files':{n:info(ROOT/n) for n in sorted(names)}}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
zip_path=ROOT/'iceland-pilot-source.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted(names+['manifest.json']):z.write(ROOT/n,n)
with zipfile.ZipFile(zip_path) as z:
 assert set(z.namelist())==set(names+['manifest.json'])
 assert z.testzip() is None
 for n,d in manifest['files'].items():assert sha(z.read(n))==d['sha256'] and len(z.read(n))==d['bytes']
 assert z.read('manifest.json')==(ROOT/'manifest.json').read_bytes()
OUT.mkdir(parents=True,exist_ok=True)
for n in names+['manifest.json',zip_path.name]:
 shutil.copyfile(ROOT/n,OUT/n);assert (OUT/n).read_bytes()==(ROOT/n).read_bytes()
report={'zip':info(zip_path),'manifest':info(ROOT/'manifest.json'),'zip_entries':len(names)+1,'payload_files':len(names),'zip_inventory_matches_manifest':True,'all_archive_hashes_verified':True,'output_copies_readback_verified':True,'destination':str(OUT),'excluded':['node_modules','.blend1','secrets','__pycache__']}
(ROOT/'delivery-check.json').write_text(json.dumps(report,indent=2));shutil.copyfile(ROOT/'delivery-check.json',OUT/'delivery-check.json');assert (OUT/'delivery-check.json').read_bytes()==(ROOT/'delivery-check.json').read_bytes()
print(json.dumps({'delivery':report,'asset':proposal['model'],'metrics':asset},indent=2))
