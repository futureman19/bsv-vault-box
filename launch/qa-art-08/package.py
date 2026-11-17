import pathlib,hashlib,json,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['qa-inventory.json','qa-art-08-report.zip','package-result.json'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'qa-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
selected=[p for p in files if p.parent==R]+[R/'qa-inventory.json']
selected += sorted((R/'parent/boards').glob('*.jpg'))
zpath=R/'qa-art-08-report.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in selected:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
 for n in z.namelist():assert z.read(n)==(R/n).read_bytes()
 assert {'review.html','reviewed-ledger.json','audit-results.json','test-results.txt','qa-inventory.json'}<=set(z.namelist())
result={'path':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath.read_bytes()),'entries':len(selected),'full_evidence_inventory_entries':len(inv),'readback':'all members exact','exclusions':'Original parent PNGs, historical source archives and original parent delivery ZIPs excluded from small report ZIP; immutable parent ref recorded in ledger; all extracted parent evidence committed on QA branch.'}
(R/'package-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
