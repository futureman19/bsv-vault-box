"""Independent exact-byte audit. No authoring, extraction of ZIP paths, or chain access."""
import pathlib, subprocess, hashlib, json, zipfile, io, base64, struct
R=pathlib.Path(__file__).resolve().parent
P=R/'parent'
REF='35f3506fdff02cce5e1e673beefb1d3f8dcf2a2f'
IDS='albania atlantic-ocean belarus brazil canada cote-d-ivoire dominican-republic eswatini germany haiti iraq kenya liberia maldives moldova nauru north-macedonia papua-new-guinea romania sao-tome-and-principe slovenia sri-lanka thailand turkmenistan uzbekistan'.split()
def sha(b): return hashlib.sha256(b).hexdigest()
def match(b,r):
    assert len(b)==r['bytes'] and sha(b)==r['sha256'],r
    return b
def blob(r,commit=None): return match(subprocess.check_output(['git','show',(r.get('commit') or commit)+':'+r['path']]),r)
report={'parent_commit':REF,'rows':[]}
parent=json.loads((P/'review-results.json').read_text())
assert sha((P/'review-results.json').read_bytes())=='e0863d34d1c46ffe0f5a02657eb22266d574e0dfe7a48551159999854570b677'
assert len(parent['entries'])==len(IDS)==len(set(IDS)) and {e['id'] for e in parent['entries']}==set(IDS)
inv=json.loads((P/'evidence-inventory.json').read_text())
for n,m in inv.items(): match((P/n).read_bytes(),m)
report['parent_evidence_files_verified']=len(inv)
remote=subprocess.check_output(['git','ls-remote','--heads','origin','feature/art-02-review']).decode().split()[0]
assert remote==REF
report['remote_parent_sha']=remote
archive_total=0
for e in parent['entries']:
    row={'id':e['id'],'archives':[]}
    html=blob(e['viewer']); assert len(html)<5000000
    model_bytes={m['path']:blob(m,e['selection']['commit']) for m in e['models']}
    glbs=[v for k,v in model_bytes.items() if k.endswith('.glb')]
    assert len(glbs)==1 and any(k.endswith('.blend') for k in model_bytes)
    for g in glbs:
        assert g[:4]==b'glTF' and struct.unpack_from('<II',g,4)==(2,len(g)) and base64.b64encode(g) in html
    blob(e['marketing'])
    for a in e['archives']:
        b=match(pathlib.Path(a['path']).read_bytes(),a) if pathlib.Path(a['path']).is_absolute() else blob(a,e['selection']['commit'])
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            names=z.namelist()
            assert len(names)==len(set(names)) and z.testzip() is None
            assert all(not n.startswith(('/','\\')) and ':' not in n and '..' not in pathlib.PurePosixPath(n.replace('\\','/')).parts for n in names)
            for m in [e['viewer']]+e['models']:
                leaf=pathlib.PurePosixPath(m['path']).name
                candidates=[n for n in names if n==leaf] or [n for n in names if n.endswith('/'+leaf)]
                assert any(sha(z.read(n))==m['sha256'] for n in candidates),(e['id'],leaf)
            candidates=[n for n in names if pathlib.PurePosixPath(n).name=='inventory.json']
            assert candidates,(e['id'],'missing inventory')
            n=min(candidates,key=len); inventory=json.loads(z.read(n)); prefix=str(pathlib.PurePosixPath(n).parent)
            if prefix=='.': prefix=''
            count=0
            records=inventory.get('files',inventory)
            if isinstance(records,list): records={r.get('path',r.get('name')):r for r in records}
            for name,meta in records.items():
                target=(prefix+'/' if prefix else '')+name
                match(z.read(target),meta); count+=1
            archive_total+=count
            row['archives'].append({'path':a['path'],'sha256':sha(b),'bytes':len(b),'entries':len(names),'inventory_entries_checked':count,'required_payloads':'pass','safe_paths_crc':'pass'})
    row.update(result='pass',viewer_sha256=sha(html),viewer_bytes=len(html),models=e['models'])
    report['rows'].append(row)
    (R/'byte-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(e['id'],'source/archive pass',flush=True)
report['archive_inventory_entries_verified']=archive_total
report['reviewed']=len(report['rows'])
(R/'byte-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(report['rows']),'designs;',archive_total,'archive members;',len(inv),'parent evidence hashes')
