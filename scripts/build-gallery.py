"""Build static gallery assets from the supplied review archive; no artwork generation.
Usage: python scripts/build-gallery.py --review PATH --marketing PATH
Requires Pillow==13.0.0. Source viewers stay outside the published site.
"""
import argparse
import base64
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--marketing', type=Path, required=True)
    args = parser.parse_args()
    raw = (args.review / 'manifest.json').read_bytes()
    source = json.loads(raw)
    entries = source['entries']
    expected = set(source['expected_country_slugs'] + source['expected_ocean_slugs'] + ['the-moon'])
    assert len(entries) == len(expected) == 201
    assert {e['id'] for e in entries} == expected
    assert Counter(e['category'] for e in entries) == {'Country': 195, 'Ocean': 5, 'Moon': 1}
    dest = ROOT / 'docs/assets/gallery'
    dest.mkdir(parents=True, exist_ok=True)
    result = []
    for entry in entries:
        slug = entry['id']
        marketing = slug in ('iceland', 'japan', 'the-moon', 'morocco')
        if marketing:
            path = (ROOT / 'docs/assets/collection/saturn-over-the-atlas.jpg') if slug == 'morocco' else args.marketing / (('moon' if slug == 'the-moon' else slug) + '-final.png')
            data = path.read_bytes()
            provenance = {'source': path.name, 'sha256': sha(data), 'kind': 'Existing promotional illustration; not a model screenshot'}
        else:
            viewer = (args.review / entry['viewer']['path']).read_bytes()
            assert sha(viewer) == entry['viewer']['sha256'], slug
            candidates = re.findall(rb'data:image/(?:jpeg|png);base64,([A-Za-z0-9+/=]+)', viewer)
            matches = [base64.b64decode(c) for c in candidates if sha(base64.b64decode(c)) == entry['thumbnail']['source_sha256']]
            assert matches, f'No hash-matched model poster: {slug}'
            data = matches[0]
            provenance = {'source': entry['thumbnail']['source_path'], 'sha256': sha(data), 'commit': entry['commit'], 'kind': 'Actual-model poster extracted from hash-verified standalone viewer'}
        image = Image.open(io.BytesIO(data)).convert('RGB')
        record = {k: entry[k] for k in ('id', 'name', 'category')}
        record.update(imageType='Promotional art' if marketing else 'Model preview', provenance=provenance)
        for key, bound, quality in [('thumbnail', 600, 80), ('image', 1400, 85)]:
            scaled = image.copy()
            scaled.thumbnail((bound, bound), Image.Resampling.LANCZOS)
            name = f'{slug}{"-thumb" if key == "thumbnail" else ""}.webp'
            path = dest / name
            scaled.save(path, 'WEBP', quality=quality, method=6)
            record[key] = {'src': f'assets/gallery/{name}', 'width': scaled.width, 'height': scaled.height, 'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())}
        result.append(record)
    manifest = {'schema': 1, 'sourceManifestSha256': sha(raw), 'counts': dict(Counter(e['category'] for e in result)), 'rosterDefinition': source['roster_definition'], 'entries': result}
    (dest / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'designs': len(result), 'categories': manifest['counts'], 'imageTypes': dict(Counter(e['imageType'] for e in result)), 'imageBytes': sum(e[k]['bytes'] for e in result for k in ('thumbnail', 'image'))}))

if __name__ == '__main__':
    main()
