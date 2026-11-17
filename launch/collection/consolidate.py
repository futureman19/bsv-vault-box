"""Immutable review overlay and deterministic offline gallery builder. No art edits."""
import base64, collections, hashlib, html, io, json, pathlib, subprocess, zipfile
from PIL import Image
HERE=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-collection-consolidated-v1')
PINS=[('45e69632c56c786dbf84ab6484d6b352f482c5c6','fd44ba989215f7a72c97a6e0d2ad9408ffefa0dedbfa1fd78c7ac8dac0b6432d'),('d6a689fd19cfddcc5fef52606f4e581938a8a004','37a0cc7efd2d00d2285d393ad7e8e8ad019da596f19d67169cd0dfe91ed4d09c'),('c869c72179ff59e534712b05aede3fecf7e341ae','970033c08d45a20b18ac595df60102492252f91dd075443387e4c313e26c8033'),('0e22c22c36e6c24b209b25e130b6f65dba12eb72','dcc85510352512b8bce1714f4ee2aba7158c53cea95950763894d1ed149e6e5e'),('94cc84a05d761f468899ed7851ad35a9faeb23b7','e275ea43d9f5d59afca849f9edb4268dc42e15f4da899ba6624b76b8f9ca3f44'),('bb6301f93b47613838f53fbaba43f47b7b1d78c6','8ae0414e820f095bd67472eb859e603ae2ddbcc2b3b583e784b3e51e13275466'),('bbb25bbe647887c394be8f28794b53e8b5a07454','539b0f571210bd92491c079421db549200aeb2aace04563c43ad31c5bc684da2'),('2b63e124d6131233cee9fb4c97c23cdb4bf91d52','187f34146e3afa9447057b147bc590003e740168cc7517a52dd2199f61847a0a')]
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(d): return json.dumps(d,sort_keys=True,ensure_ascii=True,indent=2).encode()+b'\n'
def git(c,p): return subprocess.check_output(['git','show',c+':'+p])
def save(p,b): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
def aggregate(manifest,ledgers):
    assert len(manifest['items'])==201 and len({i['slug'] for i in manifest['items']})==201, 'duplicate/missing manifest ID'
    items={i['slug']:i for i in manifest['items']}; rows=[]
    ids=[e['id'] for d in ledgers for e in d['entries']]
    assert collections.Counter(ids)==collections.Counter(items.keys()), 'exact roster mismatch'
    for n,d in enumerate(ledgers,1):
        assert not d.get('unreviewed_ids',d.get('unreviewed',[]))
        for e in d['entries']:
            item=items[e['id']]; source=e.get('source_record',e); viewer=source['viewer']; original=next(f for f in item['files'] if f['role']=='viewer')
            assert (viewer['sha256'],viewer['bytes'])==(original['sha256'],original['bytes']),e['id']
            assert viewer['bytes']<5000000
            verdict=e.get('verdict',e.get('visual_verdict')); assert verdict in ['bounded-candidate-pass','candidate-with-limitations','needs-user-review']
            assert not any(e.get(k,False) for k in ['art_changed','model_changed','final_approval','user_final_approved','launch_ready'])
            rows.append({'id':e['id'],'name':item['name'],'category':item['category'],'batch':n,'verdict':'candidate-with-limitations' if verdict=='bounded-candidate-pass' else verdict,'final_user_approved':False,'launch_ready':False,'art_changed':False,'selected_candidate':item['selected_candidate'],'viewer':viewer,'approval':item['approval'],'last_approved_baseline':item['approval']['prior_approved_baseline'],'baseline_policy':'Null means not established by these records; candidate is never promoted to approved baseline. Existing versions remain immutable.','package_history':item['historical_archive_checks'],'package_missing_gates':item['missing_gates'],'independent_review':e,'files':item['files']})
    return {'schema':'boxsv-consolidated-independent-review/1','coverage':dict(collections.Counter(r['category'] for r in rows)),'counts':dict(collections.Counter(r['verdict'] for r in rows)),'changed_art':[],'final_approvals':0,'launch_ready':False,'entries':sorted(rows,key=lambda r:r['id'])}

