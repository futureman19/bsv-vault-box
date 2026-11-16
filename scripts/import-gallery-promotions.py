"""Import reviewed native originals. Pillow==13.0.0; no generation or model edits.
Run with --batches PATH_TO_boxsv-marketing-complete. Baseline is pinned below.
All input validation completes before writes. Re-running reproduces output bytes.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fd5cf2aa5d84655fecf361fff5b0b00b0c36c05e'
HELD = set('madagascar arctic-ocean brunei estonia france cameroon malaysia romania slovakia united-states venezuela'.split())
ALLOWED = {'accepted', 'accepted_with_caveat', 'reviewed_with_limitations', 'reviewed_pass', 'reviewed_pass_with_limitations', 'reviewed'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def baseline(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{BASE}:{path}'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batches', type=Path, required=True)
    args = parser.parse_args()
    batches = args.batches.resolve()
    manifest_path = 'docs/assets/gallery/manifest.json'
    site = json.loads(baseline(manifest_path))
    entries = {e['id']: e for e in site['entries']}
    expected = {i for i, e in entries.items() if e['imageType'] == 'Model preview'}
    assert len(expected) == 197
    records, inputs = [], []
    for batch in range(5):
        path = batches / f'batch-{batch}/manifest.json'
        data = path.read_bytes()
        source = json.loads(data)
        inputs.append({'path': path.relative_to(batches).as_posix(), 'sha256': sha(data)})
        rows = source.get('records', source.get('entries'))
        assert len(rows) == source['assigned_count']
        for row in rows:
            slug = row['id']
            assert slug in expected and row['name'] == entries[slug]['name'], slug
            assert row['source_sha256'] == entries[slug]['image']['sha256'], slug
            assert sha(baseline('docs/' + entries[slug]['image']['src'])) == row['source_sha256'], slug
            # Each worker stored the native provider bytes under a different schema.
            if batch == 0:
                native = dict(path=row['generated_output_path'], sha256=row['output_sha256'], dimensions=row['dimensions'])
            elif batch == 1:
                native = row['provider_original']
            elif batch == 2:
                native = dict(path=row['generated_path'], sha256=row['generated_sha256'], dimensions=row['dimensions'])
            elif batch == 3:
                native = row['native_generated']
            else:
                native = dict(path=row['provider_original_path'], sha256=row['provider_original_sha256'], dimensions=row['provider_original_dimensions'])
            # Resolve archived Windows paths relative to the supplied archive root.
            relative = native['path'].replace('\\', '/').split('/boxsv-marketing-complete/', 1)[1]
            assert '..' not in Path(relative).parts and relative.startswith(f'batch-{batch}/')
            image_path = batches / relative
            assert sha(image_path.read_bytes()) == native['sha256'], slug
            with Image.open(image_path) as image:
                assert list(image.size) == native['dimensions'], slug
                image.verify()
            notes = row.get('inspection_notes', row.get('visual_review'))
            if isinstance(notes, dict):
                notes = notes['notes']
            assert notes and row.get('provider') == 'xai' and row.get('model') == 'grok-imagine-image', slug
            held = slug in HELD
            assert held or row['status'] in ALLOWED, (slug, row['status'])
            records.append({'id': slug, 'batch': batch, 'releaseStatus': 'held' if held else 'accepted-with-documented-limitations',
                            'reviewStatus': row['status'], 'acceptance': row.get('acceptance'), 'notes': notes,
                            'source': {'src': entries[slug]['image']['src'], 'sha256': row['source_sha256']},
                            'original': {'path': relative, 'sha256': native['sha256'], 'dimensions': native['dimensions']},
                            'provider': row['provider'], 'model': row['model'], 'providerUrl': row['provider_url'],
                            'exactModelEquivalenceClaimed': False})
    assert len(records) == len({r['id'] for r in records}) == 197
    assert {r['id'] for r in records} == expected
    assert {r['id'] for r in records if r['releaseStatus'] == 'held'} == HELD
    repair_path = batches / 'repairs/manifest.json'
    repair_bytes = repair_path.read_bytes()
    repairs = json.loads(repair_bytes)
    assert repairs['schema'] == 1
    assert repairs['presentation_transform'] == 'none; native provider bytes preserved; no square padding'
    assert len(repairs['records']) == len(HELD)
    assert {r['id'] for r in repairs['records']} == HELD
    inputs.append({'path': 'repairs/manifest.json', 'sha256': sha(repair_bytes)})
    for path, digest in repairs['prior_manifest_hashes'].items():
        relative = path.replace('\\', '/').split('/boxsv-marketing-complete/', 1)[1]
        assert sha((batches / relative).read_bytes()) == digest
    by_id = {r['id']: r for r in records}
    for repair in repairs['records']:
        slug = repair['id']
        record = by_id[slug]
        assert repair['status'] == 'accepted' and repair['approved_for_gallery'] is True and repair['inspected'] is True, slug
        assert repair['source_sha256'] == record['source']['sha256'], slug
        selected = [a for a in repair['attempts'] if a['attempt'] == repair['selected_attempt']]
        assert len(selected) == 1
        selected = selected[0]
        assert selected['status'] == 'accepted' and selected['inspected'] is True
        for key in ('output_sha256', 'dimensions', 'provider_url', 'visual_verdict'):
            assert selected[key] == repair[key], (slug, key)
        relative = repair['generated_output_path'].replace('\\', '/').split('/boxsv-marketing-complete/', 1)[1]
        assert relative == f'repairs/{slug}.png'
        raw = (batches / relative).read_bytes()
        assert sha(raw) == repair['output_sha256'] and len(raw) == repair['output_bytes']
        attempt_relative = selected['generated_output_path'].replace('\\', '/').split('/boxsv-marketing-complete/', 1)[1]
        assert attempt_relative == f"repairs/{slug}-attempt-{repair['selected_attempt']}.png"
        assert (batches / attempt_relative).read_bytes() == raw
        with Image.open(batches / relative) as image:
            assert list(image.size) == repair['dimensions']
            image.verify()
        prior = dict(record)
        record.update(releaseStatus='accepted-with-documented-limitations', reviewStatus=repair['status'],
                      notes=repair['visual_verdict'], acceptance='Explicit inspected repair approved for gallery',
                      original={'path': relative, 'sha256': repair['output_sha256'], 'dimensions': repair['dimensions']},
                      provider=repairs['provider'], model=repairs['model'], providerUrl=repair['provider_url'],
                      priorProvenance=prior,
                      repair={'manifest': 'repairs/manifest.json', 'selectedAttempt': repair['selected_attempt'],
                              'selectedNativePath': attempt_relative, 'priorRejectionNotes': repair['prior_rejection_notes'],
                              'attempts': [{k: a[k] for k in ('attempt', 'status', 'output_sha256', 'dimensions', 'provider_url', 'visual_verdict', 'inspected')} for a in repair['attempts']]})
    accepted = records
    assert len(accepted) == 197 and all(r['releaseStatus'] != 'held' for r in accepted)
    # Freeze the four original marketing designs byte-for-byte.
    for slug, entry in entries.items():
        if slug not in expected:
            for kind in ('thumbnail', 'image'):
                p = 'docs/' + entry[kind]['src']
                assert (ROOT / p).read_bytes() == baseline(p), p
    for record in accepted:
        entry = entries[record['id']]
        image = Image.open(batches / record['original']['path']).convert('RGB')
        entry['imageType'] = 'Promotional art'
        entry['provenance'] = {
            'kind': 'AI-generated promotional illustration; not an actual-model screenshot',
            'provider': record['provider'], 'model': record['model'],
            'source': record['source']['src'], 'sourceSha256': record['source']['sha256'],
            'sha256': record['original']['sha256'], 'nativeDimensions': record['original']['dimensions'],
            'reviewStatus': record['reviewStatus'], 'reviewNotes': record['notes'],
            'exactModelEquivalenceClaimed': False,
            'transform': 'Native provider original resized proportionally and WebP encoded; no cropping or added padding'}
        record['outputs'] = {}
        for key, bound, quality in [('thumbnail', 600, 80), ('image', 1400, 85)]:
            scaled = image.copy()
            scaled.thumbnail((bound, bound), Image.Resampling.LANCZOS)
            path = ROOT / 'docs' / entry[key]['src']
            scaled.save(path, 'WEBP', quality=quality, method=6)
            entry[key] = dict(src=entry[key]['src'], width=scaled.width, height=scaled.height,
                              bytes=path.stat().st_size, sha256=sha(path.read_bytes()))
            record['outputs'][key] = entry[key]
    site['imageTypeCounts'] = dict(Counter(e['imageType'] for e in site['entries']))
    assert site['imageTypeCounts'] == {'Promotional art': 201}
    (ROOT / manifest_path).write_text(json.dumps(site, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    release = {'schema': 'boxsv-marketing-release-v2', 'baselineCommit': BASE,
               'sourceManifests': inputs, 'counts': {'validated': 197, 'accepted': 197, 'held': 0, 'repaired': 11},
               'policy': 'Review-qualified promotional illustrations only; no exact-model equivalence. Native originals; no square padding. Explicitly accepted repairs supersede held candidates with prior provenance retained.',
               'entries': sorted(records, key=lambda r: r['id'])}
    out = ROOT / 'evidence/marketing-gallery-release'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'normalized-manifest.json').write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'validated': len(records), 'imported': len(accepted), 'held': [], 'imageTypes': site['imageTypeCounts'], 'imageBytes': sum(e[k]['bytes'] for e in site['entries'] for k in ('thumbnail', 'image'))}))

if __name__ == '__main__':
    main()
