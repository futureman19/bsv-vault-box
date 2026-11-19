from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish'
rows=json.loads((D/'packages/package-check.json').read_text());entries={}
for row in rows:
 for name,v in row['inventory'].items():
  if name in entries:assert entries[name]==v
  entries[name]=v
staged=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0');staged=[p for p in staged if p]
assert staged and all(p.startswith('launch/attachment-rim-repairs/finish') or (p.startswith('preview/malta-repair-v2/historical-v1/') and p.endswith('.log') and p in entries) for p in staged)
for name in staged:
 b=(R/name).read_bytes();v={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 if name in entries:assert entries[name]==v,name
 entries[name]=v
p=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for name,v in entries.items():
 p.stdin.write((':'+name+'\n').encode());p.stdin.flush();header=p.stdout.readline().decode().strip().split();assert len(header)==3,(name,header);n=int(header[2]);b=p.stdout.read(n);assert p.stdout.read(1)==b'\n';assert n==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],name
p.stdin.close();assert p.wait()==0
out={'archive_inventory_comparisons':sum(len(r['inventory']) for r in rows),'unique_staged_or_archived_paths_checked':len(entries),'new_staged_files':len(staged),'all_index_blobs_exact':True,'scope':'Only authorized finish evidence/scripts; no art changes in this recovery commit.'}
(D/'acceptance/stage-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
