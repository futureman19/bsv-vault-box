"""Independent promotion provenance, no-crop encoding and baseline preservation checks."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--batches', type=Path, required=True)
parser.add_argument('--redesigns', type=Path)
args = parser.parse_args()
redesigns = args.redesigns or args.batches.parent / 'boxsv-usa-flag-fireworks'
release = json.loads((ROOT / 'evidence/marketing-gallery-release/normalized-manifest.json').read_text(encoding='utf-8'))
site = json.loads((ROOT / 'docs/assets/gallery/manifest.json').read_text(encoding='utf-8'))
base = json.loads(subprocess.check_output(['git', '-C', str(ROOT), 'show', release['baselineCommit'] + ':docs/assets/gallery/manifest.json']))
sha = lambda b: hashlib.sha256(b).hexdigest()
current = {e['id']: e for e in site['entries']}
old = {e['id']: e for e in base['entries']}
assert [(e['id'], e['name'], e['category']) for e in site['entries']] == [(e['id'], e['name'], e['category']) for e in base['entries']]
assert len(release['entries']) == 197
assert release['counts'] == {'validated': 197, 'accepted': 197, 'held': 0, 'repaired': 11}
assert site['imageTypeCounts'] == {'Promotional art': 201}
repairs = {r['id']: r for r in json.loads((args.batches / 'repairs/manifest.json').read_text())['records']}
assert len(repairs) == 11
assert set(r['id'] for r in release['entries']) == {e['id'] for e in base['entries'] if e['imageType'] == 'Model preview'}
for source in release['sourceManifests']:
    assert sha((args.batches / source['path']).read_bytes()) == source['sha256']
accepted = set()
for record in release['entries']:
    slug = record['id']
    assert record['source']['sha256'] == old[slug]['image']['sha256']
    redesigned = record.get('intentionalRedesign', False)
    if redesigned:
        assert slug == 'united-states'
        override = json.loads((ROOT / release['redesignManifest']).read_text())
        assert record['original'] == {k: override[k] for k in ('path', 'sha256', 'dimensions')}
        assert record['providerUrl'] == override['providerUrl']
        assert current[slug]['provenance']['intentionalRedesign'] is True
        assert record['notes'] == override['notes'] and record['acceptance'] == override['authorization']
    raw = ((redesigns if redesigned else args.batches) / record['original']['path']).read_bytes()
    assert sha(raw) == record['original']['sha256']
    image = Image.open(io.BytesIO(raw)).convert('RGB')
    assert list(image.size) == record['original']['dimensions']
    assert record['releaseStatus'] == 'accepted-with-documented-limitations'
    source_bytes = subprocess.check_output(['git', '-C', str(ROOT), 'show', release['baselineCommit'] + ':docs/' + record['source']['src']])
    assert sha(source_bytes) == record['source']['sha256']
    if slug in repairs:
        repair_record = record['supersededProvenance'] if redesigned else record
        repair_raw = (args.batches / repair_record['original']['path']).read_bytes()
        repair = repairs[slug]
        assert repair['approved_for_gallery'] and repair['inspected'] and repair['status'] == 'accepted'
        assert repair_record['original']['sha256'] == repair['output_sha256'] == sha(repair_raw)
        assert repair_record['notes'] == repair['visual_verdict']
        assert repair_record['repair']['selectedAttempt'] == repair['selected_attempt']
        assert (args.batches / repair_record['repair']['selectedNativePath']).read_bytes() == repair_raw
        prior = repair_record['priorProvenance']
        assert prior['releaseStatus'] == 'held' and prior['source'] == record['source']
        assert sha((args.batches / prior['original']['path']).read_bytes()) == prior['original']['sha256']
        assert repair_record['repair']['attempts'] == [{k: a[k] for k in ('attempt', 'status', 'output_sha256', 'dimensions', 'provider_url', 'visual_verdict', 'inspected')} for a in repair['attempts']]
    accepted.add(slug)
    assert current[slug]['imageType'] == 'Promotional art'
    for kind, bound, quality in [('thumbnail', 600, 80), ('image', 1400, 85)]:
        copy = image.copy()
        copy.thumbnail((bound, bound), Image.Resampling.LANCZOS)
        encoded = io.BytesIO()
        copy.save(encoded, 'WEBP', quality=quality, method=6)
        metadata = current[slug][kind]
        data = (ROOT / 'docs' / metadata['src']).read_bytes()
        assert data == encoded.getvalue(), (slug, kind, 'not direct no-padding derivative')
        assert sha(data) == metadata['sha256']
        assert copy.size == (metadata['width'], metadata['height'])
assert len(accepted) == 197
preserved = 0
for slug in set(old) - accepted:
    assert current[slug] == old[slug]
    for kind in ('thumbnail', 'image'):
        meta = old[slug][kind]
        assert sha((ROOT / 'docs' / meta['src']).read_bytes()) == meta['sha256']
        preserved += 1
# Public manifest must not expose local paths or provider delivery URLs.
public = (ROOT / 'docs/assets/gallery/manifest.json').read_text(encoding='utf-8')
assert 'C:' not in public and 'Users' not in public and 'files-cdn.x.ai' not in public
changed = subprocess.check_output(['git', '-C', str(ROOT), 'diff', release['baselineCommit'], '--name-only'], text=True).splitlines()
assert all(p.startswith('docs/assets/gallery/') or p in {'docs/index.html', 'docs/gallery.html', 'docs/gallery.js', 'scripts/GALLERY.md', 'scripts/test-gallery.py', 'scripts/import-gallery-promotions.py', 'scripts/test-gallery-promotions.py', 'evidence/marketing-gallery-release/README.md', 'evidence/marketing-gallery-release/usa-redesign.json', 'evidence/marketing-gallery-release/normalized-manifest.json'} for p in changed), changed
# New redesign release: all 200 other entries and every image byte stay frozen.
published = json.loads(subprocess.check_output(['git', '-C', str(ROOT), 'show', 'c26e31b:docs/assets/gallery/manifest.json']))
changed_images = []
for entry in published['entries']:
    slug = entry['id']
    if slug != 'united-states': assert current[slug] == entry, slug
    for kind in ('thumbnail', 'image'):
        meta = entry[kind]
        if sha((ROOT / 'docs' / meta['src']).read_bytes()) != meta['sha256']: changed_images.append((slug, kind))
assert changed_images == [('united-states', 'thumbnail'), ('united-states', 'image')], changed_images
print('PASS only USA image pair changed; 200 other designs/400 images unchanged from c26e31b')
print(json.dumps({'result': 'PASS', 'roster': 201, 'sourceAndNativeHashes': 197, 'reproducedDerivatives': len(accepted)*2, 'unchangedImages': preserved, 'existingMarketingDesignsUnchanged': 4, 'held': 0, 'modelChanges': 0}))
