"""Run the real candidate payload recovery with network/Git disabled, then archive."""
import hashlib
import json
from pathlib import Path
import socket
import subprocess
from unittest.mock import patch
import zipfile
import packaging as p

HERE = Path(__file__).resolve().parent
root = HERE / 'bundle-v2'
report = json.loads((HERE / 'build-final.json').read_bytes())
expected = report['manifest_sha256']
assert (root / 'packaging.py').read_bytes() == (HERE / 'packaging.py').read_bytes()
assert (root / 'roster.json').read_bytes() == (HERE / 'roster.json').read_bytes()
with patch.object(socket, 'socket', side_effect=AssertionError('network prohibited')), patch.object(subprocess, 'Popen', side_effect=AssertionError('Git/subprocess prohibited')):
    recovered = p.recover(root, expected, HERE / 'recovered-final')
    archive = p.archive(root, expected, HERE / 'boxsv-candidates-recovery.zip')
# Read back ZIP-selected canonical bytes directly, independently from recovery helper.
manifest = json.loads((root / 'manifest.json').read_bytes())
with zipfile.ZipFile(HERE / 'boxsv-candidates-recovery.zip') as z:
    assert len(z.namelist()) == len(set(z.namelist()))
    checked = 0
    for item in manifest['items']:
        for f in item['files']:
            data = z.read('blobs/' + f['sha256'])
            assert hashlib.sha256(data).hexdigest() == f['sha256'] and len(data) == f['bytes']
            checked += 1
result = {'recovery': recovered, 'archive': archive, 'all_role_references_verified_in_zip': checked,
          'network_and_subprocess_disabled': True, 'bundled_code_exactly_matches_reviewed_source': True,
          'checker_sha256': p.digest((HERE / 'packaging.py').read_bytes()),
          'roster_file_sha256': p.digest((HERE / 'roster.json').read_bytes())}
(HERE / 'acceptance-report.json').write_bytes(p.canonical(result))
(HERE / 'candidate-manifest.json').write_bytes((root / 'manifest.json').read_bytes())
print(json.dumps(result, indent=2))
