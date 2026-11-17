"""Bounded local recovery and static rollback drill; never runs a chain tool."""
import argparse
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import zipfile
from contextlib import closing

from recovery import backup, restore, sha, verify

ROOT = Path(__file__).resolve().parents[2]
PIN = '01225c6aa893122525116dcfa793ac1f3d6885ae'
MANIFEST = '8e4837ac5673a34dd170ebab7a27df1de32bfb83d1215af7de89fa284ee038a6'


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    checks = []

    def reject(label, fn):
        try:
            fn()
        except (ValueError, FileExistsError, zipfile.BadZipFile):
            checks.append(label)
        else:
            raise AssertionError('failed to reject: ' + label)

    source = ROOT / 'evidence/rehearsal'
    for row in json.loads((source / 'sha256.json').read_bytes()):
        blob = subprocess.check_output(['git', 'show', PIN + ':evidence/rehearsal/' + row['path']], cwd=ROOT)
        assert sha(blob) == row['sha256']
    checks.append('all parent committed evidence hashes matched')
    archive = out / 'rehearsal-backup.zip'
    result = backup(source, archive, MANIFEST)
    expected = result['archiveSha256']
    assert len(verify(archive, expected)) == result['files']
    checks.append('backup exact allowlist and verify')
    restore(archive, expected, out / 'restored')
    checks.append('fresh restore every byte read back')
    reject('existing archive refused', lambda: backup(source, archive, MANIFEST))
    reject('existing restore destination refused', lambda: restore(archive, expected, out / 'restored'))
    reject('untrusted source inventory refused', lambda: backup(source, out / 'bad.zip', '0' * 64))
    reject('wrong external hash refused', lambda: verify(archive, '0' * 64))
    broken = out / 'corrupt.zip'
    raw = bytearray(archive.read_bytes()); raw[len(raw)//2] ^= 1
    broken.write_bytes(raw)
    reject('archive corruption refused', lambda: restore(broken, expected, out / 'bad-restore'))
    assert not (out / 'bad-restore').exists()
    for label, name in [('traversal', '../escape'), ('extra-member', 'unexpected.txt')]:
        bad = out / (label + '.zip')
        with zipfile.ZipFile(archive) as z, zipfile.ZipFile(bad, 'w') as dest:
            for item in z.infolist():
                dest.writestr(item, z.read(item.filename))
            dest.writestr(name, b'bad')
        reject(label + ' refused even with matching outer hash', lambda: verify(bad, sha(bad.read_bytes())))
    # Actual restored fixture CLI audit, then consistent SQLite backup API snapshot.
    db = out / 'restored/operator.sqlite'
    audit = subprocess.check_output([sys.executable, 'launch/mint/dry_run.py', 'audit', '--db', str(db.resolve())], cwd=ROOT)
    (out / 'restored-audit.json').write_bytes(audit)
    with closing(sqlite3.connect(db.resolve().as_uri() + '?mode=ro', uri=True)) as src:
        with closing(sqlite3.connect(out / 'snapshot.sqlite')) as dst:
            src.backup(dst)
            assert dst.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    again = subprocess.check_output([sys.executable, 'launch/mint/dry_run.py', 'audit', '--db', str((out / 'snapshot.sqlite').resolve())], cwd=ROOT)
    assert json.loads(audit) == json.loads(again)
    checks.append('restored allocation replay and SQLite backup integrity/audit equivalence')
    # Release pointer simulation over real static files; intentionally not Pages semantics.
    releases = out / 'releases'; releases.mkdir()
    pins = {'known-good': PIN, 'candidate': subprocess.check_output(['git', 'rev-parse', 'origin/master'], cwd=ROOT).decode().strip()}
    manifests = {}
    for label, pin in pins.items():
        folder = releases / label; folder.mkdir()
        manifests[label] = {}
        for name in ['index.html', 'box-demo.html', 'gallery.html']:
            data = subprocess.check_output(['git', 'show', pin + ':docs/' + name], cwd=ROOT)
            (folder / name).write_bytes(data)
            manifests[label][name] = sha(data)
    pointer = out / 'active.json'

    def select(label):
        for name, digest in manifests[label].items():
            if sha((releases / label / name).read_bytes()) != digest:
                raise ValueError('release hash mismatch')
        temp = out / 'active.next'
        with temp.open('w') as stream:
            json.dump({'release': label, 'pin': pins[label]}, stream)
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temp, pointer)

    select('known-good'); before = pointer.read_bytes()
    select('candidate'); select('known-good')
    assert pointer.read_bytes() == before
    assert sha(db.read_bytes()) == sha((source / 'operator.sqlite').read_bytes())
    checks.append('local static candidate switch and rollback preserve ledger')
    (releases / 'candidate/index.html').write_bytes(b'broken simulated candidate')
    reject('corrupt release rejected before pointer change', lambda: select('candidate'))
    assert pointer.read_bytes() == before
    checks.append('failed candidate leaves known-good pointer intact')
    report = {'mode': 'LOCAL-NONSECRET-FIXTURE-ONLY', 'parent': PIN, **result,
              'checks': checks, 'checkCount': len(checks), 'elapsedSeconds': round(time.monotonic()-start, 3),
              'releasePins': pins, 'releaseFileHashes': manifests, 'launchReady': False,
              'limits': ['Three real HTML entrypoints only, not full-site recovery or browser acceptance',
                         'Local atomic pointer is not GitHub Pages deployment rollback',
                         'No real ledger, signing key, chain RPC, monitoring service or external backup']}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True)
    run(p.parse_args().output.resolve())
