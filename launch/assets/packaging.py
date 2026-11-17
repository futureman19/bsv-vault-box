"""Offline candidate packaging. Standard-library only; no network or signing code."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
HEX = re.compile(r'^[0-9a-f]{64}$')
ROSTER = json.loads((HERE / 'roster.json').read_bytes())


def canonical(value):
    # v1 encoding: Python JSON, sorted keys, ASCII escapes, compact, no newline.
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def make_manifest(ledger):
    entries = ledger['entries']
    if (len(entries) != 201 or Counter(e['id'] for e in entries) != Counter(ROSTER.keys())
            or Counter(ledger['expected_ids']) != Counter(ROSTER.keys())):
        raise ValueError('exact roster mismatch')
    items = []
    for e in sorted(entries, key=lambda e: e['id']):
        if e['category'] != ROSTER[e['id']] or type(e['edition_supply']) is not int or e['edition_supply'] != 1:
            raise ValueError('category/supply mismatch')
        if e['approval']['user_final_approved'] is not False:
            raise ValueError('this candidate-only pipeline cannot assert final approval')
        if e['launch_ready'] is not False or not e['missing_gates']:
            raise ValueError('candidate release holds missing')
        files = []
        def add(role, record):
            if not record: return
            sha = record['sha256']
            if not HEX.fullmatch(sha) or type(record['bytes']) is not int or record['bytes'] <= 0:
                raise ValueError('invalid payload digest/size')
            files.append({'role': role, 'sha256': sha, 'bytes': record['bytes'], 'uri': 'sha256:' + sha,
                          'source': {k: record[k] for k in ('commit', 'path', 'kind') if k in record}})
        add('viewer', e['viewer'])
        if e['viewer']['bytes'] >= 5000000: raise ValueError('viewer budget')
        for s in e['model_sources']:
            role = ('model' if s['path'].endswith('.glb') else 'editable-source')
            if s['role'] != 'selected-model': role = 'historical-' + role
            add(role, s)
        if Counter(f['role'] for f in files)['model'] != 1 or not any(f['role'] == 'editable-source' for f in files):
            raise ValueError('missing/duplicate selected model or source')
        add('promotional-illustration', e['marketing'])
        if not e['provenance'].get('source_readme'): raise ValueError('missing source notice')
        add('source-notice', e['provenance'].get('source_readme'))
        add('research-brief', e['provenance'].get('research_brief'))
        if not e['source_archives']: raise ValueError('missing source archive')
        for a in e['source_archives']: add('historical-source-archive', a)
        if len({(f['role'], f['sha256']) for f in files}) != len(files):
            raise ValueError('duplicate payload role')
        files.sort(key=lambda f: (f['role'], f['sha256']))
        stable = 'urn:boxsv:collection:impossible-places:v1:' + e['id']
        certificate = {'schema': 'boxsv-detached-authenticity-fixture-v1', 'subject': stable,
                       'issuer': 'urn:boxsv:fixture:issuer:NOT-TRUSTED', 'signature': None,
                       'status': 'UNSIGNED-FIXTURE-NOT-AUTHENTICATED', 'is_nft': False,
                       'files_commitment': 'sha256:' + digest(canonical(files)),
                       'binding': 'candidate bytes only; no origin outpoint, owner or custody claim'}
        items.append({'id': stable, 'slug': e['id'], 'name': e['name'], 'category': e['category'],
                      'edition_supply': 1, 'files': files, 'certificate': certificate,
                      'approval': e['approval'], 'missing_gates': e['missing_gates'], 'launch_ready': False,
                      'visual_limitations': e['visual_limitations'], 'historical_archive_checks': e['source_archives'],
                      'marketing_provenance': e['marketing']['provenance'],
                      'rights': 'Source notice included; research brief included where available. No blanket license granted. Rights clearance pending. Promotional illustration differs from model.',
                      'selected_candidate': e['selection']})
    return {'schema': 'boxsv-candidate-package-v1', 'canonical_encoding': 'sorted-ascii-json-v1',
            'status': 'CANDIDATE-NOT-FINAL-NOT-MINTABLE', 'supply': {'Country': 195, 'Ocean': 5, 'Moon': 1, 'total': 201},
            'input_sha256': digest(canonical({**ledger, 'entries': sorted(entries, key=lambda e: e['id'])})), 'roster_sha256': digest(canonical(ROSTER)),
            'items': items, 'custody': 'Inner collectible only. No outer vault enforcement or chain issuance proven by packaging.',
            'authenticity': 'Integrity is not issuer authenticity. Certificates are unsigned deterministic fixtures. No keys loaded or created.',
            'storage': 'sha256 URIs are local content identifiers, not IPFS CIDs or availability promises. No permanent storage selected.'}


def unique_files(manifest):
    refs = {}
    for item in manifest['items']:
        for f in item['files']:
            sha = f['sha256']
            if not HEX.fullmatch(sha) or f['uri'] != 'sha256:' + sha:
                raise ValueError('invalid content address')
            if sha in refs and refs[sha]['bytes'] != f['bytes']:
                raise ValueError('conflicting payload size')
            refs[sha] = f
    return refs


def verify_payloads(manifest, root):
    refs = unique_files(manifest)
    total = 0
    for sha, ref in refs.items():
        p = Path(root) / 'blobs' / sha
        if not p.is_file() or p.is_symlink(): raise ValueError('missing payload: ' + sha)
        data = p.read_bytes()
        if len(data) != ref['bytes'] or digest(data) != sha: raise ValueError('payload integrity: ' + sha)
        total += len(data)
    return {'unique_blobs': len(refs), 'blob_bytes': total, 'items': len(manifest['items'])}


def verify(root, expected):
    root = Path(root)
    data = (root / 'manifest.json').read_bytes()
    if not HEX.fullmatch(expected) or digest(data) != expected: raise ValueError('trusted manifest hash mismatch')
    manifest = json.loads(data)
    ledger = json.loads((root / 'ledger.json').read_bytes())
    if data != canonical(make_manifest(ledger)): raise ValueError('manifest semantics mismatch')
    expected_names = set(unique_files(manifest))
    if {p.name for p in (root / 'blobs').iterdir()} != expected_names: raise ValueError('unexpected/missing blob inventory')
    return verify_payloads(manifest, root)


def source_bytes(ref):
    source = ref['source']
    if 'commit' in source:
        if not re.fullmatch('[0-9a-f]{40}', source['commit']): raise ValueError('immutable commit required')
        return subprocess.check_output(['git', 'show', source['commit'] + ':' + source['path']])
    # Local historical archives only; paths are read-only provenance inputs.
    if source.get('kind') != 'local': raise ValueError('unsupported source')
    return Path(source['path']).read_bytes()


def build(ledger_path, output):
    ledger = json.loads(Path(ledger_path).read_bytes())
    manifest = make_manifest(ledger)
    root = Path(output)
    root.mkdir(parents=True, exist_ok=False)
    (root / 'blobs').mkdir()
    (root / 'ledger.json').write_bytes(canonical(ledger))
    for sha, ref in unique_files(manifest).items():
        data = source_bytes(ref)
        if digest(data) != sha or len(data) != ref['bytes']: raise ValueError('source integrity: ' + str(ref['source']))
        (root / 'blobs' / sha).write_bytes(data)
    data = canonical(manifest)
    (root / 'manifest.json').write_bytes(data)
    (root / ('manifest-' + digest(data) + '.json')).write_bytes(data)
    for name in ('packaging.py', 'roster.json'):
        shutil.copyfile(HERE / name, root / name)
    result = verify(root, digest(data))
    result['manifest_sha256'] = digest(data)
    return result


def recover(root, expected, output):
    report = verify(root, expected)
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_bytes())
    destination = Path(output)
    destination.mkdir(parents=True, exist_ok=False)
    suffixes = {'viewer': '.html', 'model': '.glb', 'editable-source': '.blend',
                'promotional-illustration': '.webp', 'source-notice': '.md', 'research-brief': '.md',
                'historical-source-archive': '.zip', 'historical-model': '.glb', 'historical-editable-source': '.blend'}
    copied = []
    for item in manifest['items']:
        folder = destination / item['slug']
        folder.mkdir()
        (folder / 'metadata.json').write_bytes(canonical(item))
        (folder / 'certificate-UNSIGNED-FIXTURE.json').write_bytes(canonical(item['certificate']))
        for index, f in enumerate(item['files']):
            target = folder / (f['role'] + '-' + str(index) + suffixes[f['role']])
            shutil.copyfile(root / 'blobs' / f['sha256'], target)
            if digest(target.read_bytes()) != f['sha256']: raise ValueError('recovery copy mismatch')
            copied.append({'path': target.relative_to(destination).as_posix(), 'sha256': f['sha256'], 'bytes': f['bytes']})
    (destination / 'recovery-inventory.json').write_bytes(canonical(copied))
    return {**report, 'recovered_files': len(copied), 'website_used': False, 'git_used': False}


def archive(root, expected, output):
    verify(root, expected)
    root = Path(root)
    # Explicit allowlist: no keys, caches or unrelated workspace files.
    names = ['manifest.json', 'ledger.json', 'packaging.py', 'roster.json']
    names += ['blobs/' + sha for sha in sorted(unique_files(json.loads((root / 'manifest.json').read_bytes())))]
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_STORED, allowZip64=True) as z:
        for name in names:
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            z.writestr(info, (root / name).read_bytes())
    with zipfile.ZipFile(output) as z:
        if z.namelist() != names or z.testzip(): raise ValueError('archive inventory/CRC failure')
        for name in names:
            if digest(z.read(name)) != digest((root / name).read_bytes()): raise ValueError('archive integrity')
    return {'entries': len(names), 'bytes': Path(output).stat().st_size, 'sha256': digest(Path(output).read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('build'); p.add_argument('ledger'); p.add_argument('output')
    for action in ('verify', 'recover', 'archive'):
        p = sub.add_parser(action); p.add_argument('root'); p.add_argument('--expected-sha256', required=True)
        if action != 'verify': p.add_argument('output')
    args = parser.parse_args()
    if args.action == 'build': result = build(args.ledger, args.output)
    elif args.action == 'verify': result = verify(args.root, args.expected_sha256)
    elif args.action == 'recover': result = recover(args.root, args.expected_sha256, args.output)
    else: result = archive(args.root, args.expected_sha256, args.output)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
