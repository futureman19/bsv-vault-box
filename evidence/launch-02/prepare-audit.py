"""Extract pinned read-only source snapshots inside this worktree, never other worktrees."""
import io, pathlib, subprocess, tarfile, json
ROOT = pathlib.Path(__file__).resolve().parents[2]
REFS = {'bundle': 'ff5d78f1e0d486af5c882c184fc08049996ebdc8', 'funded': 'b11a382f197925fd011e8336575f8c90d7740107'}
for name, ref in REFS.items():
    dest = ROOT / '.audit-sources' / name
    dest.mkdir(parents=True, exist_ok=True)
    raw = subprocess.check_output(['git','archive',ref], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members = [m for m in archive.getmembers() if m.name.startswith(('vault/', 'mint/', 'evidence/four-ordinal-sponsored/', 'evidence/mint-canary-funded-rehearsal/')) or (m.name.startswith('BOX-') and m.name.endswith('.md'))]
        archive.extractall(dest, members=members, filter='data')
print(json.dumps(REFS, indent=2))
