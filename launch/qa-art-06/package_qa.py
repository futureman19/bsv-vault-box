import pathlib,json,hashlib,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.zip' and p.name not in ['qa-inventory.json','delivery.json'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'qa-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
selected=[p for p in files if 'parent' not in p.relative_to(R).parts and 'smoke' not in p.relative_to(R).parts and 'sources' not in p.relative_to(R).parts and 'motion' not in p.relative_to(R).parts]
selected.append(R/'qa-inventory.json')
zpath=R/'qa-art-06-report.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in selected:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(selected)
 for p in selected:assert z.read(p.relative_to(R).as_posix())==p.read_bytes()
record={'path':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath.read_bytes()),'entries':len(selected),'scope':'QA report, ledger, review findings and harnesses. Full captures/parent/motion/source evidence remains in exact branch paths, not included in this small report ZIP. Original art source archives are not repackaged.','ledger_sha256':sha((R/'reviewed-ledger.json').read_bytes()),'inventory_entries':len(inv)}
(R/'delivery.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
