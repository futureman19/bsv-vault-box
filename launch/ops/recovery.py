"""Offline, nonsecret rehearsal packet recovery. No network or live service controls."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

MAX_BYTES = 100_000_000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe(name):
    if (not isinstance(name, str) or not name or '\\' in name or ':' in name
            or name.startswith('/') or any(x in ('', '.', '..') for x in name.split('/'))
            or any(ord(x) < 32 for x in name)):
        raise ValueError('unsafe path')
    for part in name.split('/'):
        if (part.endswith((' ', '.')) or any(c in part for c in '<>"|?*')
                or re.fullmatch(r'(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\..*)?', part)):
            raise ValueError('nonportable path')
    return PurePosixPath(name)


def inventory(root):
    rows = json.loads((root / 'sha256.json').read_bytes())
    names = set()
    for row in rows:
        if set(row) != {'path', 'bytes', 'sha256'}:
            raise ValueError('invalid inventory')
        safe(row['path'])
        if row['path'].casefold() in names or row['path'] == 'sha256.json':
            raise ValueError('duplicate path')
        names.add(row['path'].casefold())
        if (type(row['bytes']) is not int or not 0 <= row['bytes'] <= MAX_BYTES
                or not re.fullmatch('[0-9a-f]{64}', row['sha256'])):
            raise ValueError('invalid size/hash')
    return rows


def backup(root, output, expected_manifest):
    """Only the externally hash-pinned rehearsal allowlist; never a directory glob."""
    if sha((root / 'sha256.json').read_bytes()) != expected_manifest:
        raise ValueError('untrusted source inventory')
    rows = inventory(root)
    payload = {'sha256.json': (root / 'sha256.json').read_bytes()}
    for row in rows:
        file = root / row['path']
        if file.is_symlink() or root.resolve() not in file.resolve().parents:
            raise ValueError('source escape')
        data = file.read_bytes()
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('source hash mismatch: ' + row['path'])
        payload[row['path']] = data
    if sum(map(len, payload.values())) > MAX_BYTES:
        raise ValueError('packet too large')
    # Exclusive creation: no accidental overwrite of earlier evidence.
    with output.open('xb') as stream, zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(payload.items()):
            item = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, data)
    return {'archiveSha256': sha(output.read_bytes()), 'files': len(payload)}


def verify(archive, expected):
    raw = archive.read_bytes()
    if sha(raw) != expected:
        raise ValueError('archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        for n in names:
            safe(n)
        if len({n.casefold() for n in names}) != len(names):
            raise ValueError('duplicate member')
        if sum(i.file_size for i in infos) > MAX_BYTES:
            raise ValueError('packet too large')
        if any(i.is_dir() or ((i.external_attr >> 16) & 0o170000) == 0o120000 for i in infos):
            raise ValueError('nonregular member')
        rows = json.loads(z.read('sha256.json'))
        expected_names = ['sha256.json'] + [r['path'] for r in rows]
        if len(set(expected_names)) != len(expected_names) or set(names) != set(expected_names):
            raise ValueError('member set mismatch')
        payload = {n: z.read(n) for n in names}
        for row in rows:
            data = payload[row['path']]
            if len(data) != row['bytes'] or sha(data) != row['sha256']:
                raise ValueError('member hash mismatch')
    return payload


def restore(archive, expected, destination):
    payload = verify(archive, expected)  # verify everything before creating destination
    destination.mkdir(parents=False, exist_ok=False)
    for name, data in payload.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as f:
            f.write(data)
        if sha(path.read_bytes()) != sha(data):
            raise ValueError('restored readback mismatch')
    return {'files': len(payload), 'destination': str(destination), 'mode': 'OFFLINE-FIXTURE-ONLY'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    b = sub.add_parser('backup')
    b.add_argument('--source', type=Path, required=True)
    b.add_argument('--output', type=Path, required=True)
    b.add_argument('--expected-manifest', required=True)
    for cmd in ('verify', 'restore'):
        p = sub.add_parser(cmd)
        p.add_argument('--archive', type=Path, required=True)
        p.add_argument('--expected-sha256', required=True)
        if cmd == 'restore':
            p.add_argument('--destination', type=Path, required=True)
    a = parser.parse_args()
    if a.command == 'backup':
        result = backup(a.source, a.output, a.expected_manifest)
    elif a.command == 'verify':
        result = {'files': len(verify(a.archive, a.expected_sha256)), 'verified': True}
    else:
        result = restore(a.archive, a.expected_sha256, a.destination)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
