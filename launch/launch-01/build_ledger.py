"""Read-only collection reconciliation. Writes only beside this script; no art rebuilding."""
import base64, collections, hashlib, io, json, pathlib, re, struct, subprocess, zipfile
ROOT = pathlib.Path(__file__).resolve().parent
OUTPUT = pathlib.Path('C:/Users/futur/.hermes/profiles/telegram2/output')
REVIEW = OUTPUT / 'boxsv-collection-review'

def git(*args):
    return subprocess.check_output(['git', *args])

def digest(b):
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def save(path, obj):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

class Blobs:
    def __init__(self):
        self.p = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    def get(self, spec):
        self.p.stdin.write((spec+'\n').encode()); self.p.stdin.flush()
        h = self.p.stdout.readline().split()
        if h[-1] == b'missing': raise ValueError(spec)
        data = self.p.stdout.read(int(h[2])); assert self.p.stdout.read(1) == b'\n'
        return data

B = Blobs()
def record(commit, path):
    return {'commit':commit, 'path':path, **digest(B.get(commit+':'+path))}

def main():
    original = (REVIEW/'manifest.json').read_bytes()
    manifest = json.loads(original)
    expected = manifest['expected_country_slugs']+manifest['expected_ocean_slugs']+['the-moon']
    assert len(expected)==len(set(expected))==201
    assert sorted(expected)==sorted(e['id'] for e in manifest['entries'])
    master = git('rev-parse','origin/master').decode().strip()
    marketing_bytes = B.get(master+':docs/assets/gallery/manifest.json')
    marketing = json.loads(marketing_bytes)
    assert sorted(expected)==sorted(e['id'] for e in marketing['entries'])
    promo = {e['id']:e for e in marketing['entries']}
    save('inputs/review-manifest.json',manifest)
    save('inputs/marketing-manifest.json',marketing)
    archives = list(OUTPUT.glob('boxsv*/*.zip'))
    entries=[]
    for number,e in enumerate(manifest['entries'],1):
        slug=e['id']; commit=e['commit']; remote=e['remote_ref']; version=e['version']
        viewer_path=e['viewer']['source_path']
        if slug=='united-states':
            commit='1e6b1712959013285769a152b1d50bbf119f7729'; remote='origin/art/united-states-flag-v9'; version='united-states-flag-v9'
            viewer_path='preview/'+version+'/'+version+'.html'
        tip=git('rev-parse',remote).decode().strip()
        ancestor=subprocess.run(['git','merge-base','--is-ancestor',commit,tip],capture_output=True).returncode==0
        assert ancestor,(slug,'selected commit not reachable')
        folder=str(pathlib.PurePosixPath(viewer_path).parent)
        paths=git('ls-tree','-r','--name-only',commit,folder).decode().splitlines()
        direct=[p for p in paths if str(pathlib.PurePosixPath(p).parent)==folder]
        blobs={p:B.get(commit+':'+p) for p in direct if p.endswith(('.glb','.blend')) and not p.endswith('/mechanism.blend')}
        html=B.get(commit+':'+viewer_path)
        v=record(commit,viewer_path); v['under_5000000']=len(html)<5000000
        local=OUTPUT/'boxsv-usa-flag-v9'/pathlib.Path(viewer_path).name if slug=='united-states' else REVIEW/e['viewer']['path']
        delivered={'path':str(local), 'exists':local.is_file()}
        if local.is_file(): delivered.update(digest(local.read_bytes())); delivered['matches_selected_commit']=delivered['sha256']==v['sha256']
        legacy={'commit':e['commit'],**e['viewer']}
        core=[]
        for p,data in blobs.items():
            r={'commit':commit,'path':p,**digest(data),'role':'historical-baseline' if pathlib.PurePosixPath(p).name.startswith(('baseline-','approved-')) else 'selected-model'}
            if p.endswith('.glb'):
                magic,ver,size=struct.unpack_from('<4sII',data)
                assert magic==b'glTF' and ver==2 and size==len(data)
                n,kind=struct.unpack_from('<II',data,12); assert kind==0x4e4f534a
                doc=json.loads(data[20:20+n]); r['structural_probe']={'glb_version':ver,'declared_size_matches':True,'meshes':len(doc.get('meshes',[])),'nodes':len(doc.get('nodes',[])),'embedded_buffers':all('uri' not in x for x in doc.get('buffers',[])),'embedded_in_html':base64.b64encode(data) in html}
            core.append(r)
        readme_path=folder+'/README.md'; readme=B.get(commit+':'+readme_path).decode('utf-8')
        rp=ROOT/'source-notes'/f'{slug}.md'; rp.parent.mkdir(exist_ok=True); rp.write_text(readme,encoding='utf-8')
        qa=[]
        for p in direct:
            if p.endswith('-check.json') or pathlib.PurePosixPath(p).name in ['features.json','wrap-layout.json']:
                raw=B.get(commit+':'+p)
                try: data=json.loads(raw)
                except ValueError: data={'parse_error':True}
                qa.append({'source':{'commit':commit,'path':p,**digest(raw)},'reported_result':data,'fresh_runtime_execution':False})
        save(f'qa/{slug}.json',qa)
        zip_paths=[p for p in direct if p.endswith('.zip') and 'source' in p]
        external=[p for p in archives if p.name==version+'-source.zip']
        archive_records=[]
        for location in ([('git',p) for p in zip_paths] or [('local',str(p)) for p in external]):
            kind,p=location
            raw=B.get(commit+':'+p) if kind=='git' else pathlib.Path(p).read_bytes()
            ar={'kind':kind,'path':p,**digest(raw)}
            if kind=='git': ar['commit']=commit
            try:
                with zipfile.ZipFile(io.BytesIO(raw)) as z:
                    names=z.namelist(); files=[n for n in names if not n.endswith('/')]
                    ar['entries']=len(files)
                    ar['safe_unique_paths']=len(names)==len(set(names)) and all(not n.startswith(('/', '\\')) and '..' not in pathlib.PurePosixPath(n.replace('\\','/')).parts and ':' not in n for n in names)
                    required={pathlib.PurePosixPath(viewer_path).name:html,**{pathlib.PurePosixPath(p).name:d for p,d in blobs.items()}}
                    ar['required_payloads']={}
                    for name,data in required.items():
                        hits=[name] if name in files else [n for n in files if pathlib.PurePosixPath(n).name==name]
                        ar['required_payloads'][name]=len(hits)==1 and digest(z.read(hits[0]))==digest(data)
                        if len(hits)==1 and not ar['required_payloads'][name]:
                            ar.setdefault('payload_differences',{})[name]={'archived':digest(z.read(hits[0])),'committed':digest(data),'newline_normalized_match':z.read(hits[0]).replace(b'\r\n',b'\n')==data.replace(b'\r\n',b'\n')}
                    invs=[n for n in files if pathlib.PurePosixPath(n).name=='inventory.json']
                    ar['inventory_checked']=False
                    if len(invs)==1:
                        inv=json.loads(z.read(invs[0])); prefix=str(pathlib.PurePosixPath(invs[0]).parent); prefix='' if prefix=='.' else prefix+'/'
                        if isinstance(inv,dict) and isinstance(inv.get('files'),list): inv={x['path']:x for x in inv['files']}
                        if isinstance(inv,dict) and all(isinstance(x,dict) and 'sha256' in x for x in inv.values()):
                            errors=[]
                            for name,meta in inv.items():
                                target=prefix+name
                                if target not in files or digest(z.read(target))!={'bytes':meta['bytes'],'sha256':meta['sha256']}: errors.append(name)
                            ar.update(inventory_checked=True,inventory_entries=len(inv),inventory_mismatches=errors)
                    ar['crc_error']=z.testzip()
            except Exception as exc: ar['error']=str(exc)
            archive_records.append(ar)
        pe=promo[slug]; mp='docs/'+pe['image']['src']; mb=B.get(master+':'+mp)
        from PIL import Image
        image=Image.open(io.BytesIO(mb)); image.load()
        marketing_record={'commit':master,'path':mp,**digest(mb),'dimensions':list(image.size),'matches_gallery_inventory':digest(mb)=={'bytes':pe['image']['bytes'],'sha256':pe['image']['sha256']},'provenance':pe['provenance'],'image_type':pe['imageType'],'not_model_approval':True}
        missing=['independent-current-model-visual-review','explicit-final-user-art-approval','fresh-full-source-and-browser-acceptance','storage-and-preservation-policy','mint-and-release-authorization']
        if not archive_records: missing.append('source-archive-not-located')
        elif not all(a.get('safe_unique_paths') and all(a.get('required_payloads',{}).values()) and a.get('crc_error') is None and 'error' not in a and not a.get('inventory_mismatches') for a in archive_records): missing.append('source-archive-integrity-or-required-payload-mismatch')
        if any(not a.get('inventory_checked') for a in archive_records): missing.append('complete-source-archive-inventory-not-verified')
        if not delivered.get('matches_selected_commit'): missing.append('delivered-viewer-mismatch-or-missing')
        if not v['under_5000000']: missing.append('offline-viewer-over-budget')
        if not marketing_record['matches_gallery_inventory']: missing.append('marketing-inventory-mismatch')
        status='candidate-not-final-approved'; limitations=[]; baseline=None
        if slug=='morocco':
            status='needs-user-review'; limitations=['Finish-v6 remains partial: unresolved ceramic motif fidelity; do not replace approved v5 baseline.']
            candidates=[p for p in git('ls-tree','-r','--name-only',commit,'preview/morocco-finish-v5').decode().splitlines() if p.endswith('morocco-finish-v5.html')]
            baseline=record(commit,candidates[0]) if candidates else {'status':'Approved v5 identified by source README; preserved baseline source/export, not new approval','artifacts':[record(commit,p) for p in paths if p in [folder+'/baseline/morocco.blend',folder+'/baseline/morocco.glb']]}
        if slug=='united-states':
            status='needs-user-review'; limitations=['V9 restored substantial 0.30-unit lid; stars wrap lid only, not full star-to-body continuation.','Four left/five front equal-size wrapped stars, red feet, exact #B50018 and #021F41 pigments and visible fireworks are requested; prior evidence is not final user approval.','Legacy collection-review viewer is v1 and is not the selected v9 candidate.']
            missing.append('usa-full-star-to-body-continuation-unresolved')
        entry={'id':slug,'name':e['name'],'category':e['category'],'edition_supply':1,'version':version,'selection':{'remote_ref':remote,'fetched_tip':tip,'commit':commit,'reachable_from_fetched_ref':ancestor},'approval':{'status':status,'user_final_approved':False,'prior_approved_baseline':baseline,'evidence_policy':'No new approval inferred from existence, published promotional acceptance, or old technical reports.'},'viewer':v,'delivered_viewer':delivered,'legacy_review_viewer':legacy,'model_sources':core,'source_archives':archive_records,'marketing':marketing_record,'qa':{'evidence_path':f'qa/{slug}.json','historical_report_count':len(qa),'fresh_runtime_execution':False},'provenance':{'source_readme':record(commit,readme_path),'readme_snapshot':f'source-notes/{slug}.md','research_brief':record(commit,folder+'/design-brief.md') if folder+'/design-brief.md' in paths else None},'visual_limitations':limitations,'missing_gates':missing,'launch_ready':False}
        entries.append(entry)
        print(number,slug,'archives',len(archive_records),flush=True)
    counts=dict(collections.Counter(e['category'] for e in entries)); assert counts=={'Country':195,'Ocean':5,'Moon':1}
    ledger={'schema':'boxsv-launch-candidates/1','task':'t_c9b4df48','purpose':'Immutable candidate/evidence ledger, not art approval or release authorization','roster_definition':manifest['roster_definition'],'expected_ids':expected,'counts':counts,'total':len(entries),'input_manifest':{'path':str(REVIEW/'manifest.json'),**digest(original)},'marketing_manifest':{'commit':master,'path':'docs/assets/gallery/manifest.json',**digest(marketing_bytes)},'storage_policy':'Bytes measured separately; HTML embeds model. Do not sum HTML and GLB as mandatory runtime payload. No chain storage, hosting permanence or costs approved. Source ZIP is recovery/build payload, not viewer payload.','entries':entries}
    save('launch-candidates.json',ledger)
    summary={'total':len(entries),'counts':counts,'viewer_bytes':sum(e['viewer']['bytes'] for e in entries),'viewer_max_bytes':max(e['viewer']['bytes'] for e in entries),'delivered_matches':sum(e['delivered_viewer'].get('matches_selected_commit',False) for e in entries),'archive_located':sum(bool(e['source_archives']) for e in entries),'marketing_matches':sum(e['marketing']['matches_gallery_inventory'] for e in entries),'missing_gate_counts':dict(collections.Counter(g for e in entries for g in e['missing_gates'])),'fresh_full_runtime_qa_count':0,'final_user_approved_count':0}
    save('summary.json',summary); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
