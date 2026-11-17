import pathlib,json,hashlib,subprocess,zipfile,io,shutil
R=pathlib.Path(__file__).resolve().parent
P=R/'parent'; C='d1becdc7366b9781a65d29712553b77fa8355059'
def sha(b):return hashlib.sha256(b).hexdigest()
inv=json.loads((P/'evidence-inventory.json').read_text())
for n,m in inv.items():
 b=(P/n).read_bytes();assert len(b)==m['bytes'] and sha(b)==m['sha256'],n
 assert b==subprocess.check_output(['git','show',C+':launch/art-06/'+n]),n
assert sha((P/'review-results.json').read_bytes())=='188fdebbae84579ec0f91aef1fea039c550eb28af5ddea1d36eec47119ae5d72'
archives=[]
base=pathlib.Path('C:/Users/futur/Desktop/bsv-vault-box/.worktrees/t_2741eb6f/launch/art-06')
for name,h in [('art-06-evidence.zip','b1da9d940c4f4387651ba45196cdf1b783aa3a56c4908a76c43ef66631772eb4'),('art-06-captures.zip','28383d45b22b7a6770cf09af0e083c5a155148323430e9f56de45c5482bd8060')]:
 b=(base/name).read_bytes();assert sha(b)==h
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  names=z.namelist();assert len(names)==len(set(names));assert z.testzip() is None
  for n in names:
   assert not n.startswith(('/','\\')) and ':' not in n and '..' not in pathlib.PurePosixPath(n).parts
   assert (P/n).read_bytes()==z.read(n),n
  archives.append({'path':str(base/name),'sha256':h,'bytes':len(b),'members_verified':len(names)})
for n in ['prepare.py','archive_checks.py','motion_checks.py','smoke_viewers.py','parent-ledger.json']:
 shutil.copyfile(P/n,R/n)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('__pycache__/\n*.zip\n')
report={'parent_commit':C,'parent_inventory_matches':len(inv),'parent_delivery_zip_readbacks':archives,'final_capture_hashes':{n:m for n,m in inv.items() if n.startswith('smoke/')},'capture_policy':'Immutable final parent images preserved; fresh runtime captures stored separately.'}
(R/'input-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'inventory':len(inv),'archives':archives},indent=2))
