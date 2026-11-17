import pathlib,json,re
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
rows=json.loads((R/'packaging-results.json').read_text());ledger={e['id']:e for e in json.loads((R/'parent-ledger.json').read_text())['entries']};out=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for row in rows:
  slug=row['id'];path=pathlib.Path(ledger[slug]['delivered_viewer']['path']);result={'id':slug}
  c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto(path.as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');result['no_js_poster']=True;c.close()
  c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto(path.as_uri());p.wait_for_function('pilot.ready')
  result['geometry']=p.evaluate('''(()=>{let meshes=0,triangles=0,nonfinite=0;pilot.root.traverse(o=>{if(!o.isMesh)return;meshes++;let a=o.geometry.attributes.position;triangles+=(o.geometry.index?.count??a.count)/3;for(let i=0;i<a.array.length;i++)if(!Number.isFinite(a.array[i]))nonfinite++;});return {meshes,triangles,nonfinite,asset:pilot.asset}})()''');assert result['geometry']['meshes']>0 and result['geometry']['nonfinite']==0
  c.close();out.append(result);(R/'extended-results.json').write_text(json.dumps(out,indent=2)+'\n');print(slug,'noJS / finite loaded geometry pass',flush=True)
 b.close()
assert len(out)==25