def gallery(ledger, thumbnails, standalone=False):
    esc=html.escape; cards=[]
    for r in ledger['entries']:
        id=r['id']; review=r['independent_review']; text=json.dumps({k:v for k,v in review.items() if any(x in k for x in ['visual','finding','reason','adjudication','hold','gate'])},ensure_ascii=False,indent=2)
        img='data:image/jpeg;base64,'+base64.b64encode(thumbnails[id]).decode() if standalone else 'boards/'+id+'.jpg'
        links='' if standalone else f'<a href="payloads/{id}/viewer.html">Open unchanged interactive model</a> · <a href="boards/{id}.jpg">Full comparison</a>'
        cards.append(f'<article data-kind="{r["category"]}" data-hold="{str(r["verdict"]=="needs-user-review").lower()}" data-search="{esc((id+" "+id.replace("-"," ")+" "+r["name"]).lower())}"><h2>{esc(r["name"])}</h2><p class="verdict">{r["verdict"]}</p><img loading="lazy" src="{img}" alt="{esc(r["name"])} inherited promotional versus actual-model comparison"><p>{links}</p><details><summary>Decision notes and unresolved gates</summary><pre>{esc(text)}</pre><p>Final approval: not granted. Prior approved baseline: {esc(json.dumps(r["last_approved_baseline"]))}. Full immutable review and packaging history in ledger.</p></details></article>')
    return ('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BoxSV · 201 candidate reviews</title><style>*{box-sizing:border-box}body{margin:0;background:#121719;color:#eee;font:16px system-ui;line-height:1.5}header,main{max-width:1440px;margin:auto;padding:24px}h1{font-size:clamp(28px,5vw,48px);margin:0}header p{max-width:85ch;color:#c5c9c7}nav{display:flex;gap:12px;flex-wrap:wrap}input,select{font:inherit;padding:12px;background:#242b2e;color:white;border:1px solid #607075;max-width:100%}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,350px),1fr));gap:20px}article{background:#202729;padding:16px;border:1px solid #3b474a;border-radius:12px;min-width:0}article[hidden]{display:none}h2{margin:0}img{width:100%;height:auto}a{color:#eed49b}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px system-ui}.verdict{color:#eed49b}summary{cursor:pointer}#count{font-weight:bold}</style><header><p>BOXSV / INTERNAL COLLECTION REVIEW</p><h1>201 designs. No final approvals.</h1><p>195 countries, five oceans and Moon; one-of-one each, equal edition scarcity. These are unchanged inner collectible candidates, not outer custody vaults or minted tokens. Promotional illustrations differ from actual models. No artwork changed in the eight reviewed batches or this consolidation: no fabricated before/after improvements.</p>'''+f'<p><b>{ledger["counts"].get("needs-user-review",0)} user/package decision holds</b>; {ledger["counts"].get("candidate-with-limitations",0)} candidates with limitations. All final art, rights, storage and release approvals remain held. USA v9 star-to-body continuation is unresolved. Historical exact-byte archive holds: Iceland, Morocco, Rwanda; unchecked full inner inventories: Iceland, Morocco, Namibia, New Zealand, Paraguay.</p>'+('<p>Standalone comparison overview only. Interactive models are in the separately delivered full local archive; this file has no missing viewer links.</p>' if standalone else '<p>Open any unchanged model below. Comparison boards are inherited evidence, not new renders or calibrated dimensional comparisons; full original captures remain on the pinned QA refs. Hidden hinges and physical-phone performance are not certified. See ledger.json for unabridged review and package holds.</p>')+'''<nav><input id="q" aria-label="Search designs" placeholder="Search designs"><select id="kind" aria-label="Category"><option value="">All categories</option><option>Country</option><option>Ocean</option><option>Moon</option></select><select id="hold" aria-label="Review status"><option value="">All review states</option><option value="true">Needs user review</option><option value="false">Candidates with limitations</option></select></nav><p id="count" aria-live="polite">201 designs</p></header><main>'''+''.join(cards)+'''</main><script>const q=document.querySelector('#q'),kind=document.querySelector('#kind'),hold=document.querySelector('#hold');function filter(){let n=0;for(const a of document.querySelectorAll('article')){a.hidden=!(a.dataset.search.includes(q.value.toLowerCase().trim())&&(!kind.value||kind.value===a.dataset.kind)&&(!hold.value||hold.value===a.dataset.hold));if(!a.hidden)n++}document.querySelector('#count').textContent=n+' designs'}for(const el of [q,kind,hold])el.addEventListener('input',filter);</script></html>''').encode()

