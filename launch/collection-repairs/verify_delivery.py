"""Read-only verification of Git index bytes and final ZIP inventories."""
from pathlib import Path
import hashlib, io, json, subprocess, zipfile
ROOT = Path(__file__).resolve().parents[2]
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def staged(path):
    return git('show', ':' + path)
def verify_zip(path, digest, size, inventory_digest):
    raw = staged(path)
    assert sha(raw) == digest and len(raw) == size, path
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        inv_raw = z.read('inventory.json')
        assert sha(inv_raw) == inventory_digest, path
        inv = json.loads(inv_raw)
        assert len(z.namelist()) == len(set(z.namelist()))
        assert set(z.namelist()) == set(inv['files']) | {'inventory.json'}
        for name, record in inv['files'].items():
            data = z.read(name)
            assert record == {'bytes': len(data), 'sha256': sha(data)}, (path, name)
        return len(z.namelist())
paths = git('diff', '--cached', '--name-only', '-z').decode().split('\0')
paths = [p for p in paths if p]
for path in paths:
    assert staged(path) == (ROOT / path).read_bytes(), ('index/worktree mismatch', path)
base = 'launch/collection-repairs/'
members = 0
packages = json.loads(staged(base + 'packages-02/report.json'))['packages']
for row in packages:
    members += verify_zip(base + 'packages-02/' + row['archive'], row['archive_sha256'], row['archive_bytes'], row['inventory_sha256'])
arts = json.loads(staged(base + 'art-delivery.json'))
for row in arts:
    members += verify_zip(base + 'deliveries/' + row['folder'] + '-source.zip', row['source_zip_sha256'], row['source_zip_bytes'], row['inventory_sha256'])
    html = staged('preview/' + row['folder'] + '/' + row['html'])
    assert len(html) == row['html_bytes'] < 5000000
    with zipfile.ZipFile(io.BytesIO(staged(base + 'deliveries/' + row['folder'] + '-source.zip'))) as z:
        for name in z.namelist():
            assert staged('preview/' + row['folder'] + '/' + name) == z.read(name), name
print(json.dumps({'index_files_equal_worktree': len(paths), 'final_archives': len(packages) + len(arts), 'verified_archive_members': members, 'standalone_budgets_pass': len(arts)}, indent=2))
