import pathlib,json,hashlib,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and str(p.relative_to(R)) not in ['evidence-inventory.json','qa-art-02-evidence.zip','qa-art-02-report.zip','delivery.json','stage-verification.txt']]
inv={str(p.relative_to(R)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
(R/'evidence-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
zp=R/'qa-art-02-evidence.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files+[R/'evidence-inventory.json']:z.write(p,str(p.relative_to(R)).replace('\\','/'))
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(files)+1
    assert {'reviewed-ledger.json','independent-visual.json','byte-verification.json','smoke-results.json','motion-results.json','README.md','evidence-inventory.json'}<=set(z.namelist())
    for n,m in inv.items():
        b=z.read(n);assert len(b)==m['bytes'] and sha(b)==m['sha256']
d={'archive':str(zp),'archive_bytes':zp.stat().st_size,'archive_sha256':sha(zp.read_bytes()),'archive_entries':len(files)+1,'inventory_entries':len(files),'ledger_sha256':sha((R/'reviewed-ledger.json').read_bytes()),'scope':'QA evidence, not source model archive'}
small={n:m for n,m in inv.items() if '/' not in n or n.startswith('parent/boards/')}
sp=R/'qa-art-02-report.zip'
with zipfile.ZipFile(sp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n in small:z.write(R/n,n)
    z.writestr('report-inventory.json',json.dumps(small,indent=2)+'\n')
with zipfile.ZipFile(sp) as z:
    assert z.testzip() is None and len(z.namelist())==len(small)+1
    for n,m in small.items():assert sha(z.read(n))==m['sha256']
d.update(report_archive=str(sp),report_bytes=sp.stat().st_size,report_sha256=sha(sp.read_bytes()),report_entries=len(small)+1)
(R/'delivery.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(d,indent=2))