def main():
    OUT.mkdir(parents=True,exist_ok=True); ledgers=[]; pins=[]; board_refs={}
    for n,(commit,expected) in enumerate(PINS,1):
        prefix=f'launch/qa-art-{n:02}'; path=prefix+'/reviewed-ledger.json'; raw=git(commit,path); assert sha(raw)==expected
        assert subprocess.check_output(['git','rev-parse',f'origin/feature/qa-art-{n:02}']).decode().strip()==commit
        save(HERE/f'inputs/qa-{n:02}.json',raw); d=json.loads(raw); ledgers.append(d); pins.append({'batch':n,'commit':commit,'path':path,'sha256':expected})
        tree=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,prefix]).decode().splitlines()
        for e in d['entries']:
            paths=[p for p in tree if p.endswith('/boards/'+e['id']+'.jpg')]
            if not paths:
                c=d['parent_commit']; t=subprocess.check_output(['git','ls-tree','-r','--name-only',c]).decode().splitlines(); paths=[p for p in t if p.endswith('/boards/'+e['id']+'.jpg')]; assert len(paths)==1; board_refs[e['id']]=(c,paths[0])
            else: assert len(paths)==1; board_refs[e['id']]=(commit,paths[0])
    manifest=json.loads((HERE/'upstream/candidate-manifest.json').read_bytes()); ledger=aggregate(manifest,ledgers); ledger['input_pins']=pins
    thumbnails={}; boards=[]
    for id,(c,p) in board_refs.items():
        b=git(c,p); save(OUT/f'boards/{id}.jpg',b); boards.append({'id':id,'commit':c,'path':p,'sha256':sha(b),'bytes':len(b)})
        im=Image.open(io.BytesIO(b)); im.thumbnail((620,620)); f=io.BytesIO(); im.convert('RGB').save(f,'JPEG',quality=65,optimize=True); thumbnails[id]=f.getvalue()
    ledger['comparison_boards']=boards
    raw=enc(ledger); save(HERE/'ledger.json',raw); save(OUT/'ledger.json',raw)
    save(HERE/'review.html',gallery(ledger,thumbnails,True)); save(OUT/'review.html',gallery(ledger,thumbnails,True)); save(OUT/'index.html',gallery(ledger,thumbnails))
    archive=pathlib.Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-launch-assets-v1/boxsv-candidates-recovery.zip')
    with archive.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()=='28c47ef3f985c4af68f1929045586e0c58cd9a1e93988e9a28fb93dc4f479947'
    inventory=[]
    suffix={'viewer':'.html','model':'.glb','editable-source':'.blend','promotional-illustration':'.webp','source-notice':'.md','research-brief':'.md','historical-source-archive':'.zip','historical-model':'.glb','historical-editable-source':'.blend'}
    with zipfile.ZipFile(archive) as z:
        assert sha(z.read('manifest.json'))==sha((HERE/'upstream/candidate-manifest.json').read_bytes())
        for item in manifest['items']:
            roles=collections.Counter()
            for f in item['files']:
                role=f['role']; roles[role]+=1; name=role+('' if roles[role]==1 else '-'+str(roles[role]))+suffix[role]; path=f'payloads/{item["slug"]}/{name}'
                b=z.read('blobs/'+f['sha256']); assert sha(b)==f['sha256'] and len(b)==f['bytes']; save(OUT/path,b); inventory.append({'path':path,'sha256':sha(b),'bytes':len(b),'id':item['slug'],'role':role})
    save(HERE/'payload-inventory.json',enc(inventory)); save(OUT/'payload-inventory.json',enc(inventory)); save(HERE/'build-report.json',enc({'coverage':ledger['coverage'],'counts':ledger['counts'],'payloads':len(inventory),'changed_art':0,'final_approvals':0,'ledger_sha256':sha(raw),'standalone_html_bytes':(OUT/'review.html').stat().st_size}))
    print((HERE/'build-report.json').read_text())
if __name__=='__main__': main()
