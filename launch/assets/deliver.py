"""Create a small review/toolkit ZIP and copy the large recovery ZIP to durable output."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
ROOT = Path(__file__).resolve().parent
OUTPUT = Path.home() / '.hermes/profiles/telegram2/output/boxsv-launch-assets-v1'
OUTPUT.mkdir(parents=True, exist_ok=False)

def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()

large = OUTPUT / 'boxsv-candidates-recovery.zip'
shutil.copyfile(ROOT / large.name, large)
expected = json.loads((ROOT / 'acceptance-report.json').read_bytes())['archive']['sha256']
assert sha(large) == expected
files = sorted(p for p in ROOT.iterdir() if p.is_file() and p.suffix != '.zip' and p.name != 'delivery-report.json')
inventory = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files}
(ROOT / 'evidence-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
kit = OUTPUT / 'boxsv-assets-toolkit.zip'
with zipfile.ZipFile(kit, 'x', compression=zipfile.ZIP_DEFLATED) as z:
    for p in files + [ROOT / 'evidence-inventory.json']:
        info = zipfile.ZipInfo(p.name, (1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, p.read_bytes())
with zipfile.ZipFile(kit) as z:
    assert len(z.namelist()) == len(set(z.namelist())) and z.testzip() is None
    for name, r in inventory.items():
        data = z.read(name)
        assert len(data) == r['bytes'] and hashlib.sha256(data).hexdigest() == r['sha256']
for name in ('README.md', 'united-states-recovered.png', 'candidate-manifest.json'):
    shutil.copyfile(ROOT / name, OUTPUT / name)
report = {'large_local_recovery_archive': {'path': str(large), 'bytes': large.stat().st_size, 'sha256': sha(large)},
          'small_toolkit': {'path': str(kit), 'bytes': kit.stat().st_size, 'sha256': sha(kit)},
          'toolkit_files': len(files) + 1, 'network_upload': False,
          'distinction': 'Toolkit contains metadata, code and evidence only, NOT all art. Full recovery requires the large local archive.'}
(ROOT / 'delivery-report.json').write_text(json.dumps(report, indent=2) + '\n')
(OUTPUT / 'delivery-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
