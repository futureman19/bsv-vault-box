import pathlib,json,hashlib,zipfile
R=pathlib.Path(__file__).resolve().parent
skip={'art-04-report.zip','evidence-inventory.json','delivery.json','package-output.txt'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in skip and p.suffix!='.zip' and '__pycache__' not in p.parts)
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}
(R/'evidence-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
with zipfile.ZipFile(R/'art-04-report.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in paths+[R/'evidence-inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'art-04-report.zip') as z:
 names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
 assert {'README.md','review-results.json','parent-ledger.json','visual-findings.json','archive-results.json','test_ledger.py'}<=set(names)
 for n,m in inv.items():
  b=z.read(n);assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
p=R/'art-04-report.zip';report={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inventory_entries':len(inv),'zip_readback':'pass','review_results_sha256':hashlib.sha256((R/'review-results.json').read_bytes()).hexdigest()}
report['delivery_parts']=[]
for name,captures in [('art-04-evidence.zip',False),('art-04-captures.zip',True)]:
 selected=[p for p in paths if ('smoke' in p.relative_to(R).parts)==captures]
 with zipfile.ZipFile(R/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in selected+[R/'evidence-inventory.json']:z.write(p,p.relative_to(R).as_posix())
 with zipfile.ZipFile(R/name) as z:
  assert z.testzip() is None
  for p in selected:
   n=p.relative_to(R).as_posix();assert hashlib.sha256(z.read(n)).hexdigest()==inv[n]['sha256']
 p=R/name;assert p.stat().st_size<25000000
 report['delivery_parts'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entries':len(selected)})
(R/'delivery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
