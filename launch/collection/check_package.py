"""Offline exact-byte recovery. Trust this code and inventory hash separately."""
import argparse, hashlib, json, pathlib, zipfile

def sha(b): return hashlib.sha256(b).hexdigest()
def records(raw):
    rows=json.loads(raw); names=[r['path'] for r in rows]
    if len(names)!=len(set(names)): raise ValueError('duplicate inventory path')
    for r in rows:
        p=pathlib.PurePosixPath(r['path'])
        if p.is_absolute() or '..' in p.parts or '\\' in r['path'] or ':' in r['path'] or not p.parts: raise ValueError('unsafe path')
        if p.as_posix()!=r['path'] or any(part.endswith((' ','.')) or pathlib.PureWindowsPath(part).is_reserved() for part in p.parts): raise ValueError('noncanonical or reserved path')
        if type(r['bytes']) is not int or r['bytes']<0: raise ValueError('invalid size')
    if len({n.casefold() for n in names})!=len(names): raise ValueError('case-insensitive path alias')
    return rows

def verify(archive,expected,output=None):
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        if len(names)!=len(set(names)): raise ValueError('duplicate archive member')
        raw=z.read('inventory.json')
        if sha(raw)!=expected: raise ValueError('trusted inventory mismatch')
        rows=records(raw)
        if set(names)!={r['path'] for r in rows}|{'inventory.json'}: raise ValueError('archive inventory mismatch')
        if output is not None: pathlib.Path(output).mkdir(parents=True,exist_ok=False)
        for r in rows:
            data=z.read(r['path'])
            if len(data)!=r['bytes'] or sha(data)!=r['sha256']: raise ValueError('payload mismatch: '+r['path'])
            if output is not None:
                p=pathlib.Path(output)/r['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
                if sha(p.read_bytes())!=r['sha256']: raise ValueError('recovered mismatch')
        if output is not None: (pathlib.Path(output)/'inventory.json').write_bytes(raw)
    return {'members_verified':len(rows),'bytes_verified':sum(r['bytes'] for r in rows),'recovered':output is not None,'network_required':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--expected-sha256',required=True);p.add_argument('--output');a=p.parse_args();print(json.dumps(verify(a.archive,a.expected_sha256,a.output),indent=2))
