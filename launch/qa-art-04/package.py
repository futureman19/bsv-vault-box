import pathlib,json,hashlib,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
parent_root=R.parents[2]/'t_5369a83b'/'launch/art-04'
# Explicit absolute handoff location, never infer a Git path for a local ZIP.
parent_root=pathlib.Path('C:/Users/futur/Desktop/bsv-vault-box/.worktrees/t_5369a83b/launch/art-04')
expected={'art-04-evidence.zip':'ffa483d28c5747aa91f275138738f0a985f3b73b8dd6ee55d8fa32c2b728e692','art-04-captures.zip':'32703a4bdc223f743319843177bf2644d06173d91cbec341c725022a2e04e198'}
checks=[]
for n,h in expected.items():
 b=(parent_root/n).read_bytes();assert sha(b)==h
 with zipfile.ZipFile(parent_root/n) as z:
  names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
  for name in names:
   assert not name.startswith(('/','\\')) and '..' not in pathlib.PurePosixPath(name).parts
   local=R/'parent'/name
   if local.exists():assert local.read_bytes()==z.read(name)
 checks.append({'path':str(parent_root/n),'sha256':h,'bytes':len(b),'crc_safe_unique':True})
(R/'delivery-verification.json').write_text(json.dumps(checks,indent=2)+'\n')
files=[p for p in R.rglob('*') if p.is_file() and p.name not in ['evidence-inventory.json','qa-art-04-report.zip','package-result.json']]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
(R/'evidence-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
chosen=[p for p in R.iterdir() if p.is_file() and p.suffix in ['.json','.py','.md','.html','.txt'] and p.name not in ['parent-ledger.json','package-result.json']]
zpath=R/'qa-art-04-report.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in chosen:z.write(p,p.name)
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 assert {'review.html','reviewed-ledger.json','README.md','packaging-audit.json'}<=set(z.namelist())
 for n in z.namelist():assert z.read(n)==(R/n).read_bytes()
print('Report ZIP',zpath.stat().st_size,sha(zpath.read_bytes()),'inventory',len(inv))
print('Ledger',sha((R/'reviewed-ledger.json').read_bytes()))
